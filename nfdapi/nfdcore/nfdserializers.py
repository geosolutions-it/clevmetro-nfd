from collections import OrderedDict
from collections import Mapping
import datetime as dt
import logging

from django.db.models.fields import (
    BooleanField,
    CharField,
    DateTimeField,
    DateField,
    DecimalField,
    IntegerField,
    FloatField,
    NullBooleanField,
    TextField,
    NOT_PROVIDED,
)
from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.gis.geos import Polygon
from django.contrib.gis.db.models.fields import GeometryField
from django.contrib.gis.db.models.fields import PolygonField
from django.template.defaultfilters import date

from rest_framework import serializers
from rest_framework import fields as rest_fields
from rest_framework_gis import serializers as gisserializer
import reversion
from reversion.models import Version
from rest_framework.exceptions import ValidationError

from . import models

logger = logging.getLogger(__name__)


def _(message):
    return message


""" -------------------------------------------
UTILITY METHODS AND CLASSES
---------------------------------------------- """

def get_form_dict(forms):
    form_dict = {}
    for form in forms:
        form_dict[form[0]] = form
    return form_dict

MANAGEMENT_FORM_NAME = _('occurrencemanagement')
MANAGEMENT_FORM_ITEMS = [{
        "key": "id",
        "label": _("id"),
        "type": "integer",
        'readonly': True
    },{
        "key": "featuretype",
        "label": _("featuretype"),
        "type": "string",
        'readonly': True
    },{
        "key": "featuresubtype",
        "label": _("featuresubtype"),
        "type": "string",
        'readonly': True
    },{
        "key": "released",
        "label": _("released"),
        "type": "boolean",
        'readonly': True
    },{
        "key": "verified",
        "label": _("verified"),
        "type": "boolean",
        'readonly': False
    },{
        "key": "inclusion_date",
        "label": _("inclusion_date"),
        "type": "string",
        'readonly': True
    },{
        "key": "version_date",
        "label": _("version_date"),
        "type": "string",
        'readonly': True
    }]

MANAGEMENT_FORM_ITEMS_PUBLISHER = [{
        "key": "id",
        "label": _("id"),
        "type": "integer",
        'readonly': True
    },{
        "key": "featuretype",
        "label": _("featuretype"),
        "type": "string",
        'readonly': True
    },{
        "key": "featuresubtype",
        "label": _("featuresubtype"),
        "type": "string",
        'readonly': True
    },{
        "key": "released",
        "label": _("released"),
        "type": "boolean",
        'readonly': False
    },{
        "key": "verified",
        "label": _("verified"),
        "type": "boolean",
        'readonly': False
    },{
        "key": "inclusion_date",
        "label": _("inclusion_date"),
        "type": "string",
        'readonly': True
    },{
        "key": "version_date",
        "label": _("version_date"),
        "type": "string",
        'readonly': True
    }]
    

LAND_ANIMAL_TYPE = [
    (_('species'), models.Species, ['species.element_species']),
    (_('species.element_species'), models.ElementSpecies, []),
    (MANAGEMENT_FORM_NAME, models.OccurrenceTaxon, []),
    (_('observation'), models.OccurrenceObservation, ['observation.reporter', 'observation.verifier', 'observation.recorder']),
    (_('observation.reporter'), models.PointOfContact, []),
    (_('observation.verifier'), models.PointOfContact, []),
    (_('observation.recorder'), models.PointOfContact, []),
    (_('voucher'), models.Voucher, []),
    (_('details'), models.LandAnimalDetails, ['details.lifestages']),
    (_('details.lifestages'), models.AnimalLifestages, []),
    (_('location'), models.TaxonLocation, []),
    ]
LAND_ANIMAL_TYPE_DICT = get_form_dict(LAND_ANIMAL_TYPE)

STREAM_ANIMAL_TYPE = [
    (_('species'), models.Species, ['species.element_species']),
    (_('species.element_species'), models.ElementSpecies, []),
    (MANAGEMENT_FORM_NAME, models.OccurrenceTaxon, []),
    (_('observation'), models.OccurrenceObservation, ['observation.reporter', 'observation.verifier', 'observation.recorder']),
    (_('observation.reporter'), models.PointOfContact, []),
    (_('observation.verifier'), models.PointOfContact, []),
    (_('observation.recorder'), models.PointOfContact, []),
    (_('voucher'), models.Voucher, []),
    (_('details'), models.StreamAnimalDetails, ['details.lifestages', 'details.substrate']),
    (_('details.lifestages'), models.AnimalLifestages, []),
    (_('details.substrate'), models.StreamSubstrate, []),
    (_('location'), models.TaxonLocation, []),
    ]

STREAM_ANIMAL_TYPE_DICT = get_form_dict(STREAM_ANIMAL_TYPE)

PONDLAKE_ANIMAL_TYPE = [
    (_('species'), models.Species, ['species.element_species']),
    (_('species.element_species'), models.ElementSpecies, []),
    (MANAGEMENT_FORM_NAME, models.OccurrenceTaxon, []),
    (_('observation'), models.OccurrenceObservation, ['observation.reporter', 'observation.verifier', 'observation.recorder']),
    (_('observation.reporter'), models.PointOfContact, []),
    (_('observation.verifier'), models.PointOfContact, []),
    (_('observation.recorder'), models.PointOfContact, []),
    (_('voucher'), models.Voucher, []),
    (_('details'), models.PondLakeAnimalDetails, ['details.lifestages']),
    (_('details.lifestages'), models.AnimalLifestages, []),
    (_('location'), models.TaxonLocation, []),
    ]
PONDLAKE_ANIMAL_TYPE_DICT = get_form_dict(PONDLAKE_ANIMAL_TYPE)


WETLAND_ANIMAL_TYPE = [
    (_('species'), models.Species, ['species.element_species']),
    (_('species.element_species'), models.ElementSpecies, []),
    (MANAGEMENT_FORM_NAME, models.OccurrenceTaxon, []),
    (_('observation'), models.OccurrenceObservation, ['observation.reporter', 'observation.verifier', 'observation.recorder']),
    (_('observation.reporter'), models.PointOfContact, []),
    (_('observation.verifier'), models.PointOfContact, []),
    (_('observation.recorder'), models.PointOfContact, []),
    (_('voucher'), models.Voucher, []),
    (_('details'), models.WetlandAnimalDetails, ['details.lifestages', 'details.vegetation']),
    (_('details.lifestages'), models.AnimalLifestages, []),
    (_('details.vegetation'), models.WetlandVetegationStructure, []),
    (_('location'), models.TaxonLocation, []),
    ]
WETLAND_ANIMAL_TYPE_DICT = get_form_dict(WETLAND_ANIMAL_TYPE)

SLIMEMOLD_TYPE = [
    (_('species'), models.Species, ['species.element_species']),
    (_('species.element_species'), models.ElementSpecies, []),
    (MANAGEMENT_FORM_NAME, models.OccurrenceTaxon, []),
    (_('observation'), models.OccurrenceObservation, ['observation.reporter', 'observation.verifier', 'observation.recorder']),
    (_('observation.reporter'), models.PointOfContact, []),
    (_('observation.verifier'), models.PointOfContact, []),
    (_('observation.recorder'), models.PointOfContact, []),
    (_('voucher'), models.Voucher, []),
    (_('details'), models.SlimeMoldDetails, ['details.lifestages']),
    (_('details.lifestages'), models.SlimeMoldLifestages, []),
    (_('location'), models.TaxonLocation, []),
    ]
SLIMEMOLD_TYPE_DICT = get_form_dict(SLIMEMOLD_TYPE)

