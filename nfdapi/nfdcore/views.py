# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import namedtuple
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import ugettext_lazy as _
from rest_framework import generics
from rest_framework import renderers
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.fields import empty
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import reversion

from nfdrenderers import pdf as pdfrenderers
from nfdrenderers import csv as csvrenderers
from nfdrenderers import xlsx as xlsrenderers
from nfdrenderers import shp as shprenderers

from . import constants
from . import filters
from . import itis
from . import models
from . import serializers
from .permissions import (
    CanCreateAnimals,
    CanUpdateFeatureType,
    CanCreateFungus,
    CanCreateNaturalAreas,
    CanCreatePlants,
    CanCreateSlimeMold,
    CanWriteOrUpdateAny,
    get_permissions,
)

logger = logging.getLogger(__name__)

FilterField = namedtuple("FilterField", [
    "name",
    "value",
    "lookup"
])

FeatureTypeFormCategory = namedtuple("FeatureTypeFormCategory", [
    "subtype",
    "is_writer",
    "is_publisher",
])


def get_units_part(*taxonomic_units):
    """Return a portion of the SQL used in the aggregation query"""
    taxonomic_units = list(
        taxonomic_units) if taxonomic_units else ["species"]
    select_fragments = []  # for use in the SELECT clause
    group_fragments = []  # for use in the GROUP BY clause
    for unit in taxonomic_units:
        part = "t.upper_ranks #>> '{%(unit)s, name}'" % {
            "unit": unit
        }
        select_fragments.append(part + " AS %(unit)s" % {"unit": unit})
        group_fragments.append(part)
    select_part = ", ".join(select_fragments)
    group_part = ", ".join(group_fragments)
    ordering_part = ", ".join(group_fragments[::-1])
    return select_part, group_part, ordering_part


def get_aggregation_query(taxonomic_units=None):
    """Return the SQL query that will be executed"""
    taxonomic_units = list(taxonomic_units) if taxonomic_units else []
    select_part, group_part, ordering_part = get_units_part(*taxonomic_units)
    query = """
        SELECT 
            COUNT(o.id) AS occurrences,
            {select_part}
        FROM nfdcore_occurrencetaxon AS o
            LEFT JOIN nfdcore_taxon AS t ON (t.tsn = o.taxon_id)
            LEFT JOIN nfdcore_occurrencecategory AS c ON (c.id =  o.occurrence_cat_id)
        WHERE c.main_cat = %(category)s
        GROUP BY
            {group_part}
        ORDER BY
            {ordering_part}
    """.format(
        select_part=select_part,
        group_part=group_part,
        ordering_part=ordering_part
    )
    return query


def get_aggregation_records(category, taxonomic_units):
    query = get_aggregation_query(taxonomic_units)
    with connection.cursor() as cursor:
        cursor.execute(query, {"category": category})
        ResultTuple = namedtuple(
            "Result", [col[0] for col in cursor.description])
        for row in cursor.fetchall():
            yield ResultTuple(*row)


