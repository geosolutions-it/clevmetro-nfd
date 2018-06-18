/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const assign = require('object-assign');
const {isString} = require('lodash');
const {
 TOGGLE_EXPORT,
 EXPORT_OPTIONS_CHANGE,
 DOWNLOADING_FEATURES,
 UPDATE_REPORT_FILTERS,
 UPDATE_REPORT_OPTIONS
} = require('../actions/exportfeatures');

function exportfeatures(state = {}, action) {
    switch (action.type) {
        case TOGGLE_EXPORT: {
            const {exportType: type, featureType, id, version} = action;
            const options = assign({}, state.options, {type, featureType, id, version});
            return assign({}, state, {options});
        }
        case EXPORT_OPTIONS_CHANGE: {
            const options = assign({}, state.options, {[action.key]: action.value});
            return assign({}, state, {options});
        }
        case DOWNLOADING_FEATURES: {
            return assign({}, state, {
                downloading: action.downloading,
                reportOptions: !action.downloading ? null : state.reportOptions && {...state.reportOptions} || null
            });
        }
        case UPDATE_REPORT_FILTERS: {
            const filters = state.reportFilters && {...state.reportFilters} || action.filters && {...action.filters} || {};
            const row = (filters.row && [...filters.row] || []).map((filter) => {
                if (action.filter && filter.code === action.filter.code) {
                    return {...action.filter};
                }
                return {...filter};
            });
            return assign({}, state, {
                reportFilters: {
                    ...filters,
                    row
                }
            });
        }
        case UPDATE_REPORT_OPTIONS: {
            if (isString(action.options)) {
                const downloadReportUrls = {
                    plant: '/nfdapi/report_taxon/',
                    fungus: '/nfdapi/report_taxon/',
                    animal: '/nfdapi/report_taxon/',
                    slime_mold: '/nfdapi/report_taxon/',
                    naturalarea: '/nfdapi/report_natural_area/'
                };
                return assign({}, state, {
                    reportOptions: {
                        featureType: action.options,
                        downloadReportUrl: downloadReportUrls[action.options] || '/nfdapi/report_taxon/'
                    }
                });
            }
            if (action.options && action.options.downloaded) {
                return assign({}, state, {reportOptions: null});
            }
            const options = action.options || {};
            const reportOptions = state.reportOptions && {...state.reportOptions, ...options} || {...options};
            return assign({}, state, {reportOptions});
        }
        default:
            return state;
    }
}

module.exports = exportfeatures;