CONIFER_PLANT_TYPE = [
    (_('species'), models.Species, ['species.element_species']),
    (_('species.element_species'), models.ElementSpecies, []),
    (MANAGEMENT_FORM_NAME, models.OccurrenceTaxon, []),
    (_('observation'), models.OccurrenceObservation, ['observation.reporter', 'observation.verifier', 'observation.recorder']),
    (_('observation.reporter'), models.PointOfContact, []),
    (_('observation.verifier'), models.PointOfContact, []),
    (_('observation.recorder'), models.PointOfContact, []),
    (_('voucher'), models.Voucher, []),
    (_('details'), models.ConiferDetails, ['details.lifestages', 'details.earthworm_evidence', 'details.disturbance_type']),
    (_('details.lifestages'), models.ConiferLifestages, []),
    (_('details.earthworm_evidence'), models.EarthwormEvidence, []),
    (_('details.disturbance_type'), models.DisturbanceType, []),
    (_('location'), models.TaxonLocation, []),
    ]
CONIFER_PLANT_TYPE_DICT = get_form_dict(CONIFER_PLANT_TYPE)

FERN_PLANT_TYPE = [
    (_('species'), models.Species, ['species.element_species']),
    (_('species.element_species'), models.ElementSpecies, []),
    (MANAGEMENT_FORM_NAME, models.OccurrenceTaxon, []),
    (_('observation'), models.OccurrenceObservation, ['observation.reporter', 'observation.verifier', 'observation.recorder']),
    (_('observation.reporter'), models.PointOfContact, []),
    (_('observation.verifier'), models.PointOfContact, []),
    (_('observation.recorder'), models.PointOfContact, []),
    (_('voucher'), models.Voucher, []),
    (_('details'), models.FernDetails, ['details.earthworm_evidence', 'details.disturbance_type']),
    (_('details.earthworm_evidence'), models.EarthwormEvidence, []),
    (_('details.disturbance_type'), models.DisturbanceType, []),
    (_('location'), models.TaxonLocation, []),
    ]
FERN_PLANT_TYPE_DICT = get_form_dict(FERN_PLANT_TYPE)

FLOWERING_PLANT_TYPE = [
    (_('species'), models.Species, ['species.element_species']),
    (_('species.element_species'), models.ElementSpecies, []),
    (MANAGEMENT_FORM_NAME, models.OccurrenceTaxon, []),
    (_('observation'), models.OccurrenceObservation, ['observation.reporter', 'observation.verifier', 'observation.recorder']),
    (_('observation.reporter'), models.PointOfContact, []),
    (_('observation.verifier'), models.PointOfContact, []),
    (_('observation.recorder'), models.PointOfContact, []),
    (_('voucher'), models.Voucher, []),
    (_('details'), models.FloweringPlantDetails, ['details.earthworm_evidence', 'details.disturbance_type']),
    (_('details.earthworm_evidence'), models.EarthwormEvidence, []),
    (_('details.disturbance_type'), models.DisturbanceType, []),
    (_('location'), models.TaxonLocation, []),
    ]
FLOWERING_PLANT_TYPE_DICT = get_form_dict(FLOWERING_PLANT_TYPE)

MOSS_PLANT_TYPE = [
    (_('species'), models.Species, ['species.element_species']),
    (_('species.element_species'), models.ElementSpecies, []),
    (MANAGEMENT_FORM_NAME, models.OccurrenceTaxon, []),
    (_('observation'), models.OccurrenceObservation, ['observation.reporter', 'observation.verifier', 'observation.recorder']),
    (_('observation.reporter'), models.PointOfContact, []),
    (_('observation.verifier'), models.PointOfContact, []),
    (_('observation.recorder'), models.PointOfContact, []),
    (_('voucher'), models.Voucher, []),
    (_('details'), models.MossDetails, ['details.earthworm_evidence', 'details.disturbance_type']),
    (_('details.earthworm_evidence'), models.EarthwormEvidence, []),
    (_('details.disturbance_type'), models.DisturbanceType, []),
    (_('location'), models.TaxonLocation, []),
    ]
MOSS_PLANT_TYPE_DICT = get_form_dict(MOSS_PLANT_TYPE)

FUNGUS_TYPE = [
    (_('species'), models.Species, ['species.element_species']),
    (_('species.element_species'), models.ElementSpecies, []),
    (MANAGEMENT_FORM_NAME, models.OccurrenceTaxon, []),
    (_('observation'), models.OccurrenceObservation, ['observation.reporter', 'observation.verifier', 'observation.recorder']),
    (_('observation.reporter'), models.PointOfContact, []),
    (_('observation.verifier'), models.PointOfContact, []),
    (_('observation.recorder'), models.PointOfContact, []),
    (_('voucher'), models.Voucher, []),
    (_('details'), models.FungusDetails, ['details.earthworm_evidence', 'details.disturbance_type', 'details.other_observed_associations', 'details.fruiting_bodies_age']),
    (_('details.earthworm_evidence'), models.EarthwormEvidence, []),
    (_('details.disturbance_type'), models.DisturbanceType, []),
    (_('details.other_observed_associations'), models.ObservedAssociations, []),
    (_('details.fruiting_bodies_age'), models.FruitingBodiesAge, []),
    (_('location'), models.TaxonLocation, []),
    ]
FUNGUS_TYPE_DICT = get_form_dict(FUNGUS_TYPE)

NATURAL_AREA_TYPE = [
    (_('element'), models.ElementNaturalAreas, ['element.earthworm_evidence', 'element.disturbance_type']),
    (MANAGEMENT_FORM_NAME, models.OccurrenceTaxon, []),
    (_('observation'), models.OccurrenceObservation, ['observation.reporter', 'observation.verifier', 'observation.recorder']),
    (_('observation.reporter'), models.PointOfContact, []),
    (_('observation.verifier'), models.PointOfContact, []),
    (_('observation.recorder'), models.PointOfContact, []),
    (_('element.earthworm_evidence'), models.EarthwormEvidence, []),
    (_('element.disturbance_type'), models.DisturbanceType, []),
    (_('location'), models.NaturalAreaLocation, []),
    ]
NATURAL_AREA_TYPE_DICT = get_form_dict(NATURAL_AREA_TYPE)


del _
from django.utils.translation import ugettext_lazy as _


def get_details_serializer(category_code):
    if category_code=='co':
        return ConiferDetailsSerializer
    elif category_code=='fe':
        return FernDetailsSerializer
    elif category_code=='fl':
        return FloweringPlantDetailsSerializer
    elif category_code=='pl':
        return serializers.Serializer # FIXME
    elif category_code=='mo':
        return MossDetailsSerializer
    elif category_code=='fu':
        return FungusDetailsSerializer
    elif category_code=='sl':
        return SlimeMoldDetailsSerializer
    elif category_code=='ln':
        return LandAnimalDetailsSerializer
    elif category_code=='lk':
        return PondLakeAnimalDetailsSerializer
    elif category_code=='st':
        return StreamAnimalDetailsSerializer
    elif category_code=='we':
        return WetlandAnimalDetailsSerializer
    elif category_code=='na':
        return NaturalAreaElementSerializer

def is_deletable_field(f):
    if not getattr(f, 'related_model', False):
        return False
    if getattr(f, 'auto_created', False):
        return False
    if issubclass(f.related_model, models.DictionaryTable):
        return False
    if issubclass(f.related_model, models.DictionaryTableExtended):
        return False
    if issubclass(f.related_model, models.Species):
        return False
    return True
    

def delete_object_and_children(parent_instance):
    
    children = []

    if not getattr(parent_instance, '_meta', None):
        print parent_instance
        print type(parent_instance)
        print repr(parent_instance)
    if not isinstance(parent_instance, QuerySet):
        for f in parent_instance._meta.get_fields():
            if is_deletable_field(f):
                child_instance = getattr(parent_instance, f.name, None)
                if isinstance(f, GenericRelation):
                    # for generic related objects such as photographs, we get the related QuerySet
                    child_instance = child_instance.all()
                if child_instance:
                    children.append(child_instance)
    
    # some children are mandatory for the parent, so we first delete parents
    parent_instance.delete()
    for child_instance in children:
        delete_object_and_children(child_instance)

