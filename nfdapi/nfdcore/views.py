# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from nfdcore.models import OccurrenceTaxon, OccurrenceNaturalArea, Species,\
    OccurrenceCategory, Photograph,\
    get_occurrence_model, OccurrenceObservation
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from nfdcore.nfdserializers import FeatureTypeSerializer, LayerSerializer, OccurrenceSerializer,\
    PhotographPublishSerializer, OccurrenceVersionSerializer,\
    TaxonOccurrenceSerializer, NaturalAreaOccurrenceSerializer,\
    TaxonListSerializer, NaturalAreaListSerializer
from django.core.exceptions import ObjectDoesNotExist

import reversion
from reversion.models import Version
from nfdcore.nfdserializers import SpeciesSearchSerializer,\
    SpeciesSearchResultSerializer, SpeciesFilter
from rest_framework.generics import ListAPIView,\
    RetrieveAPIView, ListCreateAPIView
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from nfdcore.nfdserializers import delete_object_and_children
from nfdcore.permissions import CanUpdateFeatureType, get_permissions,\
    CanCreatePlants, CanCreateAnimals,\
    CanCreateNaturalAreas, CanCreateSlimeMold, CanCreateFungus,\
    CanWriteOrUpdateAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet
import django_filters
from django.db.models import Q
from rest_framework.fields import empty
import traceback

class NfdLayer(ListCreateAPIView):

    def get_queryset(self):
        (is_writer, is_publisher) = get_permissions(self.request.user, self.get_main_cat())
        queryset = self.get_base_queryset()
        is_writer_or_publisher = (is_writer or is_publisher)
        if not is_writer_or_publisher:
            queryset = queryset.filter(released=True)
        return queryset

    def get_serializer_class(self):
        return LayerSerializer

    def get_serializer(self, instance=None, data=empty, many=False, partial=False):
        #return super(NfdLayerListNew, self).get_serializer(instance=instance, data=data, many=many, partial=partial)
        (is_writer, is_publisher) = get_permissions(self.request.user, self.get_main_cat())
        if self.request.method == 'POST':
            if data is not empty:
                serializer_class = self.get_post_serializer_class()
                return serializer_class(data=data, is_writer=is_writer, is_publisher=is_publisher)
            else:
                is_writer_or_publisher = (is_writer or is_publisher)
                return LayerSerializer(data=data, many=many, is_writer_or_publisher=is_writer_or_publisher)
        else:
            is_writer_or_publisher = (is_writer or is_publisher)
            serializer_class = self.get_serializer_class()
            return serializer_class(instance, many=many, is_writer_or_publisher=is_writer_or_publisher)

    def finalize_response(self, request, response, *args, **kwargs):
        response = super(NfdLayer, self).finalize_response(request, response, *args, **kwargs)
        if response.accepted_renderer.format == 'csv':
            response['content-disposition'] = 'attachment; filename={}.csv'.format(self.get_main_cat())
        return response

class TaxonFilter(FilterSet):
    #inclusion_date = DateFromToRangeFilter() # ?inclusion_date_0=2017-10-01&inclusion_date_1=2017-10-03
    min_inclusion_date = django_filters.filters.DateFilter(name="inclusion_date", lookup_expr='gte') #?min_inclusion_date=2017-10-01
    max_inclusion_date = django_filters.filters.DateFilter(name="inclusion_date", lookup_expr='lte') #?max_inclusion_date=2017-10-03
    min_inclusion_datetime = django_filters.filters.IsoDateTimeFilter(name="inclusion_date", lookup_expr='gte') # ?min_inclusion_datetime=2017-10-02T23:05:20
    max_inclusion_datetime = django_filters.filters.IsoDateTimeFilter(name="inclusion_date", lookup_expr='lte')
    featuresubtype = django_filters.filters.CharFilter(name="occurrence_cat__code")
    class Meta:
        model = OccurrenceTaxon
        fields = ['released', 'verified', 'species']

