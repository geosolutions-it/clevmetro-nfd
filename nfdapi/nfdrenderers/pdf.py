# -*- coding: utf-8 -*-
'''
Created on 17 nov. 2017

@author: Alessio Fabiani
'''
import json
from easy_pdf.rendering import render_to_pdf
from collections import OrderedDict
from io import BytesIO
from pyexcel import PyExcelBaseRenderer

class PdfRenderer(PyExcelBaseRenderer):
    media_type = "application/pdf"
    format = "pdf"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        observations = []
        features = self._get_features(data)
        for record in features:
            observation = {}
            observation['first_common'] = record['species.first_common']
            observation['second_common'] = record['species.second_common']
            observation['third_common'] = record['species.third_common']
            observation['synonym'] = record['species.synonym']
            observation['family'] = record['species.family']
            observation['family_common'] = record['species.family_common']
            observation['phylum'] = record['species.phylum']
            observation['phylum_common'] = record['species.phylum_common']
            observation['tsn'] = record['species.tsn']
            observation['name_sci'] = record['species.name_sci']
            observation['geom'] = ' - '
            if record['geom']:
                geom = json.loads(record['geom'])
                observation['geom'] = geom['coordinates']
            observation['images'] = []
            if record['images']:
                observation['images'] = record['images']
            observations.append(observation)
        return render_to_pdf('pdf/sample_pdf.html', context={'observations': observations})
