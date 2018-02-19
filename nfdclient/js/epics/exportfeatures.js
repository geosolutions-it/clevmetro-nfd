/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/
const Rx = require('rxjs');
const Api = require('../api/naturalfeaturesdata');
const FilterUtils = require('../utils/FilterUtils');
const fileDownload = require('react-file-download');
const copy = require('copy-to-clipboard');
const url = require('url');


const {setControlProperty} = require('../../MapStore2/web/client/actions/controls');
const {
    TOGGLE_EXPORT,
    EXPORT_FEATURES,
    downloadingFeatures,
    DOWNLOAD_REPORT,
    ADD_PERMALINK
} = require('../actions/exportfeatures');
const {
    userNotAuthenticatedError
} = require('../actions/naturalfeatures');
const {error, info} = require('../../MapStore2/web/client/actions/notifications');

const getExt = (format) => {
    switch (format) {
        case 'csv':
            return 'csv';
        case 'xlsx':
            return 'xlsx';
        case 'shp':
            return 'zip';
        default :
            return 'zip';
    }
};
const exportFt = (promise, filename) => {
    return Rx.Observable.fromPromise(promise)
            .do(({data, headers}) => {
                fileDownload(data, filename, headers && headers["content-type"]);
            })
            .map(() => downloadingFeatures(false))
            .startWith(downloadingFeatures())
            .catch((e) => {
                const action = e.status === 401 ? userNotAuthenticatedError(e) : error({title: "Export error", message: `Exporting error ${e.statusText}`});
                return Rx.Observable.of(action);
            }).concat([downloadingFeatures(false)]);
};


const getReport = (promise, filename) => {
    return Rx.Observable.fromPromise(promise)
            .do(({data, headers}) => {
                fileDownload(data, filename, headers && headers["content-type"]);
            })
            .map(() => downloadingFeatures(false))
            .startWith(downloadingFeatures())
            .catch((e) => {
                const action = e.status === 401 ? userNotAuthenticatedError(e) : error({title: "Export error", message: `Exporting error ${e.statusText}`});
                return Rx.Observable.of(action);
            }).concat([downloadingFeatures(false)]);
};

module.exports = {
    toggleExport: (action$) =>
        action$.ofType(TOGGLE_EXPORT).mapTo(setControlProperty('exportfeatures', 'enabled', true)),
    exportFeature: (action$) =>
        action$.ofType(EXPORT_FEATURES)
        .filter(a => a.downloadOptions.type === "SINGLE")
        .switchMap( a => {
            const {featureType, id, selectedFormat: format, version} = a.downloadOptions;
            return exportFt(Api.exportFeature(featureType, id, version, format), `${featureType}_${id}_${version}.${getExt(format)}`);
        }),
    exportFeatureList: (action$, store) =>
        action$.ofType(EXPORT_FEATURES)
        .filter(a => a.downloadOptions.type === "LIST")
        .switchMap( a => {
            const {featureType, selectedFormat: format, singlePage } = a.downloadOptions;
            const {featuresearch} = (store.getState());
            const filters = featuresearch[`${featureType}_filters`];
            let filter = '';
            if (filters) {
                filter = FilterUtils.getFilter({operator: featuresearch.defaultOperator, ...filters});
            }
            const page = singlePage && featuresearch[featureType] && featuresearch[featureType].page ? `&page=${featuresearch[featureType].page}` : '';
            return exportFt(Api.exportFeatureList(featureType, format, filter, page), `${featureType}.${getExt(format)}`);
        }),
    downloadReport: (action$) =>
        action$.ofType(DOWNLOAD_REPORT)
        .switchMap(a => {
            const {featureType, id, version} = a;
            return getReport(Api.downloadReport(featureType, id, version), `${featureType}${id ? `_${id}_${version}` : ''}.${'pdf'}`);
        }),
    addPermalink: (action$) =>
        action$.ofType(ADD_PERMALINK)
        .switchMap(({ft, sb, id, v}) => {
            let currentUrl = url.parse(window.location.href, true);
            currentUrl.query = {...currentUrl.query, ft, sb, id, v};
            delete currentUrl.search;
            delete currentUrl.hash;
            const link = url.format(currentUrl);
            copy(link);
            return Rx.Observable.of(info({title: "Link", message: `Permalink adde to clipboard ${link}`}));
        })
};