class NaturalAreaFilter(FilterSet):
    min_inclusion_date = django_filters.filters.DateFilter(name="inclusion_date", lookup_expr='gte') #?min_inclusion_date=2017-10-01
    max_inclusion_date = django_filters.filters.DateFilter(name="inclusion_date", lookup_expr='lte') #?max_inclusion_date=2017-10-03
    min_inclusion_datetime = django_filters.filters.IsoDateTimeFilter(name="inclusion_date", lookup_expr='gte') # ?min_inclusion_datetime=2017-10-02T23:05:20
    max_inclusion_datetime = django_filters.filters.IsoDateTimeFilter(name="inclusion_date", lookup_expr='lte')
    featuresubtype = django_filters.filters.CharFilter(name="occurrence_cat__code")

    class Meta:
        model = OccurrenceNaturalArea
        fields = ['released', 'verified']

class PlantLayer(NfdLayer):
    permission_classes = [ IsAuthenticated, CanCreatePlants ]
    filter_backends = (DjangoFilterBackend,)
    filter_class = TaxonFilter

    def get_post_serializer_class(self):
        return TaxonOccurrenceSerializer

    def get_base_queryset(self):
        return OccurrenceTaxon.objects.filter(occurrence_cat__main_cat=self.get_main_cat())

    def get_main_cat(self):
        return "plant"

class AnimalLayer(NfdLayer):
    permission_classes = [ IsAuthenticated, CanCreateAnimals ]
    filter_backends = (DjangoFilterBackend,)
    filter_class = TaxonFilter

    def get_post_serializer_class(self):
        return TaxonOccurrenceSerializer

    def get_base_queryset(self):
        return OccurrenceTaxon.objects.filter(occurrence_cat__main_cat=self.get_main_cat())

    def get_main_cat(self):
        return "animal"


class FungusLayer(NfdLayer):
    permission_classes = [ IsAuthenticated, CanCreateFungus ]
    filter_backends = (DjangoFilterBackend,)
    filter_class = TaxonFilter

    def get_post_serializer_class(self):
        return TaxonOccurrenceSerializer

    def get_base_queryset(self):
        return OccurrenceTaxon.objects.filter(occurrence_cat__main_cat=self.get_main_cat())

    def get_main_cat(self):
        return "fungus"

class SlimeMoldLayer(NfdLayer):
    permission_classes = [ IsAuthenticated, CanCreateSlimeMold ]
    filter_backends = (DjangoFilterBackend,)
    filter_class = TaxonFilter

    def get_post_serializer_class(self):
        return TaxonOccurrenceSerializer

    def get_base_queryset(self):
        return OccurrenceTaxon.objects.filter(occurrence_cat__main_cat=self.get_main_cat())

    def get_main_cat(self):
        return "slimemold"

class NaturalAreaLayer(NfdLayer):
    permission_classes = [ IsAuthenticated, CanCreateNaturalAreas ]
    filter_backends = (DjangoFilterBackend,)
    filter_class = NaturalAreaFilter

    def get_post_serializer_class(self):
        return NaturalAreaOccurrenceSerializer

    def get_base_queryset(self):
        return OccurrenceNaturalArea.objects.all()

    def get_main_cat(self):
        return "naturalarea"


class NfdListPagination(PageNumberPagination):
    page_size = 10

class NfdList(ListAPIView):
    pagination_class = NfdListPagination
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        (is_writer, is_publisher) = get_permissions(self.request.user, self.get_main_cat())
        queryset = self.get_base_queryset()
        is_writer_or_publisher = (is_writer or is_publisher)
        if not is_writer_or_publisher:
            queryset = queryset.filter(released=True)
        return queryset

    def get_serializer(self, instance=None, data=empty, many=False, partial=False):
        (is_writer, is_publisher) = get_permissions(self.request.user, self.get_main_cat())
        is_writer_or_publisher = (is_writer or is_publisher)
        serializer_class = self.get_serializer_class()
        return serializer_class(instance, many=many, is_writer_or_publisher=is_writer_or_publisher)

