from collections import Mapping
from collections import OrderedDict
import datetime as dt
import importlib
import logging

from django.db import models as django_models
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
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.gis.geos import Polygon
from django.contrib.gis.db.models.fields import GeometryField
from django.contrib.gis.db.models.fields import PolygonField
from django.contrib.postgres.fields import JSONField
from django.template.defaultfilters import date
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework import fields as rest_fields
from rest_framework_gis import serializers as gisserializer
import reversion
from reversion.models import Version
from rest_framework.exceptions import ValidationError
import yaml

from . import models

logger = logging.getLogger(__name__)


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


def get_field_values(instance, field, form_validated_data):
    if isinstance(field, (CharField, TextField)):
        old_value =  getattr(instance, field.name, '')
        new_value = form_validated_data.get(field.name, '')
    elif isinstance(field, (DateTimeField, DateField)):
        old_value =  getattr(instance, field.name, None)
        new_value = form_validated_data.get(field.name, '')
    elif isinstance(field, (BooleanField, NullBooleanField, FloatField,
                            DecimalField, IntegerField)):
        old_value =  getattr(instance, field.name, None)
        new_value = form_validated_data.get(field.name)
    elif isinstance(field, PolygonField):
        old_value =  getattr(instance, field.name, None)
        new_value = form_validated_data.get(field.name)
    elif isinstance(field, JSONField):
        old_value = getattr(instance, field.name, None)
        new_value = form_validated_data.get(field.name)
    else:
        old_value = getattr(instance, field.name, None)
        new_value = getattr(instance, field.name, None)
    return old_value, new_value


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


def _flatten_notes_representation(nested_representation):
    result = {}
    for note in nested_representation:
        key = "notes.note.{}".format(note["ui_tab"])
        result[key] = note["note"]
    return result


def get_sub_category_serializer(subcategory_code):
    """Return the relevant serializer class for the input subcategory"""
    return {
        "co": ConiferDetailsSerializer,
        "fe": FernDetailsSerializer,
        "fl": FloweringPlantDetailsSerializer,
        "fu": FungusDetailsSerializer,
        "lk": PondLakeAnimalDetailsSerializer,
        "ln": LandAnimalDetailsSerializer,
        "mo": MossDetailsSerializer,
        "na": NaturalAreaElementSerializer,
        "sl": SlimeMoldDetailsSerializer,
        "st": StreamAnimalDetailsSerializer,
        "we": WetlandAnimalDetailsSerializer,
    }.get(subcategory_code)


def is_deletable_field(f):
    if not getattr(f, 'related_model', False):
        return False
    if getattr(f, 'auto_created', False):
        return False
    if issubclass(f.related_model, models.DictionaryTable):
        return False
    if issubclass(f.related_model, models.DictionaryTableExtended):
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


def validate_json_field(values, model_class, model_field_name):
    """Perform validation on a JSONField

    This function chacks that the input values are legal, according to the
    defined json field mappings. Since we are using JSONFields in order to
    emulate a many-to-many relation from a model to another
    ``models.DictionaryTable`` model, it is necessary to enforce validation
    explicitly, by querying the related model and checking if all of the
    values in the input ``values`` iterable are there.

    Parameters
    ----------
    values: list
        An iterable with the values that are to be validated
    model_class: django.db.models.Model
        Model in which the JSONField has been defined
    model_field_name: str
        Name of the JSONField being validated

    Raises
    ------
    serializers.ValidationError:
        When there are illegal values

    """

    choices = models.get_jsonfield_validation_choices(
        model_class, model_field_name)
    errors = []
    for item in values or []:
        if item not in choices:
            errors.append("Invalid value {!r}".format(item))
    if any(errors):
        raise serializers.ValidationError(", ".join(errors))
    return values


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


class OccurrenceRelatedObjectSerialzer(serializers.Serializer):
    def __init__(self, instance=None, data=rest_fields.empty, model=None, **kwargs):
        self._model = model
        serializers.Serializer.__init__(self, instance=instance, data=data, **kwargs)


