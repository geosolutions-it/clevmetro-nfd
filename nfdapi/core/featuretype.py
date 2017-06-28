
from django.db.models.fields import BooleanField, TextField, CharField, DateTimeField,\
    DateField, related, NullBooleanField
from django.db.models.fields import IntegerField, DecimalField, FloatField
from django.db.models.fields.related import ForeignKey
from django.contrib.gis.db.models.fields import GeometryField

from core.models import DictionaryTable, Voucher, OccurrenceTaxon, PlantDetails,\
    StreamAnimalDetails, LandAnimalDetails, ElementSpecies, Species
from core.models import AnimalLifestages, OccurrenceObservation, PointOfContact
from rest_framework.serializers import Serializer, ModelSerializer
from django.db import models as db_models
from rest_framework import fields as rest_fields
from rest_framework import relations as rest_rels
from collections import OrderedDict
from rest_framework.serializers import Field
import reversion
from reversion.models import Version
from rest_framework.fields import empty

def _(message): return message

LAND_ANIMAL_TYPE = [
    (_('species'), Species, ['species.element_species']),
    (_('species.element_species'), ElementSpecies, []),
    #(_('occurrencemanagement'), OccurrenceTaxon, []),
    (_('observation'), OccurrenceObservation, ['observation.reporter', 'observation.verifier', 'observation.recorder']),
    (_('observation.reporter'), PointOfContact, []),
    (_('observation.verifier'), PointOfContact, []),
    (_('observation.recorder'), PointOfContact, []),
    (_('voucher'), Voucher, []),
    (_('landanimaldetails'), LandAnimalDetails, [])
    ]

del _
from django.utils.translation import ugettext_lazy as _

featuretype_form_fragments = {
    "observation": [
        {"formname": "observation", "formlabel": _("Observation"), "model": OccurrenceObservation},
        {"formname": "reporter", "formlabel": _("Observation reporter"), "model": PointOfContact},
        {"formname": "recorder", "formlabel": _("Observation recorder"), "model": PointOfContact},
        {"formname": "verifier", "formlabel": _("Observation verifier"), "model": PointOfContact}
        ],
    "voucher": [{"formname": "voucher", "formlabel": _("Observation voucher"), "model": Voucher}],
    "species": [{"formname": "species", "formlabel": _("What is it?"), "model": ElementSpecies}]
    }

occurrence_defs = {
    "ln": {
        "mainmodel": OccurrenceTaxon,
        "forms": featuretype_form_fragments["species"]+[
            {"formname": "landanimaldetails", "formlabel": _("Details"), "model": LandAnimalDetails},
            {"formname": "animal_lifestages", "formlabel": _("Animal lifestages"), "model": AnimalLifestages}
            ]+featuretype_form_fragments["observation"]+featuretype_form_fragments["voucher"]
    },
    "st": {
        "mainmodel": OccurrenceTaxon,
        "forms": featuretype_form_fragments["species"]+[
            {"formname": "streamanimaldetails", "formlabel": _("Details"), "model": StreamAnimalDetails},
            {"formname": "animal_lifestages", "formlabel": _("Animal lifestages"), "model": AnimalLifestages}
            ]+featuretype_form_fragments["observation"]+featuretype_form_fragments["voucher"]
    },
    "pl": {
        "mainmodel": OccurrenceTaxon,
        "forms": featuretype_form_fragments["species"]+[
            {"formname": "plantdetails", "formlabel": _("Details"), "model": PlantDetails},
            #{"formname": "animal_lifestages", "formlabel": _("Animal lifestages"), "model": AnimalLifestages},
            ]+featuretype_form_fragments["observation"]+featuretype_form_fragments["voucher"]
    }
}


