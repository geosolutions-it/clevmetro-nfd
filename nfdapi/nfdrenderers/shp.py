# -*- coding: utf-8 -*-
'''
Created on 10 oct. 2017

@author: Cesar Martinez Izquierdo
'''

import shapefile
import six
import datetime
from rest_framework.renderers import BaseRenderer
import json
from io import BytesIO
from zipfile import ZipFile
from builtins import str as text
from collections import OrderedDict

WKT_ESRI_4326 = """GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]"""

class ShpRenderer(BaseRenderer):
    #media_type = "application/x-shapefile"
    media_type = "application/zip"
    format = "shp"
    charset = None
    render_style = 'binary'

    def _get_features(self, data):
        if data.get('features'):
            return data.get('features')
        if data.get('results'):
            return data.get('results').get('features')
        return [data]

    def _get_properties(self, feature):
        if feature.get('properties'):
            return feature.get('properties')
        else:
            return feature

    def _get_field_def(self, features):
        field_dict = OrderedDict()
        field_def = []
        if len(features)>0:
            props = self._get_properties(features[0])
            for (key, value) in six.iteritems(props):
                if isinstance(key, six.text_type):
                    key = key.encode('utf-8')
                #if isinstance(key, six.binary_type):
                #    key = key.decode('utf-8')
                if isinstance(value, datetime.date) or isinstance(value, datetime.datetime):
                    field_def.append((key, "D"))
                    field_dict[key] = "D"
                elif isinstance(value, six.integer_types):
                    field_def.append((key, "N", 19))
                    field_dict[key] = "N"
                elif isinstance(value, float):
                    field_def.append((key, "N", 25, 5))
                    field_dict[key] = "N"
                else:
                    field_def.append((key, "C", 254))
                    field_dict[key] = "C"
        return (field_def, field_dict)

    def _get_row(self, feature, fdef):
        row = []
        props = self._get_properties(feature)
        for (fname, value) in six.iteritems(props):
            if fdef.get(fname):
                ftype = fdef.get(fname)[0]
                if ftype == 'C':
                    if isinstance(value, six.text_type):
                        row.append(value)
                    elif isinstance(value, list):
                        row.append(json.dumps(value))
                    else:
                        row.append(text(value))
                else:
                    row.append(value)
                """
                elif ftype == 'N':
                    if isinstance(value, six.integer_types) or isinstance(value, float):
                        row.append(value)
                elif ftype == 'D':
                # fix mishandling of timezones on pyexcel_xlsxw
                row.append(value.replace(tzinfo=None))
                """
        return row

    def _get_coords(self, feature):
        if feature.get("geometry"):
            return feature['geometry']['coordinates']
        elif feature.get("geom"):
            if isinstance(feature['geom'], six.string_types):
                geom_as_dict = json.loads(feature['geom'])
                return geom_as_dict['coordinates']
            return feature['geom']['coordinates']
        else:
            return [None, None]

    def render(self, data, accepted_media_type=None, renderer_context=None):
        w = shapefile.Writer(shapeType=shapefile.POINT)
        features = self._get_features(data)
        (dbf_def, field_dict) = self._get_field_def(features)
        for fdef in dbf_def:
            w.field(*fdef)
        for feature in features:
            w.record(*self._get_row(feature, field_dict))
            coords = self._get_coords(feature)
            w.point(coords[0], coords[1])

        # creating on memory shp, shx and dbf
        shp = BytesIO()
        shx = BytesIO()
        dbf = BytesIO()
        prj = WKT_ESRI_4326.encode("latin1")
        w.saveShp(shp)
        w.saveShx(shx)
        w.saveDbf(dbf)

        # packaging the shp in a zipfile
        with BytesIO() as zipbuffer:
            zip_writer = ZipFile(zipbuffer, 'w')
            zip_writer.writestr("nfdexport.shp", shp.getvalue())
            shp.close()
            zip_writer.writestr("nfdexport.shx", shx.getvalue())
            shx.close()
            zip_writer.writestr("nfdexport.dbf", dbf.getvalue())
            dbf.close()
            zip_writer.writestr("nfdexport.prj", prj)
            zip_writer.close()
            return zipbuffer.getvalue()