class FeatureTypeFormViewSet(viewsets.ViewSet):
    """ViewSet for featuretype forms"""
    randerer_classes = (
        renderers.JSONRenderer,
        renderers.BrowsableAPIRenderer,
    )
    serializer_class = serializers.FormDefinitionsSerializer

    @list_route()
    def ln(self, request):
        is_writer, is_publisher = get_permissions(request.user, "animal")
        serializer = self.serializer_class(
            FeatureTypeFormCategory("ln", is_writer, is_publisher))
        return Response(serializer.data)

    @list_route()
    def st(self, request):
        is_writer, is_publisher = get_permissions(request.user, "animal")
        serializer = self.serializer_class(
            FeatureTypeFormCategory("st", is_writer, is_publisher))
        return Response(serializer.data)

    @list_route()
    def lk(self, request):
        is_writer, is_publisher = get_permissions(request.user, "animal")
        serializer = self.serializer_class(
            FeatureTypeFormCategory("lk", is_writer, is_publisher))
        return Response(serializer.data)

    @list_route()
    def we(self, request):
        is_writer, is_publisher = get_permissions(request.user, "animal")
        serializer = self.serializer_class(
            FeatureTypeFormCategory("we", is_writer, is_publisher))
        return Response(serializer.data)

    @list_route()
    def sl(self, request):
        is_writer, is_publisher = get_permissions(request.user, "slimemold")
        serializer = self.serializer_class(
            FeatureTypeFormCategory("sl", is_writer, is_publisher))
        return Response(serializer.data)

    @list_route()
    def co(self, request):
        is_writer, is_publisher = get_permissions(request.user, "plant")
        serializer = self.serializer_class(
            FeatureTypeFormCategory("co", is_writer, is_publisher))
        return Response(serializer.data)

    @list_route()
    def fe(self, request):
        is_writer, is_publisher = get_permissions(request.user, "plant")
        serializer = self.serializer_class(
            FeatureTypeFormCategory("fe", is_writer, is_publisher))
        return Response(serializer.data)

    @list_route()
    def fl(self, request):
        is_writer, is_publisher = get_permissions(request.user, "plant")
        serializer = self.serializer_class(
            FeatureTypeFormCategory("fl", is_writer, is_publisher))
        return Response(serializer.data)

    @list_route()
    def mo(self, request):
        is_writer, is_publisher = get_permissions(request.user, "plant")
        serializer = self.serializer_class(
            FeatureTypeFormCategory("mo", is_writer, is_publisher))
        return Response(serializer.data)

    @list_route()
    def fu(self, request):
        is_writer, is_publisher = get_permissions(request.user, "fungus")
        serializer = self.serializer_class(
            FeatureTypeFormCategory("fu", is_writer, is_publisher))
        return Response(serializer.data)

    @list_route()
    def na(self, request):
        is_writer, is_publisher = get_permissions(request.user, "naturalarea")
        serializer = self.serializer_class(
            FeatureTypeFormCategory("na", is_writer, is_publisher))
        return Response(serializer.data)