class CustomModelSerializerMixin(object):
    """
    Used by most of our model serializers to properly manage dictionaries and
    to ignore empty forms when they are not required

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


class VoucherSerializer(CustomModelSerializerMixin,
                        serializers.ModelSerializer):

    def validate_preservative(self, value):
        return validate_json_field(value, models.Voucher, "preservative")

    def validate_storage(self, value):
        return validate_json_field(value, models.Voucher, "storage")

    class Meta:
        model = models.Voucher
        exclude = ('id',)


# class ElementSpeciesSerializer(CustomModelSerializerMixin,
#                                serializers.ModelSerializer):
#     class Meta:
#         model = models.ElementSpecies
#         exclude = ('id',)


class TaxonListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Taxon
        fields = (
            "url",
            "tsn",
            "name",
            "rank",
            "kingdom",
        )


class TaxonDetailSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        """Serialize the instance

        In addition to the fields defined in Meta.fields this will include
        also the upper taxonomic ranks in a flat structure

        """

        result = OrderedDict()
        for field_name in self.fields:
            result[field_name] = getattr(instance, field_name)
        for rank in instance.upper_ranks:
            result[rank["rank"].lower()] = rank["name"]
        result[instance.rank.lower()] = instance.name
        return result

    class Meta:
        model = models.Taxon
        fields = (
            "tsn",
            "name",
            "common_names",
            "rank",
            "native",
            "leap_concern",
            "oh_status",
            "usfws_status",
            "iucn_red_list_category",
            "other_code",
            "ibp_english",
            "ibp_scientific",
            "bblab_number",
            "nrcs_usda_symbol",
            "synonym_nrcs_usda_symbol",
            "epa_numeric_code",
        )
        read_only_fields = (
            "tsn",
            "name",
            "common_names",
            "rank",
            "native",
            "leap_concern",
            "oh_status",
            "usfws_status",
            "iucn_red_list_category",
            "other_code",
            "ibp_english",
            "ibp_scientific",
            "bblab_number",
            "nrcs_usda_symbol",
            "synonym_nrcs_usda_symbol",
            "epa_numeric_code",
        )


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

    def validate_record_origin(self, value):
        return validate_json_field(
            value, models.OccurrenceObservation, "record_origin")

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

    def validate_marks(self, value):
        return validate_json_field(value, models.AnimalDetails, "marks")

    def validate_gender(self, value):
        return validate_json_field(value, models.AnimalDetails, "gender")

    def validate_diseases_and_abnormalities(self, value):
        return validate_json_field(
            value, models.AnimalDetails, "diseases_and_abnormalities")

    def validate_sampler(self, value):
        return validate_json_field(
            value, models.LandAnimalDetails, "sampler")

    def validate_stratum(self, value):
        return validate_json_field(
            value, models.LandAnimalDetails, "stratum")

    class Meta:
        model = models.LandAnimalDetails
        exclude = ('id',)


class WetlandVetegationStructureSerializer(CustomModelSerializerMixin,
                                           serializers.ModelSerializer):

    class Meta:
        model = models.WetlandVetegationStructure
        exclude = ('id',)


class WetlandAnimalDetailsSerializer(CustomModelSerializerMixin,
                                     BaseDetailsSerializer):
    lifestages = AnimalLifestagesSerializer(required=False)
    vegetation = WetlandVetegationStructureSerializer(required=False)

    def validate_sampler(self, value):
        return validate_json_field(
            value, models.AquaticAnimalDetails, "sampler")

    def validate_water_source(self, value):
        return validate_json_field(
            value, models.WetlandAnimalDetails, "water_source")

    def validate_habitat_feature(self, value):
        return validate_json_field(
            value, models.WetlandAnimalDetails, "habitat_feature")

    def validate_wetland_type(self, value):
        return validate_json_field(
            value, models.WetlandAnimalDetails, "wetland_type")

    class Meta:
        model = models.WetlandAnimalDetails
        exclude = ('id',)


class StreamSubstrateSerializer(CustomModelSerializerMixin,
                                serializers.ModelSerializer):
    class Meta:
        model = models.StreamSubstrate
        exclude = ('id',)


class StreamAnimalDetailsSerializer(CustomModelSerializerMixin,
                                    BaseDetailsSerializer):
    lifestages = AnimalLifestagesSerializer(required=False)
    substrate = StreamSubstrateSerializer(required=False)

    def validate_sampler(self, value):
        return validate_json_field(
            value, models.AquaticAnimalDetails, "sampler")

    def validate_channel_type(self, value):
        return validate_json_field(
            value, models.StreamAnimalDetails, "channel_type")

    def validate_hmfei_local_abundance(self, value):
        return validate_json_field(
            value, models.StreamAnimalDetails, "hmfei_local_abundance")

    def validate_lotic_habitat_type(self, value):
        return validate_json_field(
            value, models.StreamAnimalDetails, "lotic_habitat_type")

    class Meta:
        model = models.StreamAnimalDetails
        exclude = ('id',)


class PondLakeAnimalDetailsSerializer(CustomModelSerializerMixin,
                                      BaseDetailsSerializer):
    lifestages = AnimalLifestagesSerializer(required=False)

    def validate_sampler(self, value):
        return validate_json_field(
            value, models.AquaticAnimalDetails, "sampler")

    def validate_microhabitat(self, value):
        return validate_json_field(
            value, models.PondLakeAnimalDetails, "microhabitat")

    def validate_pond_lake_use(self, value):
        return validate_json_field(
            value, models.PondLakeAnimalDetails, "pond_lake_use")

    def validate_shoreline_type(self, value):
        return validate_json_field(
            value, models.PondLakeAnimalDetails, "shoreline_type")

    class Meta:
        model = models.PondLakeAnimalDetails
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
    disturbance_type = DisturbanceTypeSerializer(required=False)
    earthworm_evidence = EarthwormEvidenceSerializer(required=False)

    def validate_aspect(self, value):
        return validate_json_field(
            value, models.PlantDetails, "aspect")

    def validate_general_habitat_category(self, value):
        return validate_json_field(
            value, models.PlantDetails, "general_habitat_category")

    def validate_ground_surface(self, value):
        return validate_json_field(
            value, models.PlantDetails, "ground_surface")

    def validate_landscape_position(self, value):
        return validate_json_field(
            value, models.PlantDetails, "landscape_position")

    def validate_lifestages(self, value):
        return validate_json_field(
            value, models.ConiferDetails, "lifestages")

    def validate_moisture_regime(self, value):
        return validate_json_field(
            value, models.PlantDetails, "moisture_regime")

    def validate_slope(self, value):
        return validate_json_field(
            value, models.PlantDetails, "slope")

    class Meta:
        model = models.ConiferDetails
        exclude = ('id',)


class FernDetailsSerializer(CustomModelSerializerMixin, BaseDetailsSerializer):
    disturbance_type = DisturbanceTypeSerializer(required=False)
    earthworm_evidence = EarthwormEvidenceSerializer(required=False)
    #lifestages = FernLifestages(required=False) # FIXME

    def validate_aspect(self, value):
        return validate_json_field(
            value, models.PlantDetails, "aspect")

    def validate_lifestages(self, value):
        return validate_json_field(
            value, models.FernDetails, "lifestages")

    def validate_general_habitat_category(self, value):
        return validate_json_field(
            value, models.PlantDetails, "general_habitat_category")

    def validate_ground_surface(self, value):
        return validate_json_field(
            value, models.PlantDetails, "ground_surface")

    def validate_landscape_position(self, value):
        return validate_json_field(
            value, models.PlantDetails, "landscape_position")

    def validate_moisture_regime(self, value):
        return validate_json_field(
            value, models.PlantDetails, "moisture_regime")

    def validate_slope(self, value):
        return validate_json_field(
            value, models.PlantDetails, "slope")

    class Meta:
        model = models.FernDetails
        exclude = ('id',)


class FloweringPlantDetailsSerializer(CustomModelSerializerMixin, BaseDetailsSerializer):
    disturbance_type = DisturbanceTypeSerializer(required=False)
    earthworm_evidence = EarthwormEvidenceSerializer(required=False)
    #lifestages = FloweringPlantLifestages(required=False) # FIXME

    def validate_aspect(self, value):
        return validate_json_field(
            value, models.PlantDetails, "aspect")

    def validate_lifestages(self, value):
        return validate_json_field(
            value, models.FloweringPlantDetails, "lifestages")

    def validate_general_habitat_category(self, value):
        return validate_json_field(
            value, models.PlantDetails, "general_habitat_category")

    def validate_ground_surface(self, value):
        return validate_json_field(
            value, models.PlantDetails, "ground_surface")

    def validate_landscape_position(self, value):
        return validate_json_field(
            value, models.PlantDetails, "landscape_position")

    def validate_moisture_regime(self, value):
        return validate_json_field(
            value, models.PlantDetails, "moisture_regime")

    def validate_slope(self, value):
        return validate_json_field(
            value, models.PlantDetails, "slope")

    class Meta:
        model = models.FloweringPlantDetails
        exclude = ('id',)


class MossDetailsSerializer(CustomModelSerializerMixin, BaseDetailsSerializer):
    disturbance_type = DisturbanceTypeSerializer(required=False)
    earthworm_evidence = EarthwormEvidenceSerializer(required=False)
    #lifestages = MossLifestages(required=False) # FIXME

    def validate_aspect(self, value):
        return validate_json_field(
            value, models.PlantDetails, "aspect")

    def validate_lifestages(self, value):
        return validate_json_field(
            value, models.MossDetails, "lifestages")

    def validate_general_habitat_category(self, value):
        return validate_json_field(
            value, models.PlantDetails, "general_habitat_category")

    def validate_ground_surface(self, value):
        return validate_json_field(
            value, models.PlantDetails, "ground_surface")

    def validate_landscape_position(self, value):
        return validate_json_field(
            value, models.PlantDetails, "landscape_position")

    def validate_moisture_regime(self, value):
        return validate_json_field(
            value, models.PlantDetails, "moisture_regime")

    def validate_slope(self, value):
        return validate_json_field(
            value, models.PlantDetails, "slope")

    class Meta:
        model = models.MossDetails
        exclude = ('id',)


class SlimeMoldLifestagesSerializer(CustomModelSerializerMixin,
                                    serializers.ModelSerializer):
    class Meta:
        model = models.SlimeMoldLifestages
        exclude = ('id',)


class SlimeMoldDetailsSerializer(CustomModelSerializerMixin,
                                 BaseDetailsSerializer):
    lifestages = SlimeMoldLifestagesSerializer(required=False)

    class Meta:
        model = models.SlimeMoldDetails
        exclude = ('id',)

    def validate_slime_mold_class(self, value):
        return validate_json_field(
            value, models.SlimeMoldDetails, "slime_mold_class")

    def validate_slime_mold_media(self, value):
        return validate_json_field(
            value, models.SlimeMoldDetails, "slime_mold_media")


class FruitingBodiesAgeSerializer(CustomModelSerializerMixin,
                                  serializers.ModelSerializer):
    class Meta:
        model = models.FruitingBodiesAge
        exclude = ('id',)


class ObservedAssociationsSerializer(CustomModelSerializerMixin,
                                     serializers.ModelSerializer):

    def validate_gnat_association(self, value):
        return validate_json_field(
            value, models.ObservedAssociations, "gnat_association")

    def validate_ants_association(self, value):
        return validate_json_field(
            value, models.ObservedAssociations, "ants_association")

    def validate_termite_association(self, value):
        return validate_json_field(
            value, models.ObservedAssociations, "termite_association")

    def validate_beetles_association(self, value):
        return validate_json_field(
            value, models.ObservedAssociations, "beetles_association")

    def validate_snow_flea_association(self, value):
        return validate_json_field(
            value, models.ObservedAssociations, "snow_flea_association")

    def validate_slug_association(self, value):
        return validate_json_field(
            value, models.ObservedAssociations, "slug_association")

    def validate_snail_association(self, value):
        return validate_json_field(
            value, models.ObservedAssociations, "snail_association")

    def validate_skunk_association(self, value):
        return validate_json_field(
            value, models.ObservedAssociations, "skunk_association")

    def validate_badger_association(self, value):
        return validate_json_field(
            value, models.ObservedAssociations, "badger_association")

    def validate_easter_gray_squirrel_association(self, value):
        return validate_json_field(
            value,
            models.ObservedAssociations,
            "easter_gray_squirrel_association"
        )

    def validate_chipmunk_association(self, value):
        return validate_json_field(
            value, models.ObservedAssociations, "chipmunk_association")

    def validate_other_small_rodent_association(self, value):
        return validate_json_field(
            value,
            models.ObservedAssociations,
            "other_small_rodent_association"
        )

    def validate_turtle_association(self, value):
        return validate_json_field(
            value, models.ObservedAssociations, "turtle_association")

    def validate_deer_association(self, value):
        return validate_json_field(
            value, models.ObservedAssociations, "deer_association")

    class Meta:
        model = models.ObservedAssociations
        exclude = ('id',)


class FungusDetailsSerializer(CustomModelSerializerMixin,
                              BaseDetailsSerializer):
    disturbance_type = DisturbanceTypeSerializer(required=False)
    earthworm_evidence = EarthwormEvidenceSerializer(required=False)
    fruiting_bodies_age = FruitingBodiesAgeSerializer(required=False)
    other_observed_associations = ObservedAssociationsSerializer(
        required=False)

    def validate_aspect(self, value):
        return validate_json_field(
            value, models.FungusDetails, "aspect")

    def validate_apparent_substrate(self, value):
        return validate_json_field(
            value, models.FungusDetails, "apparent_substrate")

    def validate_landscape_position(self, value):
        return validate_json_field(
            value, models.FungusDetails, "landscape_position")

    def validate_mushroom_growth_form(self, value):
        return validate_json_field(
            value, models.FungusDetails, "mushroom_growth_form")

    def validate_mushroom_odor(self, value):
        return validate_json_field(
            value, models.FungusDetails, "mushroom_odor")

    def validate_mushroom_vertical_location(self, value):
        return validate_json_field(
            value, models.FungusDetails, "mushroom_vertical_location")

    def validate_slope(self, value):
        return validate_json_field(
            value, models.FungusDetails, "slope")

    class Meta:
        model = models.FungusDetails
        exclude = ('id',)


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


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Note
        fields = ("note", "ui_tab",)


class OccurrenceSerializer(serializers.Serializer):
    """Manages serialization/deserialization of Occurrences"""
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
    notes = NoteSerializer(required=False, many=True)

    def __init__(self, instance=None, data=rest_fields.empty,
                 is_writer=False, is_publisher=False, **kwargs):
        self.is_writer = is_writer
        self.is_publisher = is_publisher
        # if instance and instance.occurrence_cat:
        #     self.forms, self._form_dict = init_forms(
        #         instance.occurrence_cat.code)
        super(OccurrenceSerializer, self).__init__(instance, data, **kwargs)

    def get_fields(self):
        fields = serializers.Serializer.get_fields(self)
        if self.instance and self.instance.occurrence_cat:
            self.featuresubtype = self.instance.occurrence_cat.code
        details_serializer = get_sub_category_serializer(self.featuresubtype)
        fields['details'] = details_serializer(required=False)
        return fields

    def to_representation(self, instance):
        if isinstance(instance, models.OccurrenceTaxon):
            details_name = instance.get_details_class().__name__.lower()
            setattr(instance, details_name, instance.get_details())
        r = serializers.Serializer.to_representation(self, instance)
        result = to_flat_representation(r)
        nested_notes = result.pop("notes")
        flattened_notes = _flatten_notes_representation(nested_notes)
        result.update(flattened_notes)
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
        """Transforms the flat ``data`` input into a dictionary of forms"""
        formvalues = OrderedDict()
        for global_field_name in data:
            field_parts = global_field_name.split(".")
            if len(field_parts) > 1:
                base = formvalues
                for local_field_name in field_parts[:-1]:
                    base[local_field_name] = base.get(local_field_name, {})
                    if base[local_field_name] is None:
                        base[local_field_name] = {}
                    base = base[local_field_name]
                # avoid overwriting new values with old empty forms
                try:
                    is_a_dict = isinstance(base.get(field_parts[-1]), dict)
                    if not (is_a_dict and data[global_field_name] is None):
                        base[field_parts[-1]] = data[global_field_name]
                except AttributeError:
                    pass
            else:
                # avoid overwriting new values with old empty forms
                is_a_dict = isinstance(formvalues.get(global_field_name), dict)
                if not (is_a_dict and data[global_field_name] is None):
                    formvalues[global_field_name] = data[global_field_name]
        return formvalues

    def _parse_notes(self, nested_notes):
        result = []
        for ui_name_part, note_value in nested_notes.items():
            if note_value is not None:
                result.append({
                    "note": note_value,
                    "ui_tab": ui_name_part
                })
        return result

    def to_internal_value(self, data):
        """Dict of native values <- Dict of primitive datatypes."""
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
        try:
            self.to_internal_value_extra(data, validated_formvalues, errors)
        except AttributeError:
            pass
        fields = self._writable_fields
        # transform the flat object to a set of dictionaries of forms
        formvalues = self.to_nested_representation(data)
        for field in fields:  # validate values
            validate_method = getattr(self, 'validate_' + field.field_name, None)
            if isinstance(field, serializers.ModelSerializer):
                primitive_value = field.get_value(formvalues)
                if check_all_null(primitive_value) and not field.required:
                    continue
            else:
                primitive_value = field.get_value(formvalues)
            if field.field_name == "notes":
                if primitive_value is not rest_fields.empty:
                    primitive_value = self._parse_notes(
                        primitive_value["note"])
            if field.field_name == "tsn":
                # skip validation
                validated_value = primitive_value
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

    def process_photos(self, instance, validated_data):
        images = validated_data.get('images')
        if images:
            try:
                updated_ids = [i.get('id') for i in images]
                instance.photographs.exclude(pk__in=updated_ids).delete()

                for photo_data in validated_data.get('images'):
                    try:
                        photo = models.Photograph.objects.get(
                            pk=photo_data.get('id'))
                    except models.Photograph.DoesNotExist:
                        num_photos =Version.objects.get_for_object_reference(
                            models.Photograph,
                            photo_data.get('id')
                        ).count()
                        if num_photos > 0:  # we are restoring a removed photo
                            last_version = (
                                Version.objects.get_for_object_reference(
                                    models.Photograph,
                                    photo_data.get('id')
                                )[0]
                            )
                            # ensure the photo matches current instance
                            matches_current = (
                                    last_version.field_dict.get(
                                        'occurrence_fk') == instance.id
                            )
                            if not matches_current:
                                raise ValidationError({
                                    "images": [
                                        _("Tried to restore an invalid image")
                                    ]
                                })
                            ct_id = last_version.field_dict.get(
                                'content_type_id')
                            matches_instance = (
                                    ct_id == ContentType.objects.get_for_model(
                                instance._meta.model).pk
                            )
                            if not matches_instance:
                                raise ValidationError({
                                    "images": [
                                        _("Tried to restore an invalid image")
                                    ]
                                })
                            last_version.revert()
                            photo = models.Photograph.objects.get(
                                pk=photo_data.get('id'))
                    updated = False
                    if not photo.occurrence:
                        photo.occurrence = instance
                        updated = True
                    elif photo.occurrence != instance:
                        raise ValidationError(
                            {"images": [_("Invalid images were specified")]})
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
                raise ValidationError(
                    {"images": [_("Invalid images were specified")]})
        else:
            instance.photographs.all().delete()

    def process_notes(self, instance, validated_notes):
        """Create or update the notes associated with the instance"""
        for note_data in validated_notes:
            instance_type = ContentType.objects.get_for_model(instance)
            try:
                note = models.Note.objects.get(
                    content_type__pk=instance_type.id,
                    object_id=instance.id,
                    ui_tab=note_data["ui_tab"]
                )
            except models.Note.DoesNotExist:
                note = models.Note(
                    occurrence=instance,
                    ui_tab=note_data["ui_tab"],
                )
            note.note = note_data["note"]
            note.save()

    def _update_field_from_dict_model(self, instance, field, validated_data):
        """Update a field that specifies a related DictionaryModel relation

        Parameters
        ----------
        instance: django.db.models.Model
            The django model being updated
        field: django.db.models.fields.Field
            Django field that is being updated
        validated_data: dict
            The data being used to update the ``instance``

        """

        new_value = validated_data.get(field.name)
        old_value = getattr(instance, field.name, None)
        is_different = old_value != new_value
        if is_different and (old_value is None or new_value != old_value.code):
            try:
                if new_value != None:
                    dict_entry = field.related_model.objects.get(
                        code=new_value)
                else:
                    dict_entry = None
                setattr(instance, field.name, dict_entry)
            except Exception:
                setattr(instance, field.name, None)

    def _update_related_not_dict_model(self, instance, field, validated_data,
                                       visited):
        if instance.__class__.__name__ == "TaxonDetails":
            sub_validated_data = validated_data
            details_class = instance.occurrencetaxon.get_details_class()
            try:
                sub_instance = validated_data.get(details_class.lower())
            except django_models.ObjectDoesNotExist:
                if len(sub_validated_data) > 0:
                    sub_instance = details_class()
                    instance.details = sub_instance
        else:
            sub_validated_data = validated_data.get(field.name, {})
            try:
                sub_instance = getattr(instance, field.name)
            except (django_models.ObjectDoesNotExist, AttributeError) as exc:
                logger.debug("Skipping this field, could not retrieve "
                             "sub_instance due to {}".format(exc))
                raise RuntimeError


        if sub_instance is None and len(sub_validated_data) > 0:
            # there's data to add but no sub model exists, so create one
            related_name = field.related_fields[0][0].name
            sub_instance = field.related_model()
            self._update_instance(
                sub_instance, sub_validated_data, visited=visited)
            try:
                related_manager = getattr(sub_instance, related_name)
                related_manager.add(instance)
            except AttributeError:  # its a onetoone relation, not a foreignkey
                setattr(instance, field.name, sub_instance)
        elif not isinstance(sub_instance, django_models.Model):
            raise RuntimeError
        else:
            self._update_instance(
                sub_instance, sub_validated_data, visited=visited)

    def _update_related_model(self, instance, field, validated_data, visited):
        """Update an instance's related model"""
        is_dict_table_model = issubclass(
            field.related_model,
            (
                models.DictionaryTable,
                models.DictionaryTableExtended
            )
        )
        if is_dict_table_model:
            self._update_field_from_dict_model(
                instance, field, validated_data)
        else:
            self._update_related_not_dict_model(
                instance, field, validated_data, visited)

    def _update_instance(self, instance, validated_data, visited=None):
        """Update an instance's attributes with the input validated data

        This method will go through the instance's fields and see if they
        need to be updated, according with the data supplied in the
        ``validated_data`` mapping. It also goes through the instance's
        related models, updating them accordingly.
        This is a recursive function.

        Parameters
        ----------
        instance: nfd.core.models.Occurrence
            The occurrence to be updated
        validated_data: dict
            The data that will be used to update the occurrence
        visited: list, optional
            A list of django field names that occur either on the
            ``instance`` or on one o its related models that should not be
            updated, even if there is data for them in ``validated_data``

        """

        visited = list(visited) if visited is not None else []
        to_visit = (
            f for f in instance._meta.get_fields() if f.name not in visited)
        for field in to_visit:
            visited.append(field.name)
            if getattr(field, 'primary_key', False):
                continue
            elif field.related_model is not None:
                try:
                    self._update_related_model(
                        instance, field, validated_data, visited)
                except RuntimeError:
                    continue
            else:  # simple field
                old_value, new_value = get_field_values(
                    instance, field, validated_data)
                if new_value != old_value:
                    setattr(instance, field.name, new_value)
        instance.save()

    def _process_point_of_contact(self, name="", email="", affiliation="",
                                  phone1="", phone2="", street_address=""):
        return models.PointOfContact(
            name=name,
            email=email,
            affiliation = affiliation,
            phone1 = phone1,
            phone2 = phone2,
            street_address = street_address,
        )

    def _process_observation(self, reporter, **validated_data):
        """Generate or update an occurrence's observation"""
        reporter_instance = self._process_point_of_contact(**reporter)
        reporter_instance.save()
        observation = models.OccurrenceObservation.objects.get_or_create(
            reporter=reporter_instance,
        )[0]
        reporter_instance.save()
        verifier_data = validated_data.pop("verifier", None)
        if verifier_data is not None:
            verifier = self._process_point_of_contact(**verifier_data)
            verifier.save()
            observation.verifier = verifier
        recorder_data = validated_data.pop("recorder", None)
        if recorder_data is not None:
            recorder = self._process_point_of_contact(**recorder_data)
            recorder.save()
            observation.recorder = recorder
        instance, remaining_fields = _process_model_fields(
            observation,
            json_fields=(
                "record_origin",
            ),
            dict_table_fields={
                "daytime": models.DayTime,
                "season": models.Season,
            },
            field_values=validated_data.copy()
        )
        instance = _process_featuretype_details(instance, **remaining_fields)
        return instance

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        code = validated_data.get('featuresubtype')
        if code == 'na':
            instance = models.OccurrenceNaturalArea()
        else:
            instance = models.OccurrenceTaxon()
        instance.occurrence_cat = models.OccurrenceCategory.objects.get(
            code=code)
        instance.geom = validated_data.get('geom')
        return self.update(instance, validated_data)