class DictionaryField(rest_fields.CharField):
    def get_attribute(self, instance):
        entry_instance = super(DictionaryField, self).get_attribute(instance)
        #entry_instance = get_attribute(instance, self.source_attrs)
        #field_name = self.source_attrs[-1]
        #entry_instance = getattr(instance, field_name, None)
        if entry_instance:
            return getattr(entry_instance, 'code', None)

    def to_internal_value(self, data):
        return rest_fields.CharField.to_internal_value(self, data)
    
    def to_representation(self, value):
        return rest_fields.CharField.to_representation(self, value)

class DictionaryExtendedField(rest_fields.CharField):
    def get_attribute(self, instance):
        entry_instance = super(DictionaryExtendedField, self).get_attribute(instance)
        #entry_instance = get_attribute(instance, self.source_attrs)
        #field_name = self.source_attrs[-1]
        #entry_instance = getattr(instance, field_name, None)
        if entry_instance:
            return getattr(entry_instance, 'code', None)

    def to_internal_value(self, data):
        return rest_fields.CharField.to_internal_value(self, data)
    
    def to_representation(self, value):
        return rest_fields.CharField.to_representation(self, value)

class TotalVersionsField(rest_fields.IntegerField):
    def get_attribute(self, instance):
        versions = Version.objects.get_for_object(instance).count()
        if versions<1:
            versions = 1
        return versions

def get_serializer_fields(form_name, model):
    fields = model._meta.get_fields()
    result = OrderedDict()
    for f in fields:
        fdef = None
        
        kwargs = {}
        if getattr(f, 'default', NOT_PROVIDED) != NOT_PROVIDED:
            kwargs['default'] = getattr(f, 'default')
        
        if getattr(f, 'primary_key', False):
            pass
        elif isinstance(f, CharField) or isinstance(f, TextField):
            kwargs['max_length'] = getattr(f, 'max_length', None)
            kwargs['allow_blank'] = getattr(f, 'blank', False)
            kwargs['allow_null'] = getattr(f, 'null', False)
            kwargs['required'] = not getattr(f, 'null', False)
            fdef = rest_fields.CharField(**kwargs)
        elif isinstance(f, BooleanField):
            fdef = rest_fields.BooleanField(**kwargs)
        elif isinstance(f, NullBooleanField):
            kwargs['required'] = not getattr(f, 'null', False)
            fdef = rest_fields.NullBooleanField(**kwargs)
        elif isinstance(f, DateTimeField):
            kwargs['allow_null'] = getattr(f, 'null', False)
            kwargs['required'] = not getattr(f, 'null', False)
            fdef = rest_fields.DateTimeField(**kwargs)
        elif isinstance(f, DateField):
            kwargs['allow_null'] = getattr(f, 'null', False)
            kwargs['required'] = not getattr(f, 'null', False)
            fdef = rest_fields.DateField(**kwargs)
        elif isinstance(f, DecimalField):
            kwargs['allow_null'] = getattr(f, 'null', False)
            kwargs['required'] = not getattr(f, 'null', False)
            kwargs['max_digits'] = getattr(f, 'max_digits', None)
            kwargs['decimal_places'] = getattr(f, 'decimal_places', None)
            fdef = rest_fields.DecimalField(**kwargs)
        elif isinstance(f, FloatField):
            kwargs['allow_null'] = getattr(f, 'null', False)
            kwargs['required'] = not getattr(f, 'null', False)
            fdef = rest_fields.FloatField(**kwargs)
        elif isinstance(f, IntegerField):
            kwargs['allow_null'] = getattr(f, 'null', False)
            kwargs['required'] = not getattr(f, 'null', False)
            fdef = rest_fields.IntegerField(**kwargs)
        elif getattr(f, 'related_model', False):
            kwargs['allow_blank'] = getattr(f, 'blank', False)
            kwargs['allow_null'] = getattr(f, 'null', False)
            kwargs['required'] = not getattr(f, 'null', False)
            if issubclass(f.related_model, models.DictionaryTable):
                fdef = DictionaryField(**kwargs)
            elif issubclass(f.related_model, models.DictionaryTableExtended):
                fdef = DictionaryExtendedField(**kwargs)
        elif isinstance(f, GeometryField):
            # skip geoms
            pass
            
        if fdef:
            if form_name:
                result[form_name + "." + f.name] = fdef
            else:
                result[f.name] = fdef
    return result


class OccurrenceRelatedObjectSerialzer(serializers.Serializer):
    def __init__(self, instance=None, data=rest_fields.empty, model=None, **kwargs):
        self._model = model
        serializers.Serializer.__init__(self, instance=instance, data=data, **kwargs)


def check_all_null(field_dict):
    if field_dict is None or field_dict is rest_fields.empty:
        return True
    for value in field_dict.values():
        if isinstance(value, dict):
            if not check_all_null(value):
                return False
        elif not (value is None or value == ''):
            return False
    return True

def to_flat_representation(values_dict, parent_path=None):
    result = OrderedDict()
    for fname, fvalue in values_dict.items():
        if parent_path:
            global_fname = parent_path + "." + fname
        else:
            global_fname = fname

        if fname != 'geom' and isinstance(fvalue, dict):
            child_dict = to_flat_representation(fvalue, global_fname)
            result.update(child_dict)
        else:
            result[global_fname] = fvalue
    return result

class CustomModelSerializerMixin(object):
    """
    Used by most of our model serializers to properly manage dictionaries and to ignore
    empty forms when they are not required
    """
    def build_field(self, field_name, info, model_class, nested_depth):
        """
        Return a two tuple of (cls, kwargs) to build a serializer field with.
        """
        if field_name in info.relations:
            relation_info = info.relations[field_name]
            if issubclass(relation_info.related_model, models.DictionaryTable):
                f = DictionaryField
                kwargs = {}
                if relation_info.model_field.blank:
                    kwargs["allow_blank"] = True
                    kwargs["required"] = False
                if relation_info.model_field.null:
                    kwargs["required"] = False
                    kwargs["allow_null"] = True
                
                return f, kwargs
            elif issubclass(relation_info.related_model, models.DictionaryTableExtended):
                f = DictionaryExtendedField
                kwargs = {}
                if relation_info.model_field.blank:
                    kwargs["allow_blank"] = True
                    kwargs["required"] = False
                if relation_info.model_field.null:
                    kwargs["required"] = False
                    kwargs["allow_null"] = True
                return f, kwargs
        return super(CustomModelSerializerMixin, self).build_field(field_name, info, model_class, nested_depth)

    def run_validation(self, data=rest_fields.empty):
        """
        We override the default `run_validation`, because the validation
        performed by validators and the `.validate()` method should
        be coerced into an error dictionary with a 'non_fields_error' key.
        """
        if not self.required and check_all_null(data):
            raise rest_fields.SkipField("Non required empty form")
        return super(CustomModelSerializerMixin, self).run_validation(data)

def init_forms(instance, category_code):
        if category_code=='co':
            instance.forms = CONIFER_PLANT_TYPE
            instance._form_dict = CONIFER_PLANT_TYPE_DICT
        elif category_code=='fe':
            instance.forms = FERN_PLANT_TYPE
            instance._form_dict = FERN_PLANT_TYPE_DICT
        elif category_code=='fl':
            instance.forms = FLOWERING_PLANT_TYPE
            instance._form_dict = FLOWERING_PLANT_TYPE_DICT
        elif category_code=='pl':
            return None #FIXME
        elif category_code=='mo':
            instance.forms = MOSS_PLANT_TYPE
            instance._form_dict = MOSS_PLANT_TYPE_DICT
        elif category_code=='fu':
            instance.forms = FUNGUS_TYPE
            instance._form_dict = FUNGUS_TYPE_DICT
        elif category_code=='sl':
            instance.forms = SLIMEMOLD_TYPE
            instance._form_dict = SLIMEMOLD_TYPE_DICT
        elif category_code=='ln':
            instance.forms = LAND_ANIMAL_TYPE
            instance._form_dict = LAND_ANIMAL_TYPE_DICT
        elif category_code=='lk':
            instance.forms = PONDLAKE_ANIMAL_TYPE
            instance._form_dict = PONDLAKE_ANIMAL_TYPE_DICT
        elif category_code=='st':
            instance.forms = STREAM_ANIMAL_TYPE
            instance._form_dict = STREAM_ANIMAL_TYPE_DICT
        elif category_code=='we':
            instance.forms = WETLAND_ANIMAL_TYPE
            instance._form_dict = WETLAND_ANIMAL_TYPE_DICT
        elif category_code=='na':
            instance.forms = NATURAL_AREA_TYPE
            instance._form_dict = NATURAL_AREA_TYPE_DICT

