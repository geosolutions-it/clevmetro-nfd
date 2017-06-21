
from django.db.models.fields import BooleanField, TextField, CharField, DateTimeField,\
    DateField
from django.db.models.fields import IntegerField, DecimalField, FloatField
from django.db.models.fields.related import ForeignKey
from django.contrib.gis.db.models.fields import GeometryField
from django.utils.translation import ugettext_lazy as _

from core.models import DictionaryTable, Voucher, OccurrenceTaxon, PlantDetails,\
    StreamAnimalDetails, LandAnimalDetails, ElementSpecies
from core.models import AnimalLifestages, OccurrenceObservation, PointOfContact

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
            form_values = []
            for f in fields:
                fdef = {}
                fvalue = getattr(form_instance, f.name, None)
                if not fvalue:
                    pass
                elif getattr(f, 'primary_key', False):
                    pass
                elif isinstance(f, CharField) or isinstance(f, TextField):
                    fdef['key'] = f.name
                    fdef['value'] = fvalue
                elif isinstance(f, BooleanField):
                    fdef['key'] = f.name
                    fdef['value'] = fvalue
                elif isinstance(f, DateTimeField) or isinstance(f, DateField):
                    fdef['key'] = f.name
                    fdef['value'] = fvalue
                elif isinstance(f, GeometryField):
                    # skip geoms
                    pass
                elif isinstance(f, FloatField) or isinstance(f, DecimalField):
                    fdef['key'] = f.name
                    fdef['value'] = fvalue
                elif isinstance(f, IntegerField):
                    fdef['key'] = f.name
                    fdef['value'] = fvalue
                elif isinstance(f, ForeignKey):
                    if issubclass(f.related_model, DictionaryTable):
                        fdef['key'] = f.name
                        fdef['value'] = fvalue.code
                if 'key' in fdef:
                    form_values.append(fdef) 
                    
            self.result[form_name] = form_values
        
    

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
            form['formitems'] = self.get_form_featuretype(formdef['model'])
            forms.append(form)
        return result
    

    def get_form_featuretype(self, model):
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
                fdef['key'] = f.name
                fdef['label'] = _(f.name) 
                result.append(fdef)
        return result