class TaxonLocationSerializer(CustomModelSerializerMixin,
                              serializers.ModelSerializer):
    class Meta:
        model = models.TaxonLocation
        exclude = ('id', 'polygon')

    def validate_reservation(self, value):
        return validate_json_field(value, models.Location, "reservation")

    def validate_watershed(self, value):
        return validate_json_field(value, models.Location, "watershed")


class NaturalAreaElementSerializer(CustomModelSerializerMixin,
                                   serializers.ModelSerializer):
    disturbance_type = DisturbanceTypeSerializer(required=False)
    earthworm_evidence = EarthwormEvidenceSerializer(required=False)
    #lifestages = MossLifestages(required=False) # FIXME

    class Meta:
        model = models.ElementNaturalAreas
        exclude = ('id',)

    def validate_aspect(self, value):
        return validate_json_field(
            value, models.ElementNaturalAreas, "aspect")

    def validate_bedrock_and_outcrops(self, value):
        return validate_json_field(
            value, models.ElementNaturalAreas, "bedrock_and_outcrops")

    def validate_sensitivity(self, value):
        return validate_json_field(
            value, models.ElementNaturalAreas, "sensitivity")

    def validate_glaciar_diposit(self, value):
        return validate_json_field(
            value, models.ElementNaturalAreas, "glaciar_diposit")

    def validate_pleistocene_glaciar_diposit(self, value):
        return validate_json_field(
            value, models.ElementNaturalAreas, "pleistocene_glaciar_diposit")

    def validate_landscape_position(self, value):
        return validate_json_field(
            value, models.ElementNaturalAreas, "landscape_position")

    def validate_leap_land_cover_category(self, value):
        return validate_json_field(
            value, models.ElementNaturalAreas, "leap_land_cover_category")

    def validate_condition(self, value):
        return validate_json_field(
            value, models.ElementNaturalAreas, "condition")

    def validate_type(self, value):
        return validate_json_field(
            value, models.ElementNaturalAreas, "type")

    def validate_regional_frequency(self, value):
        return validate_json_field(
            value, models.ElementNaturalAreas, "regional_frequency")

    def validate_slope(self, value):
        return validate_json_field(
            value, models.ElementNaturalAreas, "slope")


