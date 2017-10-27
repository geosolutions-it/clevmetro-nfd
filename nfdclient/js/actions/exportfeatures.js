/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/
const TOGGLE_EXPORT = 'TOGGLE_EXPORT';
const EXPORT_OPTIONS_CHANGE = 'EXPORT_OPTIONS_CHANGE';
const EXPORT_FEATURES = 'EXPORT_FEATURES';
const DOWNLOADING_FEATURES = 'DOWNLOADING_FEATURES';
const DOWNLOADING_FEATURES_ERROR = 'DOWNLOADING_FEATURES_ERROR';

function downloadingError(e) {
    return {
        type: DOWNLOADING_FEATURES_ERROR,
        e
    };
}

function downloadingFeatures(downloading = true) {
    return {
        type: DOWNLOADING_FEATURES,
        downloading
    };
}

function downloadFeatures(downloadOptions) {
    return {
        type: EXPORT_FEATURES,
        downloadOptions
    };
}

function onDownloadOptionChange(key, value) {
    return {
        type: EXPORT_OPTIONS_CHANGE,
        key,
        value
    };
}
function onToggleExport(exportType, featureType, id ) {
    return {
        type: TOGGLE_EXPORT,
        exportType,
        featureType,
        id
    };
}

module.exports = {
    TOGGLE_EXPORT, onToggleExport,
    EXPORT_OPTIONS_CHANGE, onDownloadOptionChange,
    EXPORT_FEATURES, downloadFeatures,
    DOWNLOADING_FEATURES, downloadingFeatures,
    DOWNLOADING_FEATURES_ERROR, downloadingError
};
