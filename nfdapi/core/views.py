# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.models import OccurrenceTaxon, OccurrenceNaturalArea, Species,\
    OccurrenceCategory, DictionaryTable, DictionaryTableExtended
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from core.nfdserializers import FeatureTypeSerializer, CreateOccurrenceSerializer, LayerTaxonSerializer, OccurrenceSerializer
from django.core.exceptions import ObjectDoesNotExist

import reversion
from reversion.models import Version
from core.nfdserializers import TaxonDetailsSerializer, SpeciesSearchSerializer,\
    SpeciesSearchResultSerializer, SpeciesSerializer
from rest_framework.generics import ListCreateAPIView, ListAPIView,\
    RetrieveAPIView
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.fields import ModelField
from core.nfdserializers import delete_object_and_children

@api_view(['GET'])
@permission_classes([])
def test_url(request):
    occurrences = OccurrenceTaxon.objects.all()
    if len(occurrences) > 0:
        la = occurrences[len(occurrences)-1]
        serializer = TaxonDetailsSerializer(la)
        return Response(serializer.data)
    else:
        return Response({"error": "no OccurrenceTaxon available"})    

@api_view(['GET'])
@permission_classes([])
def test_url2(request):
    occurrences = OccurrenceTaxon.objects.all()
    if len(occurrences) > 0:
        la = occurrences[len(occurrences)-1]
        serializer = TaxonDetailsSerializer(la)
        
        serializer2 = TaxonDetailsSerializer(la, data=serializer.data)
        serializer2.is_valid()
        serializer2.save()
        
        serializer = TaxonDetailsSerializer(la)
        return Response(serializer.data)
        #return Response(serializer2.validated_data)
    else:
        return Response({"error": "no OccurrenceTaxon available"})   


@api_view(['GET'])
@permission_classes([])
def test_url3(request):
    occurrences = OccurrenceTaxon.objects.all()
    if len(occurrences) > 0:
        la = occurrences[len(occurrences)-1]
        versions = Version.objects.get_for_object(la)
        if len(versions)>1:
            la_old = versions[1]
            serializer = TaxonDetailsSerializer(la_old.field_dict)
            return Response(serializer.data)
    
    return Response({"error": "no old versions available"})


class TaxonLayerList(APIView):
    permission_classes = [] #FIXME when authentication is implemented
    def get(self, request, main_cat, format=None):
        queryset = OccurrenceTaxon.objects.filter(occurrence_cat__main_cat=main_cat)
        serializer = LayerTaxonSerializer(queryset, many=True)
        return Response(serializer.data)
    def post(self, request, main_cat, format=None):
        serializer = OccurrenceSerializer(data=request.data)
        #serializer = CreateOccurrenceSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NaturalAreaLayerList(APIView):
    permission_classes = [] #FIXME when authentication is implemented
    def get(self, request, format=None):
        queryset = OccurrenceNaturalArea.objects.all()
        serializer = LayerTaxonSerializer(queryset, many=True) #FIXME: should be using a different serializer
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = CreateOccurrenceSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LayerDetail(APIView):
    permission_classes = [] #FIXME when authentication is implemented
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, occurrence_maincat, pk):
        try:
            if occurrence_maincat[0]=='n': # natural areas
                return OccurrenceNaturalArea.objects.get(pk=pk)
            else:
                return OccurrenceTaxon.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, occurrence_maincat, pk, format=None):
        feature = self.get_object(occurrence_maincat, pk)
        if isinstance(feature, OccurrenceNaturalArea):
            return Response({"error": "not supported yet"})
        else:
            serializer = OccurrenceSerializer(feature)
            #serializer = TaxonDetailsSerializer(feature)
        return Response(serializer.data)

    def put(self, request, occurrence_maincat, pk, format=None):
        feature = self.get_object(occurrence_maincat, pk)
        if isinstance(feature, OccurrenceNaturalArea):
            return Response({"error": "not supported yet"})
        else:
            serializer = OccurrenceSerializer(feature, data=request.data)
            #serializer = TaxonDetailsSerializer(feature, data=request.data)         
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, occurrence_maincat, pk, format=None):
        feature = self.get_object(occurrence_maincat, pk)
        with reversion.create_revision():
            delete_object_and_children(feature)
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
@permission_classes([])
def get_feature_type(request, occurrence_maincat, feature_id=None):
    if feature_id:
        if occurrence_maincat[0]=='n': # natural areas
            feat = OccurrenceNaturalArea.objects.get(pk=feature_id)
        else:
            feat = OccurrenceTaxon.objects.get(pk=feature_id)
        serializer = FeatureTypeSerializer(feat.occurrence_cat)
    else:
        # in this case we get the category code instead of the main category
        occurrence_cat = OccurrenceCategory.objects.get(code=occurrence_maincat)
        serializer = FeatureTypeSerializer(occurrence_cat)
    ftdata = serializer.get_feature_type()
    return Response(ftdata)

class SpeciesPaginationClass(PageNumberPagination):
    page_size = 15
    
    def get_paginated_response(self, data):
        return Response(data)
    
@permission_classes([])
class SpeciesSearch(ListAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesSearchSerializer
    filter_backends = (SearchFilter,)
    pagination_class = SpeciesPaginationClass
    search_fields = ('first_common', 'name_sci', 'second_common', 'third_common', 'synonym')

@permission_classes([])
class SpeciesDetail(RetrieveAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesSearchResultSerializer
    search_fields = ('first_common', 'name_sci', 'second_common', 'third_common', 'synonym')

"""
class TaxonFeatureTypeView(APIView):
    permission_classes = ()
    
    #Retrieve, update or delete a snippet instance.
    
    def get_object(self, pk):
        try:
            return OccurrenceTaxon.objects.get(pk=pk)
        except OccurrenceTaxon.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = FeatureTypeSerializer(obj)
        return Response(serializer.data)
"""

"""
# ORIGIN ELEMENT TYPES
 element_natural_areas
 
 element_taxon
 element_species
 element_fungus_or_ally
 element_slime_mold # moho
 
 
 element_amphibian
 element_arachnid , 
 element_bird
 element_crustacean (subfilo), filo Arthropoda, reino Animalia
 element_fish (clasific. informal), filo Chordata, reino Animalia
 element_flatworm
 element_insect (clase Insecta), subfilo Hexapoda, Filo  Arthropoda, reino Animalia
 element_mammal (clase Mammalia), Sufilo Vertebrata, filo Chordata, reino Animalia
 element_mollusk (filo Mollusca), reino Animalia. Acuáticos y terrestres (e.g. pulpos y caracoles)
 element_myriapod
 element_reptile
 element_roundworm
 element_segmented_worm
 element_sessile_animal
 
 element_alga
 element_conifer_or_ally
 element_fern_or_ally # helechos
 element_forb # plantas herbáceas no gramináceas
 element_grass
 element_moss_or_ally # musgo
 element_sedge_or_rush # juncos
 element_shrub_or_tree
 
 

# POR ORDEN EN LA DB
 element_natural_areas
 element_species
 element_alga
 element_amphibian
 element_arachnid
 element_bird
 element_conifer_or_ally
 element_crustacean
 element_fern_or_ally
 element_fish
 element_flatworm
 element_forb
 element_fungus_or_ally
 element_grass
 element_insect
 element_mammal
 element_mollusk
 element_moss_or_ally
 element_myriapod
 element_reptile
 element_roundworm
 element_sedge_or_rush
 element_segmented_worm
 element_sessile_animal
 element_shrub_or_tree
 element_slime_mold
 element_taxon

"""