class UpdateOccurrenceMixin(object):
    def __init__(self, instance=None, data=rest_fields.empty, is_writer=False, is_publisher=False, **kwargs):
        self.is_writer = is_writer
        self.is_publisher = is_publisher
        if instance and instance.occurrence_cat:
            init_forms(self, instance.occurrence_cat.code)
        super(UpdateOccurrenceMixin, self).__init__(instance, data, **kwargs)
        
    def _get_local_name(self, global_field_name):
        """
        Gets the local name of the provided attrib
        Example _get_local_name("species.element_species.native") returns "native"
        """
        parts = global_field_name.split(".")
        if len(parts)>0:
            return parts[-1]
        
    def _get_form_fields(self, form_name, instance):
        """
        Gets the field names of the given instance, using global name notation (e.g. "observation.reporter.name" )
        """
        result = []
        if (instance):
            return instance._meta.get_fields()                      
        return result
    
    def _get_validated_data_form(self, validated_data, form_name):
        """
        validated_data:
        form_name: dictionary key including subdicts (e.g. "species.element_species")
        Returns the data located on validated_data['species']['element_species'] or None if does not exist
        """
        if validated_data:
            if form_name == MANAGEMENT_FORM_NAME:
                return validated_data
            else:            
                parts = form_name.split(".")
                subdict = validated_data
                for part in parts:
                    subdict = subdict.get(part)
                    if subdict is None:
                        return None
            return subdict
        
    def set_form_values(self, form_name, instance, form_validated_data, force_save=False):
        """
        Updates the values of the provided instance using validated data 
        """
        if instance:
            if form_validated_data:
                fields = self._get_form_fields(form_name, instance)
                modified = False
                for f in fields:
                    if getattr(f, 'primary_key', False):
                        pass
                    elif getattr(f, 'related_model', False):
                        if issubclass(f.related_model, models.DictionaryTable) or issubclass(f.related_model, models.DictionaryTableExtended):
                            new_value = form_validated_data.get(f.name)
                            old_value =  getattr(instance, f.name, None)
                            if old_value != new_value and (old_value is None or new_value != old_value.code):
                                try:
                                    if new_value != None:
                                        dict_entry = f.related_model.objects.get(code=new_value)
                                    else:
                                        dict_entry = None
                                    modified = True
                                    setattr(instance, f.name, dict_entry)
                                except Exception as exc:
                                    setattr(instance, f.name, None)
                    else:
                        if isinstance(f, CharField) or isinstance(f, TextField):
                            new_value = form_validated_data.get(f.name, '')
                            if new_value is None:
                                new_value = ''
                            old_value =  getattr(instance, f.name, '')
                            if old_value is None:
                                old_value = ''
                        elif isinstance(f, DateTimeField) or isinstance(f, DateField):
                            new_value = form_validated_data.get(f.name, '')
                            old_value =  getattr(instance, f.name, None)
                        elif isinstance(f, BooleanField) or isinstance(f, NullBooleanField) or \
                                isinstance(f, FloatField) or isinstance(f, DecimalField) or isinstance(f, IntegerField):
                            new_value = form_validated_data.get(f.name)
                            old_value =  getattr(instance, f.name, None)
                        elif isinstance(f, PolygonField):
                            new_value = form_validated_data.get(f.name)
                            old_value =  getattr(instance, f.name, None)
                        #if new_value != None and new_value != old_value:
                        if new_value != old_value:
                            modified = True
                            setattr(instance, f.name, new_value)

                if force_save or modified:
                    instance.save()
                    return True
            else:
                # if the form is empty and instance exists, delete instance
                try: 
                    instance.delete()
                except:
                    pass
                return True
        return False
    
    def _get_form_model_instance(self, form_name, model_class, parent_instance):
        """
        Gets the related instance for the provided form name and parent instance.
        """
        if parent_instance is not None:
            if form_name == 'details':
                related_instance = parent_instance.get_details()
            else:
                related_instance = getattr(parent_instance, self._get_local_name(form_name), None)
            return related_instance
    
    def _update_form(self, form_name, model_class, validated_data, parent_instance, child_forms=[]):
        """
        Updates the appropriate instance according to the provided form_name and model instance. All
        related objects are also updated if modified.
        
        Returns True if the instance has been modified and saved, False if there were no changes. 
        """
        form_validated_data = self._get_validated_data_form(validated_data, form_name)
        
        related_instance = self._get_form_model_instance(form_name, model_class, parent_instance)
        if form_validated_data and not related_instance:
            related_instance = model_class()
            
        any_saved = False
        for (child_form_name, child_model_class, child_child_forms) in child_forms:
            saved = self._update_form(child_form_name, child_model_class, validated_data, related_instance, child_child_forms)
            any_saved = any_saved or saved
        
        saved = self.set_form_values(form_name, related_instance, form_validated_data, any_saved)
        any_saved = any_saved or saved
        
        if any_saved:
            if form_validated_data is None:
                setattr(parent_instance, self._get_local_name(form_name), None)
            else:
                setattr(parent_instance, self._get_local_name(form_name), related_instance)
        return any_saved
    
    def _get_form_dict(self):
        """
        Gets the definition of forms for the current instance type
        """
        if not self._form_dict:
            self._form_dict = get_form_dict(self.get_forms())
        return self._form_dict
        
    def _get_form_def_tree(self, form_name, model_class, children):
        """
        Gets the definition of a form and its related objects (children)
        """
        complete_children_def = []
        for child in children:
            (child_form_name, child_model_class, child_children) = self._get_form_dict()[child]
            child_def = self._get_form_def_tree(child_form_name, child_model_class, child_children)
            complete_children_def.append(child_def)
        return (form_name, model_class, complete_children_def)
    
    def get_toplevel_forms(self):
        """
        Gets the definition of the forms which are directly related to Occurrence objects. Each
        form contains also the definition of its related objects (as children)
        """
        forms = []
        for (form_name, model_class, children) in self.get_forms():
            if "." not in form_name:
                # only for top-level objects
                form_def = self._get_form_def_tree(form_name, model_class, children)
                forms.append(form_def)
        return forms
    
    def get_forms(self):
        """
        Gets the definition of all forms
        """
        return self.forms
    
    def process_photos(self, instance, validated_data):
        images = validated_data.get('images')
        if images:
            try:
                updated_ids = [i.get('id') for i in images]
                instance.photographs.exclude(pk__in=updated_ids).delete()
                
                for photo_data in validated_data.get('images'):
                    try:
                        photo = models.Photograph.objects.get(pk=photo_data.get('id'))
                    except:
                        if Version.objects.get_for_object_reference(models.Photograph, photo_data.get('id')).count() > 0:
                            # we are restoring a removed photo
                            last_version = Version.objects.get_for_object_reference(models.Photograph, photo_data.get('id'))[0]
                            # ensure the photo matches current instance
                            if last_version.field_dict.get('occurrence_fk') != instance.id:
                                raise ValidationError({"images": [_("Tried to restore an invalid image")]})
                            if last_version.field_dict.get('content_type_id') != ContentType.objects.get_for_model(instance._meta.model).pk:
                                raise ValidationError({"images": [_("Tried to restore an invalid image")]})
                            last_version.revert()
                            photo = models.Photograph.objects.get(pk=photo_data.get('id'))
                    updated = False
                    if not photo.occurrence:
                        photo.occurrence = instance
                        updated = True
                    elif photo.occurrence != instance:
                        raise ValidationError({"images": [_("Invalid images were specified")]})
                    notes = photo_data.get('notes')
                    if photo.notes != notes:
                        photo.notes = notes
                        updated = True
                    desc = photo_data.get('description')
                    if photo.description != desc:
                        photo.description = desc
                        updated = True
                    if updated:
                        photo.save()
            except ValidationError:
                raise
            except:
                raise ValidationError({"images": [_("Invalid images were specified")]})
        else:
            instance.photographs.all().delete()

    def update(self, instance, validated_data):
        with reversion.create_revision():
            for (form_name, model_class, children) in self.get_toplevel_forms():
                if form_name == 'species':
                    try:
                        species_id = validated_data['species']['id']
                        selected_species = models.Species.objects.get(pk=species_id)
                        instance.species = selected_species
                    except:
                        raise ValidationError({"species": [_("No species was selected")]})
                elif form_name != MANAGEMENT_FORM_NAME:
                    self._update_form(form_name, model_class, validated_data, instance, children)
           
            instance.geom = validated_data.get("geom") or instance.geom
            instance.version = instance.version + 1
            instance.verified = validated_data.get("verified", False) or False
            if self.is_publisher:
                instance.released = validated_data.get("released", False) or False
                if instance.released:
                    instance.released_versions = instance.released_versions + 1
            else:
                instance.released = False
            instance.save()
            # ensure the instance has been saved before associating photos
            self.process_photos(instance, validated_data)
        return instance
    
    def create(self, validated_data):
        code = validated_data.get('featuresubtype')
        if code == 'na':
            instance = models.OccurrenceNaturalArea()
        else:
            instance = models.OccurrenceTaxon()
        instance.occurrence_cat = models.OccurrenceCategory.objects.get(code=code)
        instance.geom = validated_data.get('geom')
        init_forms(self, instance.occurrence_cat.code)
        return self.update(instance, validated_data)