class FeatureInfoSerializer():
    def __init__(self):
        self.result = {}
    
    def get_feature_info(self, occurrence_instance):
        main_cat = occurrence_instance.occurrence_cat.main_cat
        subcat_code = occurrence_instance.occurrence_cat.code
        #occurrence_def = occurrence_defs[subcat_code]
        
        self.result['featuretype'] = main_cat
        self.result['versions'] = 1 #FIXME
        self.result['formvalues'] = []
        self._add_form_values(occurrence_instance.species_element, 'species')
        self._add_form_values(occurrence_instance.observation, 'observation')
        self._add_form_values(occurrence_instance.voucher, 'voucher')
        details_instance = occurrence_instance.get_details()
        details_form_name = details_instance.__class__.__name__.lower()
        self._add_form_values(details_instance, details_form_name)
        if occurrence_instance.observation:
            self._add_form_values(occurrence_instance.observation.reporter, 'reporter')
            self._add_form_values(occurrence_instance.observation.recorder, 'recorder')
            self._add_form_values(occurrence_instance.observation.verifier, 'verifier')
        #FIXME: consider the rest of main fields from occurrence
        
        #FIXME: should include also the geojson
        return self.result
    
    def _add_form_values(self, form_instance, form_name):
        if (form_instance):
            fields = form_instance._meta.get_fields()
            for f in fields:
                fdef = {}
                fvalue = getattr(form_instance, f.name, None)
                if not fvalue:
                    pass
                elif getattr(f, 'primary_key', False):
                    pass
                elif isinstance(f, CharField) or isinstance(f, TextField) or isinstance(f, BooleanField):
                    fdef['key'] = form_name + "." + f.name
                    fdef['value'] = fvalue
                elif isinstance(f, DateTimeField) or isinstance(f, DateField):
                    fdef['key'] = form_name + "." + f.name
                    fdef['value'] = fvalue
                elif isinstance(f, GeometryField):
                    # skip geoms
                    pass
                elif isinstance(f, FloatField) or isinstance(f, DecimalField) or isinstance(f, IntegerField):
                    fdef['key'] = form_name + "." + f.name
                    fdef['value'] = fvalue
                elif isinstance(f, ForeignKey):
                    if issubclass(f.related_model, DictionaryTable):
                        fdef['key'] = form_name + "." + f.name
                        fdef['value'] = fvalue.code
                if 'key' in fdef:
                    self.result['formvalues'].append(fdef)  
    

class FeatureTypeSerializer():
    def get_feature_type(self, name, subcat_code):
        occurrence_def = occurrence_defs[subcat_code]
        result = {}
        result['featuretype'] = name
        forms = []
        result['forms'] = forms
        for formdef in occurrence_def['forms']:
            form = {}
            form['formlabel'] = formdef['formlabel']
            form['formname'] = formdef['formname']
            form['formitems'] = self.get_form_featuretype(formdef['formname'], formdef['model'])
            forms.append(form)
        return result
    

    def get_form_featuretype(self, form_name, model):
        fields = model._meta.get_fields()
        result = []
        for f in fields:
            fdef = {}
            
            if getattr(f, 'primary_key', False):
                fdef['type'] = 'pk'
            elif isinstance(f, CharField) or isinstance(f, TextField):
                fdef['type'] = 'string'
            elif isinstance(f, BooleanField):
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
            elif isinstance(f, ForeignKey):
                if issubclass(f.related_model, DictionaryTable):
                    fdef['type'] = 'stringcombo'
                    items = []
                    for item in f.related_model.objects.all():
                        idef = {}
                        idef['key'] = item.code
                        idef['value'] = item.name
                        items.append(idef)
                    fdef['values'] = {'items': items}
                else:
                    fdef['type'] = 'fk'
                
            if 'type' in fdef:        
                fdef['key'] = form_name + "." + f.name
                fdef['label'] = _(f.name) 
                result.append(fdef)
        return result


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

class TotalVersionsField(rest_fields.IntegerField):
    def get_attribute(self, instance):
        versions = Version.objects.get_for_object(instance)
        return len(versions)