class NaturalAreaLocationSerializer(CustomModelSerializerMixin,
                                    serializers.ModelSerializer):
    class Meta:
        model = models.NaturalAreaLocation
        exclude = ('id', 'polygon')

    def validate_reservation(self, value):
        return validate_json_field(value, models.Location, "reservation")

    def validate_watershed(self, value):
        return validate_json_field(value, models.Location, "watershed")


class TaxonOccurrenceSerializer(OccurrenceSerializer):
    taxon = TaxonDetailSerializer(required=True)
    voucher = VoucherSerializer(required=False)
    location = TaxonLocationSerializer(required=False)

    def update(self, instance, validated_data):
        with reversion.create_revision():
            taxon, created = models.Taxon.objects.get_or_create(
                tsn=self.context.get("tsn"))
            instance.taxon = taxon
            observation_data = validated_data.pop("observation", {})
            if len(observation_data) > 0:
                observation = self._process_observation(
                    reporter=observation_data.pop("reporter"),
                    **observation_data
                )
                observation.save()
                instance.observation = observation
            details_data = validated_data.pop("details", {})
            details_data["lifestages"] = validated_data.pop("lifestages", None)
            if len(details_data) > 1 or details_data["lifestages"] is not None:
                details = self._process_details(instance, details_data)
                details.save()
                instance.details = details
            instance.geom = validated_data.pop("geom", None) or instance.geom
            instance.version += 1
            instance.verified = validated_data.pop("verified", None) or False
            if self.is_publisher:
                instance.released = validated_data.pop(
                    "released", None) or False
                if instance.released:
                    instance.released_versions += 1
            else:
                instance.released = False
            fields_to_skip_update = [
                "occurrencetaxon",
                "occurrencenaturalarea",
                "occurrence_cat",
                "inclusion_date",
                # the next fields have already been handled
                "details",
                "taxon",
                "observation",
                "geom",
                "version",
                "released_versions",
                "verified",
                "released",
                # the next fields are m2m relations and are handled elsewhere
                "photographs",
                "notes",
            ]
            self._update_instance(
                instance, validated_data, visited=fields_to_skip_update)
            self.process_photos(instance, validated_data)
            self.process_notes(instance, validated_data.get("notes", []))
        return instance

    def _process_details(self, occurrence_instance, validated_data):
        """Generate or update an occurrence's details"""
        details_class = occurrence_instance.get_details_class()
        try:
            existent_details = getattr(
                occurrence_instance.details, details_class.__name__.lower())
        except (AttributeError, details_class.DoesNotExist):
            existent_details = details_class(
                occurrencetaxon=occurrence_instance)
            existent_details.save()
        details_processor = {
            models.ConiferDetails: _process_plant_details,
            models.FernDetails: _process_plant_details,
            models.FloweringPlantDetails: _process_plant_details,
            models.PondLakeAnimalDetails: _process_pond_lake_animal_details,
            models.LandAnimalDetails: _process_land_animal_details,
            models.MossDetails: _process_plant_details,
            models.FungusDetails: _process_fungus_details,
            models.SlimeMoldDetails: _process_slimemold_details,
            models.StreamAnimalDetails: _process_stream_animal_details,
            models.WetlandAnimalDetails: _process_wetland_animal_details,
        }.get(details_class)
        return details_processor(existent_details, **validated_data)


