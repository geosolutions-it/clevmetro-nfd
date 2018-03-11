# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import namedtuple
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.http import Http404
import django_filters
from django_filters import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework import filters
from rest_framework.decorators import list_route
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.fields import empty
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ModelViewSet
import reversion

from nfdrenderers import pdf as pdfrenderers
from nfdrenderers import csv as csvrenderers
from nfdrenderers import xlsx as xlsrenderers
from nfdrenderers import shp as shprenderers

from . import itis
from . import models
from .models import (
    get_occurrence_model,
    OccurrenceNaturalArea,
    OccurrenceTaxon,
    Photograph,
)
from . import nfdserializers
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
        JSONRenderer,
        BrowsableAPIRenderer,
    )
    serializer_class = nfdserializers.FormDefinitionsSerializer

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
        JSONRenderer,
        BrowsableAPIRenderer,
    )

    def get_serializer_class(self):
        if self.action == "list":
            result = nfdserializers.ItisTaxonSearchSerializer
        elif self.action == "retrieve":
            result = nfdserializers.ItisTaxonHierarchySerializer
        else:
            raise RuntimeError("Invalid action")
        return result

    def list(self, request):
        """Search for taxa on the ITIS database"""
        feature_types = request.query_params.get("featuretypes","").split(",")
        if not any(feature_types):
            feature_types = models.OccurrenceCategory.objects.values_list(
                "main_cat", flat=True).distinct()
        kingdoms = _get_kingdoms(feature_types)
        search_results = itis.search_taxon(
            request.query_params.get("search", ""),
            kingdoms,
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
                serializer_class = nfdserializers.TaxonDetailSerializer
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
        JSONRenderer,
        BrowsableAPIRenderer,
    )
    filter_backends = (
        filters.SearchFilter,
    )
    search_fields = (
        "name",
        "upper_ranks",
    )

    queryset = models.Taxon.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            result = nfdserializers.TaxonListSerializer
        elif self.action == "retrieve":
            result = nfdserializers.TaxonDetailSerializer
        else:
            raise RuntimeError("Invalid action")
        return result


class OccurrenceAggregatorViewSet(viewsets.ViewSet):
    """ViewSet for occurrence stats"""

    renderer_classes = (
        JSONRenderer,
        BrowsableAPIRenderer,
        pdfrenderers.PdfOccurrenceStatsRenderer,
    )
    serializer_class = nfdserializers.OccurrenceAggregatorSerializer

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