def get_serializer_fields(form_name, model):
    fields = model._meta.get_fields()
    result = OrderedDict()
    for f in fields:
        fdef = None
        
        kwargs = {}
        kwargs['required'] = False # set all form fields as not required, as related fields may be missing
        
        if getattr(f, 'primary_key', False):
            pass
        elif isinstance(f, CharField) or isinstance(f, TextField):
            kwargs['max_length'] = getattr(f, 'max_length', None)
            kwargs['allow_blank'] = getattr(f, 'blank', False)
            kwargs['allow_null'] = True
            fdef = rest_fields.CharField(**kwargs)
        elif isinstance(f, BooleanField) or isinstance(f, NullBooleanField):
            fdef = rest_fields.NullBooleanField(**kwargs)
        elif isinstance(f, DateTimeField):
            kwargs['allow_null'] = True
            fdef = rest_fields.DateTimeField(**kwargs)
            kwargs['allow_null'] = True
        elif isinstance(f, DateField):
            kwargs['allow_null'] = True
            fdef = rest_fields.DateField(**kwargs)
        elif isinstance(f, DecimalField):
            kwargs['allow_null'] = True
            kwargs['max_digits'] = getattr(f, 'max_digits', None)
            kwargs['decimal_places'] = getattr(f, 'decimal_places', None)
            fdef = rest_fields.DecimalField(**kwargs)
        elif isinstance(f, FloatField):
            kwargs['allow_null'] = True
            fdef = rest_fields.FloatField(**kwargs)
        elif isinstance(f, IntegerField):
            kwargs['allow_null'] = True
            fdef = rest_fields.IntegerField(**kwargs)
        elif isinstance(f, ForeignKey): #FIXME
            if issubclass(f.related_model, DictionaryTable):
                kwargs['allow_blank'] = getattr(f, 'blank', False)
                kwargs['allow_null'] = True
                fdef = DictionaryField(**kwargs)
            else:
                pass
        elif isinstance(f, GeometryField):
            # skip geoms
            pass
            
        if fdef:
            result[form_name + "." + f.name] = fdef
    return result