class NaturalAreaOccurrenceSerializer(OccurrenceSerializer):
    element = NaturalAreaElementSerializer(required=False)
    location = NaturalAreaLocationSerializer(required=False)

    def _process_natural_area(self, **validated_data):
        element, created = models.ElementNaturalAreas.objects.get_or_create(
            natural_area_code_nac=validated_data.pop("natural_area_code_nac"))
        element, remaining_fields = _process_model_fields(
            element,
            json_fields=(
                "type",
                "aspect",
                "slop",
                "sensitivity",
                "condition",
                "leap_land_cover_category",
                "landscape_position",
                "glaciar_diposit",
                "pleistocene_glaciar_diposit",
                "bedrock_and_outcrops",
                "regional_frequency",
            ),
            dict_table_fields={
                "cm_status": models.CmStatus,
                "s_rank": models.SRank,
                "n_rank": models.NRank,
                "g_rank": models.GRank,
            },
            related_fields={
                "disturbance_type": models.DisturbanceType,
                "earthworm_evidence": models.EarthwormEvidence,
            },
            field_values=validated_data.copy()
        )
        _process_featuretype_details(element, **remaining_fields)
        return element

    def update(self, instance, validated_data):
        with reversion.create_revision():
            natural_element_data = validated_data.pop("element", {})
            if len(natural_element_data) > 0:
                natural_area = self._process_natural_area(
                    **natural_element_data)
                natural_area.save()
                instance.element = natural_area
            observation_data = validated_data.pop("observation", {})
            if len(observation_data) > 0:
                observation = self._process_observation(
                    reporter=observation_data.pop("reporter"),
                    **observation_data
                )
                observation.save()
                instance.observation = observation
            element_data = validated_data.pop("element", {})
            if len(element_data) > 0:
                element = self._process_element(instance, **element_data)
                element.save()
                instance.element = element
            instance.geom = validated_data.pop("geom", None) or instance.geom
            instance.version += 1
            instance.verified = validated_data.pop("verified", None) or False
            if self.is_publisher:
                instance.released = validated_data.pop(
                    "released", None) or False
                if instance.released:
                    instance.released_versions += 1
            else:
                instance.released = False
            fields_to_skip_update = [
                "occurrencetaxon",
                "occurrencenaturalarea",
                "occurrence_cat",
                "inclusion_date",
                # the next fields have already been handled
                "element",
                "details",
                "taxon",
                "observation",
                "geom",
                "version",
                "released_versions",
                "verified",
                "released",
                # the next fields are m2m relations and are handled elsewhere
                "photographs",
                "notes",
            ]
            self._update_instance(
                instance, validated_data, visited=fields_to_skip_update)
            self.process_photos(instance, validated_data)
            self.process_notes(instance, validated_data.get("notes", []))
        return instance

    def _process_element(self, instance, **validated_data):
        pass


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