""" -------------------------------------------
MODEL SERIALIZERs
---------------------------------------------- """
class VoucherSerializer(CustomModelSerializerMixin,
                        serializers.ModelSerializer):
    class Meta:
        model = models.Voucher
        exclude = ('id',)

class ElementSpeciesSerializer(CustomModelSerializerMixin,
                               serializers.ModelSerializer):
    class Meta:
        model = models.ElementSpecies
        exclude = ('id',)
        read_only_fields = ("native", "oh_status", "usfws_status", "iucn_red_list_category", \
                            "other_code", "ibp_english", "ibp_scientific", "bblab_number", "nrcs_usda_symbol", \
                            "synonym_nrcs_usda_symbol", "epa_numeric_code", "mushroom_group", \
                            "cm_status", "s_rank", "n_rank", "g_rank")

class SpeciesSerializer(CustomModelSerializerMixin,
                        serializers.ModelSerializer):
    element_species = ElementSpeciesSerializer(required=False, read_only=True)
    
    def to_internal_value(self, data):
        result = super(SpeciesSerializer, self).to_internal_value(data)
        if data.get("id"):
            # We need the id of the new species to set it in the occurrence 
            result['id'] = data.get('id')
        return result
    
    class Meta:
        model = models.Species
        fields = "__all__"
        read_only_fields = ("first_common", "name_sci", "tsn", "synonym", "second_common", "third_common", "family", "family_common", "phylum", "phylum_common")

class PointOfContactSerializer(CustomModelSerializerMixin,
                               serializers.ModelSerializer):
        
    class Meta:
        model = models.PointOfContact
        exclude = ('id',)

class OccurrenceObservationSerializer(CustomModelSerializerMixin,
                                      serializers.ModelSerializer):
    reporter = PointOfContactSerializer(required=True)
    recorder = PointOfContactSerializer(required=False)
    verifier = PointOfContactSerializer(required=False)
        
    class Meta:
        model = models.OccurrenceObservation
        exclude = ('id',)


class AnimalLifestagesSerializer(CustomModelSerializerMixin,
                                 serializers.ModelSerializer):
    class Meta:
        model = models.AnimalLifestages
        exclude = ('id',)

class BaseDetailsSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        if instance:
            #self.set_model_class(instance.occurrencetaxon.get_details_class())
            instance = instance.occurrencetaxon.get_details()
        return super(BaseDetailsSerializer, self).to_representation(instance)
    
class LandAnimalDetailsSerializer(CustomModelSerializerMixin, BaseDetailsSerializer):
    lifestages = AnimalLifestagesSerializer(required=False)
    class Meta:
        model = models.LandAnimalDetails
        exclude = ('id',)

class WetlandVetegationStructureSerializer(CustomModelSerializerMixin,
                                           serializers.ModelSerializer):
    class Meta:
        model = models.WetlandVetegationStructure
        exclude = ('id',)

class WetlandAnimalDetailsSerializer(CustomModelSerializerMixin, BaseDetailsSerializer):
    lifestages = AnimalLifestagesSerializer(required=False)
    vegetation = WetlandVetegationStructureSerializer(required=False)
    class Meta:
        model = models.WetlandAnimalDetails
        exclude = ('id',)


class StreamSubstrateSerializer(CustomModelSerializerMixin,
                                serializers.ModelSerializer):
    class Meta:
        model = models.StreamSubstrate
        exclude = ('id',)

class StreamAnimalDetailsSerializer(CustomModelSerializerMixin, BaseDetailsSerializer):
    lifestages = AnimalLifestagesSerializer(required=False)
    substrate = StreamSubstrateSerializer(required=False)
    class Meta:
        model = models.StreamAnimalDetails
        exclude = ('id',)

class PondLakeAnimalDetailsSerializer(CustomModelSerializerMixin, BaseDetailsSerializer):
    lifestages = AnimalLifestagesSerializer(required=False)
    class Meta:
        model = models.PondLakeAnimalDetails
        exclude = ('id',)

class ConiferLifestagesSerializer(CustomModelSerializerMixin,
                                  serializers.ModelSerializer):
    class Meta:
        model = models.ConiferLifestages
        exclude = ('id',)


class DisturbanceTypeSerializer(CustomModelSerializerMixin,
                                serializers.ModelSerializer):
    class Meta:
        model = models.DisturbanceType
        exclude = ('id',)

class EarthwormEvidenceSerializer(CustomModelSerializerMixin,
                                  serializers.ModelSerializer):
    class Meta:
        model = models.EarthwormEvidence
        exclude = ('id',)

class ConiferDetailsSerializer(CustomModelSerializerMixin, BaseDetailsSerializer):
    lifestages = ConiferLifestagesSerializer(required=False)
    disturbance_type = DisturbanceTypeSerializer(required=False)
    earthworm_evidence = EarthwormEvidenceSerializer(required=False)
    
    class Meta:
        model = models.ConiferDetails
        exclude = ('id',)

class FernDetailsSerializer(CustomModelSerializerMixin, BaseDetailsSerializer):
    disturbance_type = DisturbanceTypeSerializer(required=False)
    earthworm_evidence = EarthwormEvidenceSerializer(required=False)
    #lifestages = FernLifestages(required=False) # FIXME
    class Meta:
        model = models.FernDetails
        exclude = ('id',)

class FloweringPlantDetailsSerializer(CustomModelSerializerMixin, BaseDetailsSerializer):
    disturbance_type = DisturbanceTypeSerializer(required=False)
    earthworm_evidence = EarthwormEvidenceSerializer(required=False)
    #lifestages = FloweringPlantLifestages(required=False) # FIXME
    class Meta:
        model = models.FloweringPlantDetails
        exclude = ('id',)
    
