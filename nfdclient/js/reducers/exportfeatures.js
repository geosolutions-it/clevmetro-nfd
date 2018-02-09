/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const assign = require('object-assign');
const {
 TOGGLE_EXPORT,
 EXPORT_OPTIONS_CHANGE,
 DOWNLOADING_FEATURES
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
            return assign({}, state, {downloading: action.downloading});
        }
        default:
            return state;
    }
}

module.exports = exportfeatures;
