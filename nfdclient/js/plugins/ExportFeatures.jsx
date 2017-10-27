/*
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const {connect} = require('react-redux');
const {downloadFeatures, onDownloadOptionChange} = require('../actions/exportfeatures');
const {toggleControl} = require('../../MapStore2/web/client/actions/controls');

const {createSelector} = require('reselect');

const DownloadDialog = require('../ms2Override/DownloadDialog');
/**
 * Provides advanced export functionalities using WFS.
 * @memberof plugins
 * @name WFSDownload
 * @class
 * @prop {object[]} formats An array of name-label objects for the allowed formats available.
 * @prop {object[]} srsList An array of name-label objects for the allowed srs available. Use name:'native' to omit srsName param in wfs filter
 * @prop {string} defaultSrs Deafult selected srs
 * @prop {string} closeGlyph The icon to use for close the dialog
 * @example
 * {
 *  "name": "exportfeatures",
 *  "cfg": {
 *    "formats": [
 *            {"name": "csv", "label": "csv"},
 *            {"name": "shape-zip", "label": "shape-zip"},
 *            {"name": "excel", "label": "excel"},
 *            {"name": "excel2007", "label": "excel2007"},
 *            {"name": "dxf-zip", "label": "dxf-zip"}
 *    ]
 *  }
 * }
 */
module.exports = {
    ExportFeaturesPlugin: connect(createSelector(
            state => state && state.controls && state.controls.exportfeatures && state.controls.exportfeatures.enabled,
            state => state && state.exportfeatures && state.exportfeatures.options,
            state => state && state.exportfeatures && state.exportfeatures.downloading,
            ( enabled, downloadOptions, loading) => ({
                enabled,
                downloadOptions,
                loading
            })
    ), {
        onDownloadOptionChange,
        onExport: downloadFeatures,
        onClose: () => toggleControl("exportfeatures")
    }
)(DownloadDialog),
    epics: require('../epics/exportfeatures'),
    reducers: {
        exportfeatures: require('../reducers/exportfeatures')
    }
};