class MossDetailsSerializer(CustomModelSerializerMixin, BaseDetailsSerializer):
    disturbance_type = DisturbanceTypeSerializer(required=False)
    earthworm_evidence = EarthwormEvidenceSerializer(required=False)
    #lifestages = MossLifestages(required=False) # FIXME
    class Meta:
        model = models.MossDetails
        exclude = ('id',)


class SlimeMoldLifestagesSerializer(CustomModelSerializerMixin,
                                    serializers.ModelSerializer):
    class Meta:
        model = models.SlimeMoldLifestages
        exclude = ('id',)

class SlimeMoldDetailsSerializer(CustomModelSerializerMixin, BaseDetailsSerializer):
    lifestages = SlimeMoldLifestagesSerializer(required=False)
    class Meta:
        model = models.SlimeMoldDetails
        exclude = ('id',)

class FruitingBodiesAgeSerializer(CustomModelSerializerMixin,
                                  serializers.ModelSerializer):
    class Meta:
        model = models.FruitingBodiesAge
        exclude = ('id',)

class ObservedAssociationsSerializer(CustomModelSerializerMixin,
                                     serializers.ModelSerializer):
    class Meta:
        model = models.ObservedAssociations
        exclude = ('id',)
    
class FungusDetailsSerializer(CustomModelSerializerMixin, BaseDetailsSerializer):
    disturbance_type = DisturbanceTypeSerializer(required=False)
    earthworm_evidence = EarthwormEvidenceSerializer(required=False)
    fruiting_bodies_age = FruitingBodiesAgeSerializer(required=False)
    other_observed_associations = ObservedAssociationsSerializer(required=False)
    class Meta:
        model = models.FungusDetails
        exclude = ('id',)


""" --------------------------------------------
PHOTOGRAPHS
------------------------------------------------ """

class PhotographPublishSerializer(serializers.Serializer):
    """
    Used to publish new photographs
    """ 
    image = serializers.ListField(
        child=rest_fields.ImageField(max_length=1000,
            allow_empty_file=False,
            use_url=True))
    id = rest_fields.IntegerField(required=False, read_only=True)
    thumbnail = rest_fields.CharField(required=False, read_only=True)
    description = rest_fields.CharField(required=False, allow_blank=True)
    notes = rest_fields.CharField(required=False, allow_blank=True)
               
    class Meta:
        model = models.Photograph
        fields = ('image', 'featuretype', 'occurrence_fk')

    def to_representation(self, instance):
        return instance


    def create(self, validated_data):
        image=validated_data.pop('image')
        image_list = []
        for img in image:
            photo = models.Photograph.objects.create(image=img, **validated_data)
            img_desc = {
                'image': photo.image.url,
                'id': photo.id
                }
            if photo.thumbnail:
                img_desc['thumbnail'] = photo.thumbnail.url
            image_list.append(img_desc)
        return {'images': image_list}

class PhotographSerializer(serializers.ModelSerializer):
    """
    Used to list photographs
    """
    class Meta:
        model = models.Photograph
        fields = '__all__'
        read_only_fields = ('image', 'thumbnail', 'image_width', 'image_height','thumb_width', 'thumb_height', 'date')
        #exclude = ('occurrence_fk', 'occurrence', 'content_type') 

""" -------------------------------------------
OCCURRENCE SERIALIZER
---------------------------------------------- """
class OccurrenceSerializer(UpdateOccurrenceMixin, serializers.Serializer):
    """
    Manages serialization/deserialization of Occurrences
    """
    id = rest_fields.IntegerField(required=False, read_only=True)
    featuretype = rest_fields.CharField(required=False, read_only=True)
    featuresubtype = rest_fields.CharField(read_only=True)
    released = rest_fields.NullBooleanField(required=False, read_only=False)
    verified = rest_fields.NullBooleanField(required=False, read_only=False)
    version = rest_fields.IntegerField(required=False, read_only=True)
    total_versions = TotalVersionsField(required=False, read_only=True)
    inclusion_date = rest_fields.DateTimeField(required=False, read_only=True)
    version_date = rest_fields.DateTimeField(required=False, read_only=True)
    geom = gisserializer.GeometryField(required=False)
    polygon = gisserializer.GeometryField(required=False)
    observation = OccurrenceObservationSerializer(required=True)
    images = PhotographSerializer(required=False, many=True)
    
    def get_fields(self):
        fields = serializers.Serializer.get_fields(self)
        
        if self.instance and self.instance.occurrence_cat:
            self.featuresubtype = self.instance.occurrence_cat.code
        
        fields['details'] = get_details_serializer(self.featuresubtype)(required=False)
        return fields
    
    def to_representation(self, instance):
        if isinstance(instance, models.OccurrenceTaxon):
            details_name = instance.get_details_class().__name__.lower()
            setattr(instance, details_name, instance.get_details())
        r = serializers.Serializer.to_representation(self, instance)

        result = to_flat_representation(r)
        result["id"] = r["id"]
        
        if self.is_writer or self.is_publisher:
            result["version"] = instance.version
            result["total_versions"] = instance.version
        else:
            result["version"] = instance.released_versions
            result["total_versions"] = instance.released_versions
        result['featuretype'] = instance.occurrence_cat.main_cat
        result['featuresubtype'] = instance.occurrence_cat.code
        result['version_date'] = instance.inclusion_date
        photo_serializer = PhotographSerializer(instance.photographs, many=True)
        result['images'] = photo_serializer.data
        result['is_writer'] = self.is_writer
        result['is_publisher'] = self.is_publisher
        result['geom'] = instance.geom.geojson
        if instance.location and isinstance(instance.location.polygon, Polygon):
            result['polygon'] = instance.location.polygon.geojson
        return result
    
    def to_nested_representation(self, data):
        formvalues = OrderedDict()
        for global_field_name in data: # transform the flat object to a set of dictionaries of forms
            field_parts = global_field_name.split(".")
            if len(field_parts)>1:
                base = formvalues
                for local_field_name in field_parts[:-1]:
                    base[local_field_name] = base.get(local_field_name, {})
                    if base[local_field_name] is None:
                        base[local_field_name] = {}
                    base = base[local_field_name]
                if not (isinstance(base.get(field_parts[-1]), dict) and data[global_field_name] is None):  # avoid overwritting new values with old empty forms
                    base[field_parts[-1]] = data[global_field_name]
            else:
                if not (isinstance(formvalues.get(global_field_name), dict) and data[global_field_name] is None): # avoid overwritting new values with old empty forms 
                    formvalues[global_field_name] = data[global_field_name]
        return formvalues
    
    def to_internal_value(self, data):
        
        """
        Dict of native values <- Dict of primitive datatypes.
        """
        if not isinstance(data, Mapping):
            message = self.error_messages['invalid'].format(
                datatype=type(data).__name__
            )
            raise rest_fields.ValidationError({
                rest_fields.api_settings.NON_FIELD_ERRORS_KEY: [message]
            }, code='invalid')

        validated_formvalues = OrderedDict()
        errors = OrderedDict()
        self.featuresubtype = data.get("featuresubtype")
        self.to_internal_value_extra(data, validated_formvalues, errors)
        
        fields = self._writable_fields
        
        # transform the flat object to a set of dictionaries of forms
        formvalues = self.to_nested_representation(data)

        for field in fields: # validate values
            validate_method = getattr(self, 'validate_' + field.field_name, None)
            if isinstance(field, serializers.ModelSerializer):
                primitive_value = field.get_value(formvalues)
                if check_all_null(primitive_value) and not field.required:
                    continue
            else:
                primitive_value = field.get_value(formvalues)
            try:
                validated_value = field.run_validation(primitive_value)
                if validate_method is not None:
                    validated_value = validate_method(validated_value)
            except rest_fields.ValidationError as exc:
                errors[field.field_name] = exc.detail
            except rest_fields.DjangoValidationError as exc:
                errors[field.field_name] = rest_fields.get_error_detail(exc)
            except rest_fields.SkipField:
                pass
            else:
                rest_fields.set_value(validated_formvalues, field.source_attrs, validated_value)

        validated_formvalues["released"] = data.get("released", False)
        validated_formvalues["verified"] = data.get("verified", False)
        validated_formvalues['featuretype'] = data.get("featuretype")
        validated_formvalues['featuresubtype'] = data.get("featuresubtype")
        validated_formvalues['images'] = formvalues.get('images')
            
        if isinstance(validated_formvalues.get('polygon'), Polygon):
            location = validated_formvalues.get('location', {})
            location['polygon'] = validated_formvalues.pop('polygon')
            validated_formvalues['location'] = location
        
        try:
            geom_serializer = gisserializer.GeometryField()
            validated_formvalues['geom'] = geom_serializer.to_internal_value(data.get("geom"))
        except:
            if not data.get('id'):
                errors["geom"] = [_("Geometry is missing")]

        if errors:
            raise rest_fields.ValidationError(to_flat_representation(errors))

        return validated_formvalues

