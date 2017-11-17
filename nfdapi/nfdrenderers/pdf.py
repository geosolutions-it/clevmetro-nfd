# -*- coding: utf-8 -*-
'''
Created on 17 nov. 2017

@author: Alessio Fabiani
'''

import easy_pdf
from collections import OrderedDict
from io import BytesIO
from pyexcel import PyExcelBaseRenderer

class PdfRenderer(PyExcelBaseRenderer):
    media_type = "application/pdf"
    format = "pdf"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        sheet_data = OrderedDict()
        features = self._get_features(data)
        matrix = [self._get_header(features)]
        for record in features:
            matrix.append(self._get_row(record))
        sheet_data.update({"Sheet 1": matrix})
        return easy_pdf.rendering.render_to_pdf('hello_pdf.html', context={})
