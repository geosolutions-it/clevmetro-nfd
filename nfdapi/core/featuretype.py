
from django.db.models.fields import BooleanField, TextField, CharField, DateTimeField
from django.db.models.fields import IntegerField, DecimalField, FloatField

from django.db.models.fields.related import ForeignKey
from core.models import DictionaryTable
from django.contrib.gis.db.models.fields import GeometryField
from django.utils.translation import ugettext_lazy as _

featureTypes = {
    "landanimal": {
        "forms": [
            "land_animal_details": {"model": },
            "animal_lifestages": {"model": },
            "observation": {"model": },
            "reporter": {"model": },
            "recorder": {"model": },
            "verifier": {"model": }
            ]
    }
}

def get_form_featuretype(model):
    fields = model._meta.get_fields()
    result = []
    for f in fields:
        fdef = {}
        
        if f.primary_key:
            fdef['type'] = 'pk'
        if isinstance(f, CharField) or isinstance(f, TextField):
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