class MetroparksSerializer(Serializer):
    
    def get_fields(self):
        """
        Gets seralizer fields, according to the defined forms
        """
        fields = OrderedDict()
        fields['id'] = rest_fields.IntegerField(read_only=True)
        fields['released'] = rest_fields.BooleanField()
        fields['inclusion_date'] = rest_fields.DateTimeField()
        fields['occurrence_cat'] = DictionaryField()
        fields['version'] = rest_fields.IntegerField(read_only=True)
        fields['versions'] = TotalVersionsField()
        
        
        forms = self.get_forms()
        for form in forms:
            form_name = form[0]
            model_class = form[1]
            serializer_fields = get_serializer_fields(form_name, model_class)
            for field_name, serializer_field_class in serializer_fields.items():
                fields[field_name] = serializer_field_class
        return fields
    
    def get_forms(self):
        return self.forms
    
    def _get_form_fieldnames(self, form_name, instance):
        result = []
        if (instance):
            fields = instance._meta.get_fields()
            for f in fields:
                if getattr(f, 'primary_key', False):
                    pass
                elif isinstance(f, CharField) or isinstance(f, TextField) or isinstance(f, BooleanField) or \
                    isinstance(f, DateTimeField) or isinstance(f, DateField) or isinstance(f, FloatField) or \
                    isinstance(f, DecimalField) or isinstance(f, IntegerField):
                    name = form_name + "." + f.name
                    result.append(name)
        return result
    
    """
    Not implemented for the moment
    def create(self, validated_data):

        with reversion.create_revision():
            ModelClass = self.Meta.model
            if isinstance(ModelClass, OccurrenceTaxon):
                # taxon
                pass
            else:
                # natural area
                pass
    """
    
    def set_form_values(self, form_name, instance, validated_data, force_save=False):
        if instance and validated_data:
            fields = self._get_form_fieldnames(form_name, instance)
            #if instance.pk is None:
            #    force_save = True
            modified = False
            for fname in fields:
                new_value = validated_data.get(form_name + "." + fname)
                old_value = getattr(instance, fname, None)
                if new_value != old_value:
                    modified = True
                    setattr(instance, fname, new_value)
            if force_save or modified:
                instance.save()
                return True
        return False
    
    def _get_form_model_instance(self, form_name, model_class, parent_instance):
        if 'details' in form_name:
            related_instance = parent_instance.get_details()
        else:
            related_instance = getattr(parent_instance, form_name, None)
        if not related_instance:
            related_instance = model_class()
        return related_instance
    
    def _delete_related(self, main_instance, rel_field_name, related_instance):
        setattr(main_instance, rel_field_name, None)
        related_instance.delete()
    
    def _update_form(self, form_name, model_class, validated_data, parent_instance, child_forms=[]):
        """
        Returns a tuple (instance, saved).
        instance: processed instance object (or None)
        saved: (boolean) True if the instance has been created or updated, false otherwise
        """
        related_instance = self._get_form_model_instance(form_name, model_class, parent_instance)
        any_saved = False
        for (child_form_name, child_model_class, child_child_forms) in child_forms:
            saved = self._update_form(child_form_name, child_model_class, validated_data, related_instance, child_child_forms)
            any_saved = any_saved or saved
            
        saved = self.set_form_values(form_name, related_instance, validated_data, any_saved)
        any_saved = any_saved or saved
        
        if related_instance:
            if any_saved:
                if 'details' in form_name:
                    setattr(parent_instance, 'details', related_instance)
                else:
                    setattr(parent_instance, form_name, related_instance)
        return any_saved
        
    def update0(self, instance, validated_data):
        with reversion.create_revision():
            observation_children = [
                ('reporter', PointOfContact, []),
                ('verifier', PointOfContact, []),
                ('recorder', PointOfContact, []),
                ]
            self._update_form('observation', OccurrenceObservation, validated_data, instance, child_forms=observation_children)
            self._update_form('voucher', Voucher, validated_data, instance)
            details_model_class = instance.get_details_class()
            self._update_form('landanimaldetails', details_model_class, validated_data, instance)
            
            if isinstance(instance, OccurrenceTaxon):
                # taxon
                pass
            else:
                # natural area
                pass
            instance.version = instance.version + 1
            instance.save()
        return instance
    
    def _get_form_def_tree(self, form_name, model_class, children):
        complete_children_def = []
        for child in children:
            (child_form_name, child_model_class, child_children) = self._form_dict[child]
            child_def = self._get_form_def_tree(child_form_name, child_model_class, child_children)
            complete_children_def.append(child_def)
        return (form_name, model_class, complete_children_def)
        
    
    def get_toplevel_forms(self):
        forms = []
        for (form_name, model_class, children) in self.get_forms():
            if "." not in form_name:
                # only for top-level objects
                form_def = self._get_form_def_tree(form_name, model_class, children)
                forms.append(form_def)
        return forms
    
    def update(self, instance, validated_data):
        with reversion.create_revision():
            print self.get_toplevel_forms()
            for (form_name, model_class, children) in self.get_toplevel_forms():
                self._update_form(form_name, model_class, validated_data, instance, children)
            
            if isinstance(instance, OccurrenceTaxon):
                # taxon
                pass
            else:
                # natural area
                pass
            instance.version = instance.version + 1
            instance.save()
        return instance
    
    def to_representation(self, instance):
        return Serializer.to_representation(self, instance)
    
    def to_internal_value(self, data):
        return Serializer.to_internal_value(self, data)


class LandAnimalSerializer(MetroparksSerializer):
    def __init__(self, instance=None, data=empty, **kwargs):
        self.forms = LAND_ANIMAL_TYPE
        # FIXME: move any form pre-processing out of the instance
        self._form_dict = {}
        for form in self.forms:
            self._form_dict[form[0]] = form

        super(LandAnimalSerializer, self).__init__(instance, data, **kwargs)

        