class TaxonOccurrenceListSerializer(ListSerializer):
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
        result["taxon.tsn"] = instance.taxon.tsn
        result["taxon.name"] = instance.taxon.name
        result['observation.observation_date'] = instance.observation.observation_date
        return result


class NaturalAreaOccurrenceListSerializer(ListSerializer):
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


class ItisTaxonSearchSerializer(serializers.Serializer):

    def to_representation(self, instance):
        return {
            "tsn": instance.tsn,
            "name": "{0.tsn} - {0.name} - {0.rank}".format(instance),
        }


class ItisTaxonHierarchySerializer(serializers.Serializer):

    def to_representation(self, instance):
        result = {
            "tsn": instance.tsn,
            "name": instance.name,
            "rank": instance.rank,
            instance.rank.lower(): instance.name,
        }
        if instance.common_names is not None:
            names = (n[1] for n in instance.common_names if
                     n[0].lower() == "english")
            english_names = ", ".join(names)
            result["common_names.English"] = english_names
        for rank in instance.upper_ranks:
            result[rank["rank"].lower()] = rank["name"]
        return result


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


class FormDefinitionsSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        form_definition = get_complete_form_definition(instance.subtype)
        try:
            management_page = [
                p for p in form_definition if p["id"] == "management"][0]
            self._adjust_management_page(
                management_page, instance.is_writer, instance.is_publisher)
        except KeyError:
            pass
        occurrence_category = models.OccurrenceCategory.objects.get(
            code=instance.subtype)
        return get_form_representation(
            form_definition,
            feature_type=occurrence_category.main_cat,
            sub_type=instance.subtype
        )

    def _adjust_management_page(self, management_page, is_writer,
                                is_publisher):
        for field in management_page["fields"]:
            if field["field"] == "released" and is_publisher:
                field["readonly"] = False
            elif field["field"] == "verified" and (is_publisher or is_writer):
                field["readonly"] = False