class ItisBackedSearchViewSet(viewsets.ViewSet):
    permission_classes = [
        IsAuthenticated,
    ]

    renderer_classes = (
        renderers.JSONRenderer,
        renderers.BrowsableAPIRenderer,
    )

    def get_serializer_class(self):
        if self.action == "list":
            result = serializers.ItisTaxonSearchSerializer
        elif self.action == "retrieve":
            result = serializers.ItisTaxonHierarchySerializer
        else:
            raise RuntimeError("Invalid action")
        return result

    def list(self, request):
        """Search for taxa on the ITIS database"""
        feature_type = request.query_params.get("featuretype")
        kingdom = {
            "animal": "Animalia",
            "fungus": "Fungi",
            "plant": "Plantae",
            "slimemold": "Fungi",
        }.get(feature_type)
        search_results = itis.search_taxon(
            request.query_params.get("search", ""),
            [kingdom] if kingdom else ["Animalia", "Plantae", "Fungi"],
            page_size=20,
        )
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(search_results, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Retrieve a taxon

        If we have a ``models.Taxon`` instance in the DB, return it.
        Otherwise search for the taxon details in ITIS DB, generate an
        in-memory ``models.Taxon`` instance and return that.

        """

        if pk is not None:
            try:
                taxon_instance = models.Taxon.objects.get(pk=pk)
                serializer_class = serializers.TaxonDetailSerializer
            except models.Taxon.DoesNotExist:
                taxon_instance = models.Taxon(tsn=pk)
                taxon_instance.populate_attributes_from_itis()
                serializer_class = self.get_serializer_class()
            serializer = serializer_class(taxon_instance)
            namespaced = {
                "taxon.{}".format(k): v for k, v in serializer.data.items()}
            result = Response(namespaced)
        else:
            result = Response({
                _("error"): _("Could not find taxon identifier")
            })
        return result


class TaxonViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = [
        IsAuthenticated,
    ]

    renderer_classes = (
        renderers.JSONRenderer,
        renderers.BrowsableAPIRenderer,
    )
    filter_backends = (
        SearchFilter,
    )
    search_fields = (
        "name",
        "upper_ranks",
    )

    queryset = models.Taxon.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            result = serializers.TaxonListSerializer
        elif self.action == "retrieve":
            result = serializers.TaxonDetailSerializer
        else:
            raise RuntimeError("Invalid action")
        return result


class OccurrenceAggregatorViewSet(viewsets.ViewSet):
    """ViewSet for occurrence stats"""

    renderer_classes = (
        renderers.JSONRenderer,
        renderers.BrowsableAPIRenderer,
        pdfrenderers.PdfOccurrenceStatsRenderer,
    )
    serializer_class = serializers.OccurrenceAggregatorSerializer

    taxonomic_units = [
        "species",
        "family",
        "phylum",
    ]

    @list_route(methods=["get",])
    def animal(self, request):
        raw_year = request.query_params.get("year")
        serializer = self.serializer_class(
            get_aggregation_records("animal", self.taxonomic_units),
            context={
                "title": "Animals",
                "year": int(raw_year) if raw_year is not None else raw_year
            }
        )
        return Response(serializer.data)

    @list_route(methods=["get",])
    def plant(self, request):
        raw_year = request.query_params.get("year")
        serializer = self.serializer_class(
            get_aggregation_records("plant", self.taxonomic_units),
            context={
                "title": "Plants",
                "year": int(raw_year) if raw_year is not None else raw_year
            }
        )
        return Response(serializer.data)

    @list_route(methods=["get",])
    def fungus(self, request):
        raw_year = request.query_params.get("year")
        serializer = self.serializer_class(
            get_aggregation_records("fungus", self.taxonomic_units),
            context={
                "title": "Fungi",
                "year": int(raw_year) if raw_year is not None else raw_year
            }
        )
        return Response(serializer.data)

    @list_route(methods=["get",])
    def slime_mold(self, request):
        raw_year = request.query_params.get("year")
        serializer = self.serializer_class(
            get_aggregation_records("slimemold", self.taxonomic_units),
            context={
                "title": "Slimemolds",
                "year": int(raw_year) if raw_year is not None else raw_year
            }
        )
        return Response(serializer.data)


class NfdLayer(generics.ListCreateAPIView):

    def get_queryset(self):
        (is_writer, is_publisher) = get_permissions(self.request.user,
                                                    self.get_main_cat())
        queryset = self.get_base_queryset()
        is_writer_or_publisher = (is_writer or is_publisher)
        if not is_writer_or_publisher:
            queryset = queryset.filter(released=True)
        return queryset

    def get_base_queryset(self):
        """Provide this method in derived classes"""
        raise NotImplementedError

    def get_main_cat(self):
        """Provide this method in derived classes"""
        raise NotImplementedError

    def get_post_serializer_class(self):
        """Provide this method in derived classes"""
        raise NotImplementedError

    def get_serializer_class(self):
        return serializers.LayerSerializer

    def get_serializer(self, instance=None, data=empty, many=False,
                       partial=False):
        # return super(NfdLayerListNew, self).get_serializer(
        #     instance=instance, data=data, many=many, partial=partial)
        (is_writer, is_publisher) = get_permissions(self.request.user,
                                                    self.get_main_cat())
        if self.request.method == 'POST':
            if data is not empty:
                serializer_class = self.get_post_serializer_class()
                request_data = data.copy()
                tsn = request_data.pop("taxon.tsn", None)
                context = {"tsn": tsn,} if tsn is not None else {}
                return serializer_class(
                    data=request_data,
                    is_writer=is_writer,
                    is_publisher=is_publisher,
                    context=context
                )
            else:
                is_writer_or_publisher = (is_writer or is_publisher)
                return serializers.LayerSerializer(
                    data=data,
                    many=many,
                    is_writer_or_publisher=is_writer_or_publisher
                )
        else:
            is_writer_or_publisher = (is_writer or is_publisher)
            serializer_class = self.get_serializer_class()
            return serializer_class(
                instance,
                many=many,
                is_writer_or_publisher=is_writer_or_publisher
            )


class PlantLayer(NfdLayer):
    permission_classes = [IsAuthenticated, CanCreatePlants]
    filter_backends = (DjangoFilterBackend, )
    filter_class = filters.OccurrenceTaxonFilterSet

    def get_post_serializer_class(self):
        return serializers.TaxonOccurrenceSerializer

    def get_base_queryset(self):
        return models.OccurrenceTaxon.objects.filter(
            occurrence_cat__main_cat=self.get_main_cat())

    def get_main_cat(self):
        return "plant"


class AnimalLayer(NfdLayer):
    permission_classes = [IsAuthenticated, CanCreateAnimals]
    filter_backends = (DjangoFilterBackend, )
    filter_class = filters.OccurrenceTaxonFilterSet

    def get_post_serializer_class(self):
        return serializers.TaxonOccurrenceSerializer

    def get_base_queryset(self):
        return models.OccurrenceTaxon.objects.filter(
            occurrence_cat__main_cat=self.get_main_cat())

    def get_main_cat(self):
        return "animal"


class FungusLayer(NfdLayer):
    permission_classes = [IsAuthenticated, CanCreateFungus]
    filter_backends = (DjangoFilterBackend, )
    filter_class = filters.OccurrenceTaxonFilterSet

    def get_post_serializer_class(self):
        return serializers.TaxonOccurrenceSerializer

    def get_base_queryset(self):
        return models.OccurrenceTaxon.objects.filter(
            occurrence_cat__main_cat=self.get_main_cat())

    def get_main_cat(self):
        return "fungus"


class SlimeMoldLayer(NfdLayer):
    permission_classes = [IsAuthenticated, CanCreateSlimeMold]
    filter_backends = (DjangoFilterBackend, )
    filter_class = filters.OccurrenceTaxonFilterSet

    def get_post_serializer_class(self):
        return serializers.TaxonOccurrenceSerializer

    def get_base_queryset(self):
        return models.OccurrenceTaxon.objects.filter(
            occurrence_cat__main_cat=self.get_main_cat())

    def get_main_cat(self):
        return "slimemold"


class NaturalAreaLayer(NfdLayer):
    permission_classes = [IsAuthenticated, CanCreateNaturalAreas]
    filter_backends = (DjangoFilterBackend, )
    filter_class = filters.NaturalAreaFilter

    def get_post_serializer_class(self):
        return serializers.NaturalAreaOccurrenceSerializer

    def get_base_queryset(self):
        return models.OccurrenceNaturalArea.objects.all()

    def get_main_cat(self):
        return "naturalarea"


class NfdListPagination(PageNumberPagination):
    page_size = 10


class NfdList(generics.ListAPIView):
    pagination_class = NfdListPagination
    filter_backends = (DjangoFilterBackend, )

    def get_base_queryset(self):
        """Provide this method in derived classes"""
        raise NotImplementedError

    def get_main_cat(self):
        """Provide this method in derived classes"""
        raise NotImplementedError

    def get_queryset(self):
        (is_writer, is_publisher) = get_permissions(self.request.user,
                                                    self.get_main_cat())
        queryset = self.get_base_queryset()
        if not (is_writer or is_publisher):
            queryset = queryset.filter(released=True)
        return queryset

    def get_serializer(self, instance=None, data=empty,
                       many=False, partial=False):
        (is_writer, is_publisher) = get_permissions(self.request.user,
                                                    self.get_main_cat())
        is_writer_or_publisher = (is_writer or is_publisher)
        serializer_class = self.get_serializer_class()
        return serializer_class(instance, many=many,
                                is_writer_or_publisher=is_writer_or_publisher)


class OccurrenceTaxonList(NfdList):
    filter_class = filters.OccurrenceTaxonFilterSet

    def get_serializer_class(self):
        return serializers.TaxonOccurrenceListSerializer

    def get_base_queryset(self):
        return models.OccurrenceTaxon.objects.filter(
            occurrence_cat__main_cat=self.get_main_cat())


class OccurrencePlantList(OccurrenceTaxonList):
    permission_classes = [IsAuthenticated, CanCreatePlants]

    def get_main_cat(self):
        return "plant"


class OccurrenceAnimalList(OccurrenceTaxonList):
    # permission_classes = [IsAuthenticated, CanCreateAnimals]

    def get_main_cat(self):
        return "animal"


class OccurrenceFungusList(OccurrenceTaxonList):
    permission_classes = [IsAuthenticated, CanCreateFungus]

    def get_main_cat(self):
        return "fungus"


class OccurrenceSlimeMoldList(OccurrenceTaxonList):
    permission_classes = [IsAuthenticated, CanCreateSlimeMold]

    def get_main_cat(self):
        return "slimemold"


class OccurrenceNaturalAreaList(NfdList):
    permission_classes = [IsAuthenticated, CanCreateNaturalAreas]
    filter_class = filters.NaturalAreaFilter

    def get_base_queryset(self):
        return models.OccurrenceNaturalArea.objects.all()

    def get_serializer_class(self):
        return serializers.NaturalAreaOccurrenceListSerializer

    def get_main_cat(self):
        return "naturalarea"


class LayerDetail(APIView):
    """
    Retrieve, update or delete an occurrence instance.
    """
    permission_classes = [IsAuthenticated, CanUpdateFeatureType]
    renderer_classes = (
        renderers.JSONRenderer,
        renderers.BrowsableAPIRenderer,
        pdfrenderers.PdfLayerDetailRenderer,
        csvrenderers.CsvRenderer,
        xlsrenderers.XlsxRenderer,
        shprenderers.ShpRenderer,
    )

    def get_object(self, occurrence_maincat, pk):
        try:
            return models.get_occurrence_model(
                occurrence_maincat).objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, occurrence_maincat, pk, format=None):
        (is_writer, is_publisher) = get_permissions(request.user,
                                                    occurrence_maincat)
        feature = self.get_object(occurrence_maincat, pk)
        if not feature.released and not (is_writer or is_publisher):
            return Response(
                {
                    _("error"): _("You don't have permissions to access the "
                                  "occurrence")
                },
                status=status.HTTP_403_FORBIDDEN
            )
        if isinstance(feature, models.OccurrenceNaturalArea):
            serializer = serializers.NaturalAreaOccurrenceSerializer(
                feature, is_writer=is_writer, is_publisher=is_publisher)
        else:
            serializer = serializers.TaxonOccurrenceSerializer(
                feature, is_writer=is_writer, is_publisher=is_publisher)
        return Response(serializer.data)

    def put(self, request, occurrence_maincat, pk, format=None):
        is_writer, is_publisher = get_permissions(
            request.user, occurrence_maincat)
        feature = self.get_object(occurrence_maincat, pk)
        if isinstance(feature, models.OccurrenceNaturalArea):
            serializer = serializers.NaturalAreaOccurrenceSerializer(
                feature, data=request.data, is_writer=is_writer,
                is_publisher=is_publisher
            )
        else:
            request_data = request.data.copy()
            tsn = request_data.pop("taxon.tsn")
            serializer = serializers.TaxonOccurrenceSerializer(
                feature,
                data=request.data,
                is_writer=is_writer,
                is_publisher=is_publisher,
                context={"tsn": tsn}
            )
        if serializer.is_valid():
            serializer.save()
            result = Response(serializer.data)
        else:
            result = Response(serializer.errors,
                              status=status.HTTP_400_BAD_REQUEST)
        return result

    def delete(self, request, occurrence_maincat, pk, format=None):
        feature = self.get_object(occurrence_maincat, pk)
        with reversion.create_revision():
            serializers.delete_object_and_children(feature)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LayerVersionDetail(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, occurrence_maincat, pk, version, format=None):
        try:
            (is_writer, is_publisher) = get_permissions(request.user,
                                                        occurrence_maincat)
            instance = models.get_occurrence_model(
                occurrence_maincat).objects.get(pk=pk)
            serializer = serializers.OccurrenceVersionSerializer()
            excude_unreleased = not (is_writer or is_publisher)
            serialized = serializer.get_version(
                instance, int(version), excude_unreleased)
            if not serialized.get('released', False) and excude_unreleased:
                return Response(
                    {
                        _("error"): _("You don't have permissions to access "
                                      "the occurrence")
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            serialized['featuretype'] = occurrence_maincat
            serialized['featuresubtype'] = instance.occurrence_cat.code
            return Response(serialized)
        except ObjectDoesNotExist:
            raise
            # raise Http404


class PhotoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, CanWriteOrUpdateAny]
    serializer_class = serializers.PhotographPublishSerializer
    parser_classes = (MultiPartParser, FormParser,)
    queryset = models.Photograph.objects.all()


class OccurrenceNaturalAreaReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.OccurrenceNaturalArea.objects.all()
    serializer_class = serializers.NaturalAreaReportSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )
    filter_class = filters.OccurrenceNaturalAreaReportFilterSet
    search_fields = (
        "element__natural_area_code_nac",
    )
    renderer_classes = (
        renderers.JSONRenderer,
        renderers.BrowsableAPIRenderer,
        pdfrenderers.OccurrenceNaturalAreaReportRenderer,
    )


class OccurrenceTaxonReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.OccurrenceTaxon.objects.all()
    serializer_class = serializers.OccurrenceTaxonReportSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    filter_backends = (
        filters.ReportTaxonFilterBackend,
        DjangoFilterBackend,
    )
    filter_class = filters.OccurrenceTaxonReportFilterSet
    renderer_classes = (
        renderers.JSONRenderer,
        renderers.BrowsableAPIRenderer,
        pdfrenderers.OccurrenceTaxonReportRenderer,
    )


class TaxonRanksViewSet(viewsets.ViewSet):
    serializer_class = serializers.TaxonRanksSerializer

    def list(self, request):
        serializer = self.serializer_class(instance=constants.TAXON_RANKS)
        return Response(serializer.data)

