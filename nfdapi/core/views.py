# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import datetime
from rest_framework.serializers import Serializer
from rest_framework import serializers
from core.models import OccurrenceTaxon, Occurrence, OccurrenceNaturalArea
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from django.template.context_processors import request
from featuretype import FeatureTypeSerializer, FeatureInfoSerializer, CreateOccurrenceSerializer, LayerTaxonSerializer
from django.core.exceptions import ObjectDoesNotExist

import reversion
from reversion.models import Version
from core.featuretype import TaxonDetailsSerializer
from rest_framework.generics import ListCreateAPIView

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

# Create your views here.
def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


#class TaxonLayerList(ListCreateAPIView):
class TaxonLayerList(APIView):
    permission_classes = [] #FIXME when authentication is implemented
    def get(self, request, format=None):
        queryset = OccurrenceTaxon.objects.filter(occurrence_cat__main_cat='animal')
        serializer = LayerTaxonSerializer(queryset, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = CreateOccurrenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NaturalAreaLayerList(APIView):
    permission_classes = [] #FIXME when authentication is implemented
    def get(self, request, format=None):
        queryset = OccurrenceNaturalArea.objects.all()
        serializer = LayerTaxonSerializer(queryset, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = CreateOccurrenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
            serializer = TaxonDetailsSerializer(feature)
        return Response(serializer.data)

    def put(self, request, occurrence_maincat, pk, format=None):
        feature = self.get_object(occurrence_maincat, pk)
        if isinstance(feature, OccurrenceNaturalArea):
            return Response({"error": "not supported yet"})
        else:
            serializer = TaxonDetailsSerializer(feature, data=request.data)         
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, occurrence_maincat, pk, format=None):
        feature = self.get_object(occurrence_maincat, pk)
        with reversion.create_revision():
            feature.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class DictionarySerializer(Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    
    def __init__(self, instance=None, data=None, **kwargs):
        super(DictionarySerializer, self).__init__(**kwargs)

"""
class LayerTaxonSerializer(Serializer):
    occurrence_cat = DictionarySerializer(required=False)
    
    def __init__(self, instance=None, data=None, **kwargs):
        super(LayerTaxonSerializer, self).__init__(**kwargs)
"""

"""
@api_view(['GET', 'POST', 'HEAD'])
@permission_classes([])
class PlantLayerView(LayerList):
    model = OccurrenceTaxon
    
    def get_queryset(self):
        return OccurrenceTaxon.objects.filter(occurrence_cat__main_cat='plant')

@api_view(['GET', 'POST', 'HEAD'])
@permission_classes([])
class AnimalLayerView(LayerList):
    def get_queryset(self):
        return OccurrenceTaxon.objects.filter(occurrence_cat__main_cat='animal')

@api_view(['GET', 'POST', 'HEAD'])
@permission_classes([])
class SlimeMoldLayerView(LayerList):
    def get_queryset(self):
        return OccurrenceTaxon.objects.filter(occurrence_cat__main_cat='slime mold')

@api_view(['GET', 'POST', 'HEAD'])
@permission_classes([])
class FungusLayerView(LayerList):
    def get_queryset(self):
        return OccurrenceTaxon.objects.filter(occurrence_cat__main_cat='fungus')

@api_view(['GET', 'POST', 'HEAD'])
@permission_classes([])
class NaturalAreaLayerView(LayerList):
    def get_queryset(self):
        return OccurrenceTaxon.objects.filter(occurrence_cat__main_cat='natural area')
"""

@api_view(['GET'])
@permission_classes([])
def get_feature_type(request, occurrence_maincat, feature_id):
    if occurrence_maincat[0]=='n': # natural areas
        feat = OccurrenceNaturalArea.objects.get(pk=feature_id)
    else:
        feat = OccurrenceTaxon.objects.get(pk=feature_id)
    serializer = FeatureTypeSerializer(feat)
    ftdata = serializer.get_feature_type()
    return Response(ftdata)

@api_view(['GET'])
@permission_classes([])
def get_feature_info(request, occurrence_maincat, feature_id):
    if occurrence_maincat[0]=='n': # natural areas
        feat = OccurrenceNaturalArea.objects.get(pk=feature_id)
    else:
        feat = OccurrenceTaxon.objects.get(pk=feature_id)
    #main_cat = feat.occurrence_cat.main_cat
    #subcat_code = feat.occurrence_cat.code
    serializer = FeatureInfoSerializer()
    ftdata = serializer.get_feature_info(feat)
    return Response(ftdata)

"""
"""


class TaxonFeatureTypeView(APIView):
    permission_classes = ()
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return OccurrenceTaxon.objects.get(pk=pk)
        except OccurrenceTaxon.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = LayerTaxonSerializer(obj)
        return Response(serializer.data)

class PlantDetail(APIView):
    permission_classes = ()
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return OccurrenceTaxon.objects.get(pk=pk)
        except OccurrenceTaxon.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = LayerTaxonSerializer(obj)
        return Response(serializer.data)
        

    def put(self, request, pk, format=None):
        obj = self.get_object(pk)
        serializer = LayerTaxonSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
"""
    class Meta:
        model = OccurrenceTaxon
        fields = ('inclusion_date', 'released')
"""

plants = ['plant', 'plant_conifer_or_ally', 'plant_fern_or_ally',
          'plant_flowering_plant', 'plant_moss_or_ally']
slime_mold = ['slime_mold']
fungus = ['fungus']
animals = ['animal', 'animal_aquatic_animal', 'animal_land_animal',
           'animal_pond_lake_animal', 'animal_stream_animal', 'animal_wetland_animal']
natural_area = ['natural_area']

layers = plants + slime_mold + fungus + animals + natural_area
"""
# POR TIPO
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