class TaxonList(NfdList):
    filter_class = TaxonFilter
    def get_serializer_class(self):
        return TaxonListSerializer
    def get_base_queryset(self):
        return OccurrenceTaxon.objects.filter(occurrence_cat__main_cat=self.get_main_cat())

class PlantList(TaxonList):
    permission_classes = [ IsAuthenticated, CanCreatePlants ]
    def get_main_cat(self):
        return "plant"

class AnimalList(TaxonList):
    permission_classes = [ IsAuthenticated, CanCreateAnimals ]
    def get_main_cat(self):
        return "animal"


class FungusList(TaxonList):
    permission_classes = [ IsAuthenticated, CanCreateFungus ]
    def get_main_cat(self):
        return "fungus"

class SlimeMoldList(TaxonList):
    permission_classes = [ IsAuthenticated, CanCreateSlimeMold ]

    def get_main_cat(self):
        return "slimemold"

class NaturalAreaList(NfdList):
    permission_classes = [ IsAuthenticated, CanCreateNaturalAreas ]
    filter_class = NaturalAreaFilter

    def get_base_queryset(self):
        return OccurrenceNaturalArea.objects.all()

    def get_serializer_class(self):
        return NaturalAreaListSerializer

    def get_main_cat(self):
        return "naturalarea"

class LayerDetail(APIView):
    permission_classes = [ IsAuthenticated, CanUpdateFeatureType ]
    """
    Retrieve, update or delete an occurrence instance.
    """
    def get_object(self, occurrence_maincat, pk):

        try:
            return get_occurrence_model(occurrence_maincat).objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, occurrence_maincat, pk, format=None):
        (is_writer, is_publisher) = get_permissions(request.user, occurrence_maincat)
        feature = self.get_object(occurrence_maincat, pk)
        if feature.released == False and not (is_writer or is_publisher):
            return Response({_("error"): _("You don't have permissions to access the occurrence")}, status=status.HTTP_403_FORBIDDEN)
        if isinstance(feature, OccurrenceNaturalArea):
            serializer = NaturalAreaOccurrenceSerializer(feature, is_writer=is_writer, is_publisher=is_publisher)
        else:
            serializer = TaxonOccurrenceSerializer(feature, is_writer=is_writer, is_publisher=is_publisher)
        return Response(serializer.data)

    def put(self, request, occurrence_maincat, pk, format=None):
        (is_writer, is_publisher) = get_permissions(request.user, occurrence_maincat)
        feature = self.get_object(occurrence_maincat, pk)
        if isinstance(feature, OccurrenceNaturalArea):
            serializer = NaturalAreaOccurrenceSerializer(feature, data=request.data, is_writer=is_writer, is_publisher=is_publisher)
        else:
            serializer = TaxonOccurrenceSerializer(feature, data=request.data, is_writer=is_writer, is_publisher=is_publisher)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, occurrence_maincat, pk, format=None):
        feature = self.get_object(occurrence_maincat, pk)
        with reversion.create_revision():
            delete_object_and_children(feature)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LayerVersionDetail(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request, occurrence_maincat, pk, version, format=None):
        try:
            (is_writer, is_publisher) = get_permissions(request.user, occurrence_maincat)
            instance = get_occurrence_model(occurrence_maincat).objects.get(pk=pk)
            serializer = OccurrenceVersionSerializer()
            excude_unreleased = not (is_writer or is_publisher)
            serialized_feature = serializer.get_version(instance, int(version), excude_unreleased)
            if serialized_feature.get('released', False) == False and excude_unreleased:
                return Response({_("error"): _("You don't have permissions to access the occurrence")}, status=status.HTTP_403_FORBIDDEN)
            serialized_feature['featuretype'] = occurrence_maincat
            serialized_feature['featuresubtype'] = instance.occurrence_cat.code
            return Response(serialized_feature)
        except ObjectDoesNotExist:
            raise
            #raise Http404