class NfdLayer(ListCreateAPIView):

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
        return nfdserializers.LayerSerializer

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
                return nfdserializers.LayerSerializer(
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


class TaxonFilter(FilterSet):
    featuresubtype = django_filters.filters.CharFilter(
        name="occurrence_cat__code"
    )
    taxon = django_filters.filters.CharFilter(
        name="taxon__upper_ranks",
        lookup_expr="icontains"
    )
    reservation = django_filters.filters.CharFilter(
        name="location__reservation",
        lookup_expr="icontains",
    )
    watershed = django_filters.filters.CharFilter(
        name="location__watershed",
        lookup_expr="icontains",
    )
    cm_status = django_filters.filters.ModelChoiceFilter(
        name="taxon__cm_status__code",
        queryset=models.CmStatus.objects.all()
    )

    class Meta:
        model = OccurrenceTaxon
        fields = ['location', 'released', 'verified', 'taxon']


class NaturalAreaFilter(FilterSet):
    featuresubtype = django_filters.filters.CharFilter(
        name="occurrence_cat__code")
    cm_status = django_filters.filters.ModelChoiceFilter(
        name="element__cm_status__code",
        queryset=models.CmStatus.objects.all()
    )

    class Meta:
        model = OccurrenceNaturalArea
        fields = ['released', 'verified']


class PlantLayer(NfdLayer):
    permission_classes = [IsAuthenticated, CanCreatePlants]
    filter_backends = (DjangoFilterBackend, )
    filter_class = TaxonFilter

    def get_post_serializer_class(self):
        return nfdserializers.TaxonOccurrenceSerializer

    def get_base_queryset(self):
        return OccurrenceTaxon.objects.filter(
            occurrence_cat__main_cat=self.get_main_cat())

    def get_main_cat(self):
        return "plant"


class AnimalLayer(NfdLayer):
    permission_classes = [IsAuthenticated, CanCreateAnimals]
    filter_backends = (DjangoFilterBackend, )
    filter_class = TaxonFilter

    def get_post_serializer_class(self):
        return nfdserializers.TaxonOccurrenceSerializer

    def get_base_queryset(self):
        return OccurrenceTaxon.objects.filter(
            occurrence_cat__main_cat=self.get_main_cat())

    def get_main_cat(self):
        return "animal"


class FungusLayer(NfdLayer):
    permission_classes = [IsAuthenticated, CanCreateFungus]
    filter_backends = (DjangoFilterBackend, )
    filter_class = TaxonFilter

    def get_post_serializer_class(self):
        return nfdserializers.TaxonOccurrenceSerializer

    def get_base_queryset(self):
        return OccurrenceTaxon.objects.filter(
            occurrence_cat__main_cat=self.get_main_cat())

    def get_main_cat(self):
        return "fungus"


class SlimeMoldLayer(NfdLayer):
    permission_classes = [IsAuthenticated, CanCreateSlimeMold]
    filter_backends = (DjangoFilterBackend, )
    filter_class = TaxonFilter

    def get_post_serializer_class(self):
        return nfdserializers.TaxonOccurrenceSerializer

    def get_base_queryset(self):
        return OccurrenceTaxon.objects.filter(
            occurrence_cat__main_cat=self.get_main_cat())

    def get_main_cat(self):
        return "slimemold"


class NaturalAreaLayer(NfdLayer):
    permission_classes = [IsAuthenticated, CanCreateNaturalAreas]
    filter_backends = (DjangoFilterBackend, )
    filter_class = NaturalAreaFilter

    def get_post_serializer_class(self):
        return nfdserializers.NaturalAreaOccurrenceSerializer

    def get_base_queryset(self):
        return OccurrenceNaturalArea.objects.all()

    def get_main_cat(self):
        return "naturalarea"


class NfdListPagination(PageNumberPagination):
    page_size = 10


class NfdList(ListAPIView):
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
    filter_class = TaxonFilter

    def get_serializer_class(self):
        return nfdserializers.TaxonOccurrenceListSerializer

    def get_base_queryset(self):
        return OccurrenceTaxon.objects.filter(
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
    filter_class = NaturalAreaFilter

    def get_base_queryset(self):
        return OccurrenceNaturalArea.objects.all()

    def get_serializer_class(self):
        return nfdserializers.NaturalAreaOccurrenceListSerializer

    def get_main_cat(self):
        return "naturalarea"


class LayerDetail(APIView):
    """
    Retrieve, update or delete an occurrence instance.
    """
    permission_classes = [IsAuthenticated, CanUpdateFeatureType]
    renderer_classes = (
        JSONRenderer,
        BrowsableAPIRenderer,
        pdfrenderers.PdfLayerDetailRenderer,
        csvrenderers.CsvRenderer,
        xlsrenderers.XlsxRenderer,
        shprenderers.ShpRenderer,
    )

    def get_object(self, occurrence_maincat, pk):
        try:
            return get_occurrence_model(occurrence_maincat).objects.get(pk=pk)
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
        if isinstance(feature, OccurrenceNaturalArea):
            serializer = nfdserializers.NaturalAreaOccurrenceSerializer(
                feature, is_writer=is_writer, is_publisher=is_publisher)
        else:
            serializer = nfdserializers.TaxonOccurrenceSerializer(
                feature, is_writer=is_writer, is_publisher=is_publisher)
        return Response(serializer.data)

    def put(self, request, occurrence_maincat, pk, format=None):
        is_writer, is_publisher = get_permissions(
            request.user, occurrence_maincat)
        feature = self.get_object(occurrence_maincat, pk)
        if isinstance(feature, OccurrenceNaturalArea):
            serializer = nfdserializers.NaturalAreaOccurrenceSerializer(
                feature, data=request.data, is_writer=is_writer,
                is_publisher=is_publisher
            )
        else:
            request_data = request.data.copy()
            tsn = request_data.pop("taxon.tsn")
            serializer = nfdserializers.TaxonOccurrenceSerializer(
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
            nfdserializers.delete_object_and_children(feature)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LayerVersionDetail(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, occurrence_maincat, pk, version, format=None):
        try:
            (is_writer, is_publisher) = get_permissions(request.user,
                                                        occurrence_maincat)
            instance = get_occurrence_model(
                occurrence_maincat).objects.get(pk=pk)
            serializer = nfdserializers.OccurrenceVersionSerializer()
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


class PhotoViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, CanWriteOrUpdateAny]
    serializer_class = nfdserializers.PhotographPublishSerializer
    parser_classes = (MultiPartParser, FormParser,)
    queryset = Photograph.objects.all()


def _get_kingdoms(feature_types):
    """Map between feature types and ITIS kingdoms"""
    feature_type_to_kingdom = {
        "animal": "Animalia",
        "fungus": "Fungi",
        "plant": "Plantae",
        "slimemold": "Fungi",
    }
    kingdoms = []
    for feature_type in feature_types:
        kingdom = feature_type_to_kingdom.get(feature_type)
        if kingdom is not None:
            kingdoms.append(kingdom)
    return kingdoms


