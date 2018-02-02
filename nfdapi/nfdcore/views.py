# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import namedtuple
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Count
from django.db.models.fields import DateField
from django.db.models.functions import TruncMonth
from django.http import Http404
import django_filters
from django_filters import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import list_route
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.fields import empty
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import ModelViewSet
import reversion

from nfdrenderers import pdf as pdfrenderers

from . import models
from .models import (
    get_occurrence_model,
    OccurrenceCategory,
    OccurrenceNaturalArea,
    OccurrenceTaxon,
    Photograph,
    Species,
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


class TaxonomyFilterer(object):
    """Prepares aggregation querysets"""

    @property
    def aggregate_by(self):
        return self._aggregate_by

    @property
    def aggregation_params(self):
        return self._aggregation_params

    def __init__(self, year=None, released=None,
                 daytime=None, season=None, location=None,
                 reporter=None, category=None, subcategory=None, phylum=None,
                 family=None, species=None, aggregate_by=None,
                 split_by_month=False, include_subcategories=False):
        geom_location = self._get_geom(location) if location else None
        year = int(year) if year is not None else None
        self.filter_attributes = [
            FilterField("year", year,
                        "observation__observation_date__year"),
            FilterField("released", bool(released),
                        "released"),
            FilterField("daytime", daytime,
                        "observation__daytime__name"),
            FilterField("season", season,
                        "observation__season__name"),
            FilterField("location", geom_location,
                        "geom__contained"),
            FilterField("reporter", reporter,
                        ""),
            FilterField("category", category,
                        "occurrence_cat__main_cat"),
            FilterField("subcategory", subcategory,
                        "occurrence_cat__name"),
            FilterField("phylum", phylum,
                        "species__phylum"),
            FilterField("family", family,
                        "species__family"),
            FilterField("species", species,
                        "species__name_sci"),
        ]
        self.split_by_month = split_by_month
        self.include_subcategories = include_subcategories
        self._aggregate_by = aggregate_by
        self._aggregation_params = self._get_aggregation_parameters()

    @classmethod
    def from_query_params(cls, query_params):
        return cls(
            year=query_params.get("year"),
            released=query_params.get("released"),
            daytime=query_params.get("daytime"),
            season=query_params.get("season"),
            location=query_params.get("location"),
            reporter=query_params.get("reporter"),
            category=query_params.get("category"),
            subcategory=query_params.get("subcategory"),
            phylum=query_params.get("phylum"),
            family=query_params.get("family"),
            species=query_params.get("species"),
            aggregate_by=query_params.get("aggregate_by", "species"),
            split_by_month=query_params.get("split_by_month"),
            include_subcategories=query_params.get(
                "include_subcategories", False),
        )

    def get_filter_queryset(self):
        qs = models.OccurrenceTaxon.objects.all()
        for field in self.filter_attributes:
            if field.value is not None:
                qs = qs.filter(**{field.lookup: field.value})
        return qs

    def get_field_by_name(self, name):
        try:
            result = [f for f in self.filter_attributes if f.name == name][0]
        except KeyError:
            result = None
        return result

    def get_field_by_lookup(self, lookup):
        try:
            result = [f for f in self.filter_attributes if f.lookup == lookup][0]
        except KeyError:
            result = None
        return result

    def get_aggregation_queryset(self, qs, count_greater_than=0):
        aggregation_atributes = self.aggregation_params[:]
        if self.split_by_month is not None:
            annotate_kwargs = {
                "month": TruncMonth(
                    "observation__observation_date",
                    output_field=DateField()
                )
            }
            qs = qs.annotate(**annotate_kwargs)
            aggregation_atributes.append("month")
        qs = qs.values(*aggregation_atributes).annotate(
            num_occurrences=Count("id")
        ).filter(num_occurrences__gt=count_greater_than)
        return qs

    def _get_geom(self, wkt=None, srid=4326):
        # TODO: check for valid geometry type (POLYGON)
        # TODO: check for valid geometry
        return GEOSGeometry(wkt, srid=4326)

    def _get_aggregation_parameters(self):
        if self.aggregate_by == "category":
            parameters = [
                "occurrence_cat__main_cat",
            ]
        elif self.aggregate_by == "phylum":
            parameters = [
                "occurrence_cat__main_cat",
                "species__phylum",
            ]
        elif self.aggregate_by == "family":
            parameters = [
                "occurrence_cat__main_cat",
                "species__phylum",
                "species__family",
            ]
        else:
            parameters = [
                "occurrence_cat__main_cat",
                "species__phylum",
                "species__family",
                "species__name_sci",
            ]
        if self.include_subcategories and self.aggregate_by != "category":
            parameters.append("occurrence_cat__name")
        return parameters


class OccurrenceAggregatorViewSet(viewsets.ViewSet):
    """ViewSet for occurrence stats"""

    renderer_classes = (
        JSONRenderer,
        BrowsableAPIRenderer,
        pdfrenderers.PdfOccurrenceStatsRenderer,
    )
    serializer_class = nfdserializers.OccurrenceAggregatorSerializer

    def list(self, request):
        filterer = TaxonomyFilterer.from_query_params(request.query_params)
        filter_qs = filterer.get_filter_queryset()
        aggregation_qs = filterer.get_aggregation_queryset(filter_qs)
        serializer = self.serializer_class(
            aggregation_qs,
            context={"filterer": filterer}
        )
        return Response(serializer.data)

    @list_route(methods=["get",])
    def animal(self, request):
        return self._aggregate_by_category(
            request.query_params.dict(),
            "animal",
            title="Animals"
        )

    @list_route(methods=["get",])
    def land_animal(self, request):
        return self._aggregate_by_category(
            request.query_params.dict(),
            "animal",
            subcategory="Land animal",
            title="Land Animals"
        )

    @list_route(methods=["get",])
    def plant(self, request):
        return self._aggregate_by_category(
            request.query_params.dict(),
            "plant",
            title="Plants"
        )

    @list_route(methods=["get",])
    def fungus(self, request):
        return self._aggregate_by_category(
            request.query_params.dict(),
            "fungus",
            title="Fungi"
        )

    @list_route(methods=["get",])
    def slime_mold(self, request):
        return self._aggregate_by_category(
            request.query_params.dict(),
            "slimemold",
            title="Slime Molds"
        )

    def _aggregate_by_category(self, query_params, category, subcategory=None,
                               title=""):
        query_params["category"] = category
        if subcategory is not None:
            query_params["subcategory"] = subcategory
        filterer = TaxonomyFilterer.from_query_params(query_params)
        filter_qs = filterer.get_filter_queryset()
        aggregation_qs = filterer.get_aggregation_queryset(filter_qs)
        serializer = self.serializer_class(
            aggregation_qs,
            context={
                "filterer": filterer,
                "title": title,
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
                return serializer_class(data=data, is_writer=is_writer,
                                        is_publisher=is_publisher)
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
    # ?inclusion_date_0=2017-10-01&inclusion_date_1=2017-10-03
    # inclusion_date = DateFromToRangeFilter()
    min_inclusion_date = django_filters.filters.DateFilter(
        name="inclusion_date",
        lookup_expr='gte'
    )  # ?min_inclusion_date=2017-10-01
    max_inclusion_date = django_filters.filters.DateFilter(
        name="inclusion_date",
        lookup_expr='lte'
    )  # ?max_inclusion_date=2017-10-03
    min_inclusion_datetime = django_filters.filters.IsoDateTimeFilter(
        name="inclusion_date",
        lookup_expr='gte'
    )  # ?min_inclusion_datetime=2017-10-02T23:05:20
    max_inclusion_datetime = django_filters.filters.IsoDateTimeFilter(
        name="inclusion_date",
        lookup_expr='lte'
    )
    featuresubtype = django_filters.filters.CharFilter(
        name="occurrence_cat__code")

    class Meta:
        model = OccurrenceTaxon
        fields = ['released', 'verified', 'species']


class NaturalAreaFilter(FilterSet):
    min_inclusion_date = django_filters.filters.DateFilter(
        name="inclusion_date",
        lookup_expr='gte'
    )  # ?min_inclusion_date=2017-10-01
    max_inclusion_date = django_filters.filters.DateFilter(
        name="inclusion_date",
        lookup_expr='lte'
    )  # ?max_inclusion_date=2017-10-03
    min_inclusion_datetime = django_filters.filters.IsoDateTimeFilter(
        name="inclusion_date",
        lookup_expr='gte'
    )  # ?min_inclusion_datetime=2017-10-02T23:05:20
    max_inclusion_datetime = django_filters.filters.IsoDateTimeFilter(
        name="inclusion_date",
        lookup_expr='lte'
    )
    featuresubtype = django_filters.filters.CharFilter(
        name="occurrence_cat__code")

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


class TaxonList(NfdList):
    filter_class = TaxonFilter

    def get_serializer_class(self):
        return nfdserializers.TaxonListSerializer

    def get_base_queryset(self):
        return OccurrenceTaxon.objects.filter(
            occurrence_cat__main_cat=self.get_main_cat())


class PlantList(TaxonList):
    permission_classes = [IsAuthenticated, CanCreatePlants]

    def get_main_cat(self):
        return "plant"


class AnimalList(TaxonList):
    # permission_classes = [IsAuthenticated, CanCreateAnimals]

    def get_main_cat(self):
        return "animal"


class FungusList(TaxonList):
    permission_classes = [IsAuthenticated, CanCreateFungus]

    def get_main_cat(self):
        return "fungus"


class SlimeMoldList(TaxonList):
    permission_classes = [IsAuthenticated, CanCreateSlimeMold]

    def get_main_cat(self):
        return "slimemold"


class NaturalAreaList(NfdList):
    permission_classes = [IsAuthenticated, CanCreateNaturalAreas]
    filter_class = NaturalAreaFilter

    def get_base_queryset(self):
        return OccurrenceNaturalArea.objects.all()

    def get_serializer_class(self):
        return nfdserializers.NaturalAreaListSerializer

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
        (is_writer, is_publisher) = get_permissions(request.user,
                                                    occurrence_maincat)
        feature = self.get_object(occurrence_maincat, pk)
        if isinstance(feature, OccurrenceNaturalArea):
            serializer = nfdserializers.NaturalAreaOccurrenceSerializer(
                feature, data=request.data, is_writer=is_writer,
                is_publisher=is_publisher
            )
        else:
            serializer = nfdserializers.TaxonOccurrenceSerializer(
                feature, data=request.data, is_writer=is_writer,
                is_publisher=is_publisher
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


@api_view(['GET'])
def get_feature_type(request, occurrence_subcat, feature_id=None):
    if feature_id:
        if occurrence_subcat[0] == 'n':  # natural areas
            feat = OccurrenceNaturalArea.objects.get(pk=feature_id)
        else:
            feat = OccurrenceTaxon.objects.get(pk=feature_id)
        serializer = nfdserializers.FeatureTypeSerializer(feat.occurrence_cat)
    else:
        # in this case we get the category code instead of the main category
        occurrence_cat = OccurrenceCategory.objects.get(code=occurrence_subcat)
        (is_writer, is_publisher) = get_permissions(request.user,
                                                    occurrence_cat.main_cat)
        serializer = nfdserializers.FeatureTypeSerializer(
            occurrence_cat,
            is_writer=is_writer,
            is_publisher=is_publisher
        )
    ftdata = serializer.get_feature_type()
    return Response(ftdata)


class SpeciesPaginationClass(PageNumberPagination):
    page_size = 15

    def get_paginated_response(self, data):
        return Response(data)


class SpeciesSearch(ListAPIView):
    queryset = Species.objects.all()
    serializer_class = nfdserializers.SpeciesSearchSerializer
    filter_backends = (SearchFilter,)
    pagination_class = SpeciesPaginationClass
    search_fields = (
        'first_common',
        'name_sci',
        'second_common',
        'third_common',
        'synonym',
    )


class SpeciesDetail(RetrieveAPIView):
    queryset = Species.objects.all()
    serializer_class = nfdserializers.SpeciesSearchResultSerializer
    search_fields = (
        'first_common',
        'name_sci',
        'second_common',
        'third_common',
        'synonym',
    )