class TaxonLocationSerializer(CustomModelSerializerMixin,
                              serializers.ModelSerializer):
    class Meta:
        model = models.TaxonLocation
        exclude = ('id', 'polygon')

class NaturalAreaElementSerializer(CustomModelSerializerMixin,
                                   serializers.ModelSerializer):
    disturbance_type = DisturbanceTypeSerializer(required=False)
    earthworm_evidence = EarthwormEvidenceSerializer(required=False)
    #lifestages = MossLifestages(required=False) # FIXME
    class Meta:
        model = models.ElementNaturalAreas
        exclude = ('id',)

class NaturalAreaLocationSerializer(CustomModelSerializerMixin,
                                    serializers.ModelSerializer):
    class Meta:
        model = models.NaturalAreaLocation
        exclude = ('id', 'polygon')

class TaxonOccurrenceSerializer(OccurrenceSerializer):
    species = SpeciesSerializer(required=False)
    voucher = VoucherSerializer(required=False)
    location = TaxonLocationSerializer(required=False)
    
    def to_internal_value_extra(self, data, result, errors):
        species_id = data.get('species.id')
        if not species_id:
            errors["species"] = [_("No species was selected")]

class NaturalAreaOccurrenceSerializer(OccurrenceSerializer):
    element = NaturalAreaElementSerializer(required=False)
    location = NaturalAreaLocationSerializer(required=False)
    
    def to_internal_value_extra(self, data, result, errors):
        pass

""" -------------------------------------------
LAYERS
---------------------------------------------- """

class LayerSerializer(gisserializer.GeoFeatureModelSerializer):
    id = rest_fields.IntegerField(required=False, read_only=True)
    featuretype = rest_fields.CharField(required=False, read_only=True)
    featuresubtype = rest_fields.CharField()
    released = rest_fields.BooleanField(required=False, read_only=True)
    inclusion_date = rest_fields.DateTimeField(required=False, read_only=True)
    verified = rest_fields.BooleanField(required=False, read_only=True)
    version = rest_fields.IntegerField(required=False, read_only=True)
    total_versions = rest_fields.IntegerField(required=False, read_only=True)
    
    def __init__(self, *args, **kwargs):
        self.is_writer_or_publisher = kwargs.pop('is_writer_or_publisher', False)
        super(LayerSerializer, self).__init__(*args, **kwargs)
    
    def get_properties(self, instance, fields):
        result = {}
        if self.is_writer_or_publisher:
            result['total_versions'] = instance.version
        else:
            result['total_versions'] = instance.released_versions
        result['version'] = instance.version
        result['featuretype'] = instance.occurrence_cat.main_cat
        result['featuresubtype'] = instance.occurrence_cat.code
        result['released'] = instance.released
        result['verified'] = instance.verified
        result['inclusion_date'] = instance.inclusion_date
        result['id'] = instance.id
        return result
    
    class Meta:
        model = models.OccurrenceTaxon
        geo_field = "geom"
        fields = ('id', 'featuretype', 'featuresubtype', 'inclusion_date', 'released', 'verified', 'version', 'total_versions')

class ListSerializer(gisserializer.GeoFeatureModelSerializer):
    id = rest_fields.IntegerField(required=False, read_only=True)
    featuretype = rest_fields.CharField(required=False, read_only=True)
    featuresubtype = rest_fields.CharField()
    released = rest_fields.BooleanField(required=False, read_only=True)
    inclusion_date = rest_fields.DateTimeField(required=False, read_only=True)
    verified = rest_fields.BooleanField(required=False, read_only=True)
    version = rest_fields.IntegerField(required=False, read_only=True)
    total_versions = rest_fields.IntegerField(required=False, read_only=True)
    
    def __init__(self, *args, **kwargs):
        self.is_writer_or_publisher = kwargs.pop('is_writer_or_publisher', False)
        super(ListSerializer, self).__init__(*args, **kwargs)
    
    
    class Meta:
        model = models.OccurrenceTaxon
        geo_field = "geom"
        fields = ('id', 'featuretype', 'featuresubtype', 'inclusion_date', 'released', 'verified', 'version', 'total_versions')


class TaxonListSerializer(ListSerializer):    
    def get_properties(self, instance, fields):
        result = {}
        if self.is_writer_or_publisher:
            result['total_versions'] = instance.version
        else:
            result['total_versions'] = instance.released_versions
        result['version'] = instance.version
        result['featuretype'] = instance.occurrence_cat.main_cat
        result['featuresubtype'] = instance.occurrence_cat.code
        result['released'] = instance.released
        result['verified'] = instance.verified
        result['inclusion_date'] = instance.inclusion_date
        result['id'] = instance.id
        result['species.id'] = instance.species.id
        result['species.first_common'] = instance.species.first_common
        result['species.name_sci'] = instance.species.name_sci
        result['observation.observation_date'] = instance.observation.observation_date
        return result


class NaturalAreaListSerializer(ListSerializer):    
    def get_properties(self, instance, fields):
        result = {}
        if self.is_writer_or_publisher:
            result['total_versions'] = instance.version
        else:
            result['total_versions'] = instance.released_versions
        result['version'] = instance.version
        result['featuretype'] = instance.occurrence_cat.main_cat
        result['featuresubtype'] = instance.occurrence_cat.code
        result['released'] = instance.released
        result['verified'] = instance.verified
        result['inclusion_date'] = instance.inclusion_date
        result['id'] = instance.id
        if instance.element:
            result['element.id'] = instance.element.id
            result['element.general_description'] = instance.element.general_description
            result['element.type'] = instance.element.type
            result['element.natural_area_code_nac'] = instance.element.natural_area_code_nac
        result['observation.observation_date'] = instance.observation.observation_date
        return result

