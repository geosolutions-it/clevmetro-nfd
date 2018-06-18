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
const INITIALIZE_REPORT_FILTERS = 'INITIALIZE_REPORT_FILTERS';
const UPDATE_REPORT_FILTERS = 'UPDATE_REPORT_FILTERS';
const UPDATE_REPORT_OPTIONS = 'UPDATE_REPORT_OPTIONS';
const DOWNLOAD_REPORT = 'DOWNLOAD_REPORT';
const DOWNLOAD_REPORT_WITH_FILTER = 'DOWNLOAD_REPORT_WITH_FILTER';
const ADD_PERMALINK = 'ADD_PERMALINK';

function addPermalink(ft, sb, id, v) {
    return {
        type: ADD_PERMALINK,
        ft,
        id,
        sb,
        v
    };
}

function initializeReportFilters(filters) {
    return {
        type: INITIALIZE_REPORT_FILTERS,
        filters
    };
}

function updateReportFilters(filter, filters) {
    return {
        type: UPDATE_REPORT_FILTERS,
        filter,
        filters
    };
}

function updateReportOptions(options) {
    return {
        type: UPDATE_REPORT_OPTIONS,
        options
    };
}

function downloadReportWithFilter(featureType, id, version) {
    return {
        type: DOWNLOAD_REPORT_WITH_FILTER,
        featureType,
        id,
        version
    };
}

function downloadReport(featureType, id, version) {
    return {
        type: DOWNLOAD_REPORT,
        featureType,
        id,
        version
    };
}

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
function onToggleExport(exportType, featureType, id, version) {
    return {
        type: TOGGLE_EXPORT,
        exportType,
        featureType,
        id,
        version
    };
}

module.exports = {
    TOGGLE_EXPORT, onToggleExport,
    EXPORT_OPTIONS_CHANGE, onDownloadOptionChange,
    EXPORT_FEATURES, downloadFeatures,
    DOWNLOADING_FEATURES, downloadingFeatures,
    DOWNLOADING_FEATURES_ERROR, downloadingError,
    INITIALIZE_REPORT_FILTERS, initializeReportFilters,
    UPDATE_REPORT_FILTERS, updateReportFilters,
    UPDATE_REPORT_OPTIONS, updateReportOptions,
    DOWNLOAD_REPORT, downloadReport,
    DOWNLOAD_REPORT_WITH_FILTER, downloadReportWithFilter,
    ADD_PERMALINK, addPermalink
};