def get_form_representation(form_definition, feature_type, sub_type):
    return {
        "featuretype": feature_type,
        "featuresubtype": sub_type,
        "forms": [
            get_page_representation(page_def) for page_def in form_definition]
    }

def get_page_representation(page_definition):
    page = {
        "formlabel": page_definition["label"],
        "formname": page_definition["id"],
        "formitems": [],
    }
    for field_definition in page_definition["fields"]:
        page["formitems"].append(
            get_field_representation(field_definition))
    return page


def get_field_representation(field_definition):
    field = {
        "type": field_definition.get("widget", "string"),
        "key": field_definition["field"],
        "label": field_definition["label"],
        "mandatory": field_definition.get("mandatory", False),
        "readonly": field_definition.get("readonly", False),
    }
    if field["type"] in ("stringcombo", "stringcombo_multiple"):
        choices_dict_model_path = field_definition.get("choices")
        field["values"] = {"items": []}
        if choices_dict_model_path is not None:
            choices = get_form_field_choices(choices_dict_model_path)
            field["values"]["items"] = [
                {"key": k, "value": v} for k, v in choices]
    show_key_with_value = field_definition.get("show_key_with_value")
    if show_key_with_value is not None:
        field["show_key_with_value"] = True
    return field


def import_class(python_path):
    module_path, class_name = python_path.rpartition(".")[::2]
    module = importlib.import_module(module_path)
    class_ = getattr(module, class_name)
    return class_


def get_form_field_choices(choices_dict_model_path):
    class_ = import_class(choices_dict_model_path)
    return class_.objects.values_list("code", "name")


def get_complete_form_definition(category_subtype_code):
    form_definition = get_plain_form_definition(category_subtype_code)
    needs_common_defs = any((i.has_key("common") for i in form_definition))
    if needs_common_defs:
        common_defs = get_common_form_definitions()
        for page_def in form_definition:
            common_field_definitions = common_defs.get(page_def.get("common"))
            if common_field_definitions is not None:
                del page_def["common"]
                page_def.update(common_field_definitions)
    return form_definition


def get_plain_form_definition(category_subtype_code):
    """Get the form definition without updating the ``common`` pages."""
    category_path = settings.NFDCORE_FORM_DEFINITIONS[category_subtype_code]
    with open(category_path) as fh:
        definition = yaml.safe_load(fh)
    return definition


def get_common_form_definitions():
    common_path = settings.NFDCORE_FORM_DEFINITIONS.get("common")
    try:
        with open(common_path) as fh:
            common_definitions = yaml.safe_load(fh)
    except (IOError, TypeError):
        common_definitions = None
    return common_definitions



def _process_json_fields(instance, fields, **field_values):
    for field_name in fields:
        value = field_values.get(field_name)
        if value is not None:
            setattr(instance, field_name, value)
            field_values.pop(field_name)
    return field_values


def _process_dict_table_foreign_key_fields(instance, fields,
                                           **field_values):
    for field_name, dict_model in fields.items():
        value = field_values.get(field_name)
        if value is not None:
            dict_table_instance = dict_model.objects.get(code=value)
            setattr(instance, field_name, dict_table_instance)
            field_values.pop(field_name)
    return field_values


