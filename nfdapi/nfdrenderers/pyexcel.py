# -*- coding: utf-8 -*-
'''
Created on 10 oct. 2017

@author: Cesar Martinez Izquierdo
'''
from rest_framework.renderers import BaseRenderer    
from pyexcel_io import save_data
from collections import OrderedDict
from io import BytesIO
from six import itervalues
from datetime import datetime
import json

class NotImplemented(Exception):
    pass

class PyExcelBaseRenderer(BaseRenderer):    
    def _get_features(self, data):
        if data.get('features'):
            return data.get('features')
        if data.get('results'):
            return data.get('results').get('features')
        return [data]
    
    def _get_coords(self, feature):
        if feature.get("geometry"):
            return feature['geometry']['coordinates']
        else:
            return [None, None]
         
    def _get_row(self, feature):
        row = list(self._get_coords(feature))
        props = self._get_properties(feature)
        for value in itervalues(props):
            if isinstance(value, datetime):
                # fix mishandling of timezones on pyexcel_xlsxw
                row.append(value.replace(tzinfo=None))
            elif isinstance(value, list):
                row.append(json.dumps(value))
            else:
                row.append(value)
        return row
    
    def _get_header(self, features):
        if len(features)>0:
            props = self._get_properties(features[0])
            header = [ fname for fname in iter(props) ]
            return ['lon', 'lat'] + header
        return []
    
    def _get_properties(self, feature):
        if feature.get('properties'):
            return feature.get('properties')
        else:
            return feature
        
    def render(self, data, accepted_media_type=None, renderer_context=None):
        raise NotImplemented()