# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from nfdcore.models import OccurrenceTaxon, OccurrenceNaturalArea, Species,\
    OccurrenceCategory, Photograph,\
    get_occurrence_model
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from nfdcore.nfdserializers import FeatureTypeSerializer, LayerTaxonSerializer, OccurrenceSerializer,\
    PhotographPublishSerializer
from django.core.exceptions import ObjectDoesNotExist

import reversion
from reversion.models import Version
from nfdcore.nfdserializers import SpeciesSearchSerializer,\
    SpeciesSearchResultSerializer
from rest_framework.generics import ListAPIView,\
    RetrieveAPIView
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from nfdcore.nfdserializers import delete_object_and_children
from nfdcore.permissions import CanUpdateFeatureType, get_permissions,\
    CanCreateFeatureType
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet

class NfdLayerList(APIView):
    permission_classes = [ IsAuthenticated, CanCreateFeatureType ]
    
    def get(self, request, main_cat, format=None):
        (is_writer, is_publisher) = get_permissions(request.user, main_cat)    
        queryset = self.get_base_queryset(main_cat)
        if not (is_writer or is_publisher):
            queryset = queryset.filter(released=True)
        serializer = self.get_list_serializer(queryset)
        return Response(serializer.data)
    def post(self, request, main_cat, format=None):
        (is_writer, is_publisher) = get_permissions(request.user, main_cat)
        serializer = OccurrenceSerializer(data=request.data, is_writer=is_writer, is_publisher=is_publisher)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaxonLayerList(NfdLayerList):
    def get_base_queryset(self, main_cat):
        return OccurrenceTaxon.objects.filter(occurrence_cat__main_cat=main_cat)
    
    def get_list_serializer(self, queryset):
        return LayerTaxonSerializer(queryset, many=True)

class NaturalAreaLayerList(NfdLayerList):
    def get_base_queryset(self, main_cat):
        return OccurrenceNaturalArea.objects.all()
    
    def get_list_serializer(self, queryset):
        return LayerTaxonSerializer(queryset, many=True) #FIXME: should be using a different serializer

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
            return Response({"error": "not supported yet"})
        else:
            serializer = OccurrenceSerializer(feature, is_writer=is_writer, is_publisher=is_publisher)
        return Response(serializer.data)

    def put(self, request, occurrence_maincat, pk, format=None):
        (is_writer, is_publisher) = get_permissions(request.user, occurrence_maincat)    
        feature = self.get_object(occurrence_maincat, pk)
        if isinstance(feature, OccurrenceNaturalArea):
            return Response({"error": "not supported yet"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = OccurrenceSerializer(feature, data=request.data, is_writer=is_writer, is_publisher=is_publisher)         
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, occurrence_maincat, pk, format=None):
        feature = self.get_object(occurrence_maincat, pk)
        with reversion.create_revision():
            delete_object_and_children(feature)
        return Response(status=status.HTTP_204_NO_CONTENT)

class PhotoViewSet(ModelViewSet):
    serializer_class = PhotographPublishSerializer
    parser_classes = (MultiPartParser, FormParser,)
    queryset=Photograph.objects.all()
    
    def pre_save(self, obj):
        print "hola"
        pass
        #self.request

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
    page_size = 15
    
    def get_paginated_response(self, data):
        return Response(data)

class SpeciesSearch(ListAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesSearchSerializer
    filter_backends = (SearchFilter,)
    pagination_class = SpeciesPaginationClass
    search_fields = ('first_common', 'name_sci', 'second_common', 'third_common', 'synonym')


class SpeciesDetail(RetrieveAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesSearchResultSerializer
    search_fields = ('first_common', 'name_sci', 'second_common', 'third_common', 'synonym')