class PhotoViewSet(ModelViewSet):
    permission_classes = [ IsAuthenticated, CanWriteOrUpdateAny ]
    serializer_class = PhotographPublishSerializer
    parser_classes = (MultiPartParser, FormParser,)
    queryset=Photograph.objects.all()

@api_view(['GET'])
def get_feature_type(request, occurrence_subcat, feature_id=None):
    if feature_id:
        if occurrence_subcat[0]=='n': # natural areas
            feat = OccurrenceNaturalArea.objects.get(pk=feature_id)
        else:
            feat = OccurrenceTaxon.objects.get(pk=feature_id)
        serializer = FeatureTypeSerializer(feat.occurrence_cat)
    else:
        # in this case we get the category code instead of the main category
        occurrence_cat = OccurrenceCategory.objects.get(code=occurrence_subcat)
        (is_writer, is_publisher) = get_permissions(request.user, occurrence_cat.main_cat)
        serializer = FeatureTypeSerializer(occurrence_cat, is_writer=is_writer, is_publisher=is_publisher)
    ftdata = serializer.get_feature_type()
    return Response(ftdata)

class SpeciesPaginationClass(PageNumberPagination):
    page_size = 100

    def get_paginated_response(self, data):
        return Response(data)

class SpeciesSearch(ListAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesSearchSerializer
    filter_backends = (SearchFilter,)
    # filter_class = SpeciesFilter
    pagination_class = SpeciesPaginationClass
    search_fields = ('first_common', 'name_sci', 'second_common', 'third_common', 'synonym')

    def get_queryset(self):
        queryset = Species.objects.all()

        request = self.request
        if request and request.query_params:
            try:
                search_params = request.query_params.getlist('search')
                for filter_param in search_params:
                    queryset = queryset.filter(
                        Q(first_common__icontains=filter_param) |
                        Q(second_common__icontains=filter_param) |
                        Q(third_common__icontains=filter_param) |
                        Q(name_sci__icontains=filter_param) |
                        Q(synonym__icontains=filter_param) |
                        # startswith
                        Q(first_common__startswith=filter_param) |
                        Q(second_common__startswith=filter_param) |
                        Q(third_common__startswith=filter_param) |
                        Q(name_sci__startswith=filter_param) |
                        Q(synonym__startswith=filter_param) |
                        # endswith
                        Q(first_common__endswith=filter_param) |
                        Q(second_common__endswith=filter_param) |
                        Q(third_common__endswith=filter_param) |
                        Q(name_sci__endswith=filter_param) |
                        Q(synonym__endswith=filter_param)
                        )
            except:
                traceback.print_exc()

        return queryset.order_by('first_common')

class SpeciesDetail(RetrieveAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesSearchResultSerializer
    search_fields = ('first_common', 'name_sci', 'second_common', 'third_common', 'synonym')

    def get_queryset(self):
        queryset = Species.objects.all()

        request = self.request
        if request and request.query_params:
            try:
                search_params = request.query_params.getlist('search')
                for filter_param in search_params:
                    queryset = queryset.filter(
                        Q(first_common__icontains=filter_param) |
                        Q(second_common__icontains=filter_param) |
                        Q(third_common__icontains=filter_param) |
                        Q(name_sci__icontains=filter_param) |
                        Q(synonym__icontains=filter_param) |
                        # startswith
                        Q(first_common__startswith=filter_param) |
                        Q(second_common__startswith=filter_param) |
                        Q(third_common__startswith=filter_param) |
                        Q(name_sci__startswith=filter_param) |
                        Q(synonym__startswith=filter_param) |
                        # endswith
                        Q(first_common__endswith=filter_param) |
                        Q(second_common__endswith=filter_param) |
                        Q(third_common__endswith=filter_param) |
                        Q(name_sci__endswith=filter_param) |
                        Q(synonym__endswith=filter_param)
                        )
            except:
                traceback.print_exc()

        return queryset.order_by('first_common')