""" -------------------------------------------
FEATURE TYPES
---------------------------------------------- """
class FeatureTypeSerializer():
    def __init__(self, occurrence_cat, is_writer=False, is_publisher=False):
        self.is_writer = is_writer
        self.is_publisher = is_publisher
        self.occurrence_cat = occurrence_cat
        if occurrence_cat:
            init_forms(self, occurrence_cat.code)
    
    def get_feature_type(self):
        result = {}
        result['featuretype'] = self.occurrence_cat.main_cat
        result['featuresubtype'] = self.occurrence_cat.code
        forms = []
        for formdef in self.forms:
            form = {}
            form_name = formdef[0]
            form['formlabel'] = _(form_name)
            form['formname'] = form_name
            if 'species' == form_name:
                form['formitems'] = self.get_form_featuretype(form_name, formdef[1], SpeciesSerializer())
            elif 'species.element_species' == form_name:
                form['formitems'] = self.get_form_featuretype(form_name, formdef[1], ElementSpeciesSerializer())
            elif form_name != MANAGEMENT_FORM_NAME:
                form['formitems'] = self.get_form_featuretype(form_name, formdef[1])
            else:
                if self.is_publisher:
                    form['formitems'] = MANAGEMENT_FORM_ITEMS_PUBLISHER
                else:
                    form['formitems'] = MANAGEMENT_FORM_ITEMS
            forms.append(form)
        result['forms'] = forms
        return result

    def get_form_featuretype(self, form_name, model, model_serializer=None):
        fields = model._meta.get_fields()
        model_fields = model_serializer.get_fields() if model_serializer else {}
        result = []
        for f in fields:
            fdef = {}

            if getattr(f, 'primary_key', False):
                pass
                #fdef['type'] = 'pk'
            elif isinstance(f, CharField) or isinstance(f, TextField):
                fdef['type'] = 'string'
            elif isinstance(f, BooleanField):
                fdef['type'] = 'boolean'
            elif isinstance(f, NullBooleanField):
                fdef['type'] = 'boolean'
            elif isinstance(f, DateTimeField):
                fdef['type'] = 'datetime'
            elif isinstance(f, DateField):
                fdef['type'] = 'date'
            elif isinstance(f, GeometryField):
                # skip geoms
                pass
            elif isinstance(f, FloatField) or isinstance(f, DecimalField):
                fdef['type'] = 'double'
            elif isinstance(f, IntegerField):
                fdef['type'] = 'integer'
            elif getattr(f, 'related_model', False):
                if issubclass(f.related_model, models.DictionaryTable) or issubclass(f.related_model, models.DictionaryTableExtended):
                    fdef['type'] = 'stringcombo'
                    items = []
                    for item in f.related_model.objects.all():
                        idef = {}
                        idef['key'] = item.code
                        idef['value'] = item.name
                        items.append(idef)
                    fdef['values'] = {'items': items}
                else:
                    #fdef['type'] = 'fk'
                    pass
                
            if 'type' in fdef:
                mfield = model_fields.get(f.name)
                if mfield:
                    fdef['readonly'] = getattr(mfield, "read_only", False)
                    fdef['mandatory'] = (not getattr(mfield, "allo_null", True) and not getattr(mfield, "allow_blank", True))
                else:
                    fdef['mandatory'] = (not getattr(f, "null", True) and not getattr(f, "blank", True))
                if not (self.is_writer or self.is_publisher):
                    fdef['readonly'] = True
                fdef['key'] = form_name + "." + f.name
                fdef['label'] = _(f.name)
                result.append(fdef)
        return result

class OccurrenceVersionSerializer():
    def is_related_field(self, f):
        if not getattr(f, 'related_model', False):
            return False
        if getattr(f, 'auto_created', False):
            return False
        return True
    
    def is_dict_model(self, related_model):
        if issubclass(related_model, models.DictionaryTable):
            return True
        if issubclass(related_model, models.DictionaryTableExtended):
            return True
        return False
    
    def get_related_fields(self, model_meta):
        rel_fields = []
        for f in model_meta.get_fields():
            if self.is_related_field(f):
                rel_fields.append((f.name, f.attname, f.related_model))
        return rel_fields
    
    def add_related_values(self, obj_dict, model_meta, revision_date):
        for (rel_field_name, rel_attname, rel_field_model) in self.get_related_fields(model_meta):
            rel_id = obj_dict.get(rel_attname)
            rel_field_model = self.get_instance_model(obj_dict, rel_field_model)
            if rel_id is None:
                obj_dict[rel_field_name] = None
            elif self.is_dict_model(rel_field_model):
                obj_dict[rel_field_name] = rel_field_model.objects.get(pk=rel_id).code
            else:
                obj_dict[rel_field_name] = self.get_version_from_model(rel_field_model, rel_id, revision_date)
            del obj_dict[rel_attname]
        return obj_dict
        
    def get_version_from_model(self, model, id, revision_date):
        obj_versions = Version.objects.get_for_object_reference(model, id).filter(revision__date_created__lte=revision_date)
        if len(obj_versions)>0: 
        #try:
            requested_version = obj_versions[0]
            requested_obj = requested_version.field_dict
            return self.add_related_values(requested_obj, model._meta, revision_date)
        #except:
        #    pass
    
    def get_instance_model(self, parent_instance, model):
        if issubclass(model, models.TaxonDetails):
            category_code = parent_instance.get('occurrence_cat')
            category = models.OccurrenceCategory.objects.get(code=category_code)
            return models.get_details_class(category.code)
        return model 
    
    def get_images(self, requested_version):
        versioned_photos = []
        for version in requested_version.revision.version_set.all():
            if isinstance(version._object_version.object, models.Photograph):
                versioned_photos.append(version._object_version.object)
                
        photo_serializer = PhotographSerializer(versioned_photos, many=True)
        return photo_serializer.data
        
    
    def get_version(self, instance, version, exclude_unreleased=False):
        """
        Gets a dict representing a particular version of the occurrence
        
        instance: an instance of the last version of the occurrence
        version: the requested version 
        """
        versions = Version.objects.get_for_object(instance)
        if exclude_unreleased:
            total_versions = instance.released_versions
            num_released_version = total_versions
            for v in versions:
                if v.field_dict.get('released', False):
                    if num_released_version != version:
                        num_released_version = num_released_version - 1
                    else:
                        requested_version = v
                        break
        else:
            total_versions = instance.version
            version_internal = total_versions - version
            requested_version = versions[version_internal]

        revision_date = requested_version.revision.date_created
        
        result = self.add_related_values(requested_version.field_dict, instance._meta, revision_date)
        if result.get('location') and isinstance(result.get('location').get('polygon'), Polygon):
            result['polygon'] = result.get('location').pop('polygon').geojson
        result['geom'] = {'type': 'Point', 'coordinates': result['geom'].coords}
        
        images = self.get_images(requested_version)
        result['images'] = images
        result['total_versions'] = total_versions
        result['version'] = version
        result['version_date'] = revision_date
        return to_flat_representation(result)

""" -------------------------------------------
SPECIES SEARCH
---------------------------------------------- """
class SpeciesSearchSerializer(serializers.ModelSerializer):
    name = rest_fields.SerializerMethodField()

    def get_name(self, obj):
        return '{} - {}'.format(obj.first_common, obj.name_sci) 
    
    class Meta:
        model = models.Species
        fields = ('id', 'name')

class SpeciesSearchResultSerializer(serializers.ModelSerializer):
    element_species = ElementSpeciesSerializer(required=False)
    
    class Meta:
        model = models.Species
        fields = "__all__"
        
    def to_representation(self, instance):
        r = super(SpeciesSearchResultSerializer, self).to_representation(instance)
        return to_flat_representation(r, 'species')


class OccurrenceAggregatorSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        filterer = self.context["filterer"]
        result = {
            "total_occurrences": 0,
            "title": self.context.get("title", ""),
            "items": [],
        }
        year = filterer.get_field_by_name("year")
        if year.value is not None:
            result["year"] = year.value
        if filterer.split_by_month:
            entries = self.group_months(
                instance,
                filterer.get_field_by_name(filterer.aggregate_by).lookup,
            )
        else:
            entries = instance
        for entry in entries:
            item = {}
            for lookup, value in entry.iteritems():
                if lookup == "num_occurrences":
                    item["occurrences"] = value
                    result["total_occurrences"] += value
                elif lookup == "months":
                    item["months"] = value
                    result["total_occurrences"] += sum(value.values())
                else:
                    field = filterer.get_field_by_lookup(lookup)
                    item[field.name] = value
            result["items"].append(item)
        return result

    def group_months(self, entries, entry_id_key):
        grouped_entries = {}
        initial_months = [  # here we care about months, year is irrelevant
            (date(dt.datetime(2000, i, 1), "F"), 0) for i in range(1, 13)]
        for entry in entries:
            entry_id = entry[entry_id_key]
            new_entry = grouped_entries.setdefault(
                entry_id, {"months": OrderedDict(initial_months)})
            month_name = date(entry["month"], "F")
            new_entry["months"][month_name] = entry["num_occurrences"]
            for k, v in entry.items():
                if k not in ("month", "num_occurrences"):
                    new_entry[k] = v
        return grouped_entries.values()