def _process_foreign_key_fields(instance, fields, **field_values):
    for field_name, related_model in fields.items():
        field_data = field_values.pop(field_name, {})
        if len(field_data) > 0:
            related_instance = related_model(**field_data)
            related_instance.save()
            setattr(instance, field_name, related_instance)
    return field_values


def _process_model_fields(instance, json_fields=None, dict_table_fields=None,
                          related_fields=None, field_values=None):
    json_fields = list(json_fields) if json_fields is not None else []
    dict_table_fields = dict(
        dict_table_fields) if dict_table_fields is not None else {}
    related_fields = dict(related_fields) if related_fields is not None else {}
    values = field_values.copy() if field_values is not None else {}
    remaining_fields = _process_json_fields(instance, json_fields, **values)
    remaining_fields = _process_dict_table_foreign_key_fields(
        instance, dict_table_fields, **remaining_fields)
    remaining_fields = _process_foreign_key_fields(
        instance, related_fields, **remaining_fields)
    return instance, remaining_fields


def _process_featuretype_details(instance, **validated_fields):
    for field_name, field_value in validated_fields.items():
        current_value = getattr(instance, field_name, None)
        if current_value != field_value and field_value is not None:
            setattr(instance, field_name, field_value)
    return instance


def _process_plant_details(instance, **validated_fields):
    instance, remaining_fields = _process_model_fields(
        instance,
        json_fields=(
            "moisture_regime",
            "ground_surface",
            "general_habitat_category",
            "disturbance_type",
            "landscape_position",
            "aspect",
            "slope",
            "lifestages",
        ),
        dict_table_fields={
            "plant_count": models.PlantCount,
            "tree_canopy_cover": models.CanopyCover,
            "disturbance_type": models.DisturbanceType,
            "earthworm_evidence": models.EarthwormEvidence
        },
        field_values=validated_fields.copy()
    )
    return _process_featuretype_details(instance, **remaining_fields)


def _process_animal_details(instance, **validated_fields):
    instance, remaining_fields = _process_model_fields(
        instance,
        json_fields=(
            "gender",
            "marks",
            "lifestages",
            "diseases_and_abnormalities",
            "lifestages",
        ),
        field_values=validated_fields.copy()
    )
    return _process_featuretype_details(instance, **remaining_fields)


def _process_aquatic_animal_details(instance, **validated_fields):
    instance, remaining_fields = _process_model_fields(
        instance,
        json_fields=(
            "sampler",
        ),
        field_values=validated_fields.copy()
    )
    return _process_animal_details(instance, **remaining_fields)


def _process_land_animal_details(instance, **validated_fields):
    instance, remaining_fields = _process_model_fields(
        instance,
        json_fields=(
            "sampler",
            "stratum",
        ),
        field_values=validated_fields.copy()
    )
    return _process_animal_details(instance, **remaining_fields)


def _process_pond_lake_animal_details(instance, **validated_fields):
    instance, remaining_fields = _process_model_fields(
        instance,
        json_fields=(
            "pond_lake_use",
            "shoreline_type",
            "microhabitat",
        ),
        dict_table_fields={
            "pond_lake_type": models.PondLakeType
        },
        field_values=validated_fields.copy()
    )
    return _process_aquatic_animal_details(instance, **remaining_fields)


def _process_stream_animal_details(instance, **validated_fields):
    instance, remaining_fields = _process_model_fields(
        instance,
        json_fields=(
            "channel_type",
            "hmfei_local_abundance",
            "lotic_habitat_type",
        ),
        dict_table_fields={
            "designated_use": models.StreamDesignatedUse,
            "substrate": models.StreamSubstrate,
            "water_flow_type": models.WaterFlowType,
        },
        field_values=validated_fields.copy()
    )
    return _process_aquatic_animal_details(instance, **remaining_fields)


def _process_wetland_animal_details(instance, **validated_fields):
    instance, remaining_fields = _process_model_fields(
        instance,
        json_fields=(
            "wetland_type",
            "water_source",
            "habitat_feature",
        ),
        dict_table_fields={
            "wetland_location": models.WetlandLocation,
            "connectivity": models.WetlandConnectivity,
        },
        related_fields={
            "vegetation": models.WetlandVetegationStructure,
        },
        field_values=validated_fields.copy()
    )
    return _process_aquatic_animal_details(instance, **remaining_fields)


def _process_fungus_details(instance, **validated_fields):
    instance, remaining_fields = _process_model_fields(
        instance,
        json_fields=(
            "aspect",
            "slope",
            "landscape_position",
            "apparent_substrate",
            "mushroom_vertical_location",
            "mushroom_growth_form",
            "mushroom_odor",
        ),
        dict_table_fields={
            "canopy_cover": models.CanopyCover,
            "mushroom_group": models.MushroomGroup,
        },
        related_fields={
            "other_observed_associations": models.ObservedAssociations,
            "earthworm_evidence": models.EarthwormEvidence,
            "fruiting_bodies_age": models.FruitingBodiesAge,
            "disturbance_type": models.DisturbanceType,
        },
        field_values=validated_fields.copy()
    )
    return _process_featuretype_details(instance, **remaining_fields)


def _process_slimemold_details(instance, **validated_fields):
    instance, remaining_fields = _process_model_fields(
        instance,
        json_fields=(
            "slime_mold_class",
            "slime_mold_media",
            "lifestages",
        ),
        field_values=validated_fields.copy()
    )
    return _process_featuretype_details(instance, **remaining_fields)


def _process_naturalarea_element(instance, **validated_fields):
    instance, remaining_fields = _process_model_fields(
        instance,
        json_fields=(
            "type",
            "aspect",
            "slope",
            "sensitivity",
            "condition",
            "leap_land_cover_category",
            "landscape_position",
            "glaciar_diposit",
            "pleistocene_glaciar_diposit",
            "bedrock_and_outcrops",
            "regional_frequency",
        ),
        related_fields={
            "disturbance_type": models.DisturbanceType,
            "earthworm_evidence": models.EarthwormEvidence,
        },
        field_values=validated_fields.copy()
    )
    return _process_featuretype_details(instance, **remaining_fields)
