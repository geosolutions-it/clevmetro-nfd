# -*- coding: utf-8 -*-
'''
Created on 10 oct. 2017

@author: Cesar Martinez Izquierdo
'''
    
from pyexcel_xlsxw import save_data
from collections import OrderedDict
from io import BytesIO
from pyexcel import PyExcelBaseRenderer

class XlsxRenderer(PyExcelBaseRenderer):
    media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    format = "xlsx"
    charset = None
    render_style = 'binary'
        
    def render(self, data, accepted_media_type=None, renderer_context=None):
        sheet_data = OrderedDict()
        features = self._get_features(data)
        matrix = [self._get_header(features)]
        for record in features:
            matrix.append(self._get_row(record))
        sheet_data.update({"Sheet 1": matrix})
        with BytesIO() as xlsx_io: 
            save_data(xlsx_io, sheet_data)
            return xlsx_io.getvalue()
