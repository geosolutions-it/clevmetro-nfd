
from django.db.models.fields import BooleanField, TextField, CharField, DateTimeField
from django.db.models.fields import IntegerField, DecimalField, FloatField
from django.db.models.fields.related import ForeignKey
from django.contrib.gis.db.models.fields import GeometryField
from django.utils.translation import ugettext_lazy as _

from core.models import DictionaryTable, Voucher, OccurrenceTaxon, PlantDetails,\
    StreamAnimalDetails, LandAnimalDetails
from core.models import AnimalDetails, AnimalLifestages, OccurrenceObservation, PointOfContact

featuretype_form_fragments = {
    "observation": [
        {"formname": "observation", "formlabel": _("Observation"), "model": OccurrenceObservation},
        {"formname": "reporter", "formlabel": _("Observation reporter"), "model": PointOfContact},
        {"formname": "recorder", "formlabel": _("Observation recorder"), "model": PointOfContact},
        {"formname": "verifier", "formlabel": _("Observation verifier"), "model": PointOfContact}
        ],
    "voucher": [{"formname": "voucher", "formlabel": _("Observation voucher"), "model": Voucher}],
    }

occurrence_defs = {
    "ln": {
        "mainmodel": OccurrenceTaxon,
        "forms": [
            {"formname": "land_animal_details", "formlabel": _("Details"), "model": LandAnimalDetails},
            {"formname": "animal_lifestages", "formlabel": _("Animal lifestages"), "model": AnimalLifestages}
            ]+featuretype_form_fragments["observation"]+featuretype_form_fragments["voucher"]
    },
    "st": {
        "mainmodel": OccurrenceTaxon,
        "forms": [
            {"formname": "land_animal_details", "formlabel": _("Details"), "model": StreamAnimalDetails},
            {"formname": "animal_lifestages", "formlabel": _("Animal lifestages"), "model": AnimalLifestages}
            ]+featuretype_form_fragments["observation"]+featuretype_form_fragments["voucher"]
    },
    "pl": {
        "mainmodel": OccurrenceTaxon,
        "forms": [
            {"formname": "land_animal_details", "formlabel": _("Details"), "model": PlantDetails},
            #{"formname": "animal_lifestages", "formlabel": _("Animal lifestages"), "model": AnimalLifestages},
            ]+featuretype_form_fragments["observation"]+featuretype_form_fragments["voucher"]
    }
}

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