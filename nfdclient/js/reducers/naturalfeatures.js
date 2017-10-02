/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const assign = require('object-assign');
const {
    NATURAL_FEATURE_TYPE_LOADED,
    UPDATE_NATURAL_FEATURE_FORM,
    UPDATE_NATURAL_FEATURE_ERROR,
    CREATE_NATURAL_FEATURE_ERROR,
    UPDATE_SPECIES_FORMS,
    NATURAL_FEATURE_POLYGON_REPLACED,
    NATURAL_FEATURE_MARKER_REPLACED
} = require('../actions/naturalfeatures');

function naturalfeatures(state = {}, action) {
    switch (action.type) {
        case NATURAL_FEATURE_TYPE_LOADED: {
            return assign({}, state, {
                forms: action.forms,
                featuretype: action.featuretype,
                featuresubtype: action.featuresubtype,
                mode: action.mode
            });
        }
        case UPDATE_NATURAL_FEATURE_FORM: {
            return assign({}, state, {
                selectedFeature: action.feature,
                errors: {}
            });
        }
        case CREATE_NATURAL_FEATURE_ERROR:
        case UPDATE_NATURAL_FEATURE_ERROR: {
            if (action.error.status >= 500) {
                return assign({}, state, {
                    errors: { badrequest: [action.error.statusText] }
                });
            }
            return assign({}, state, {
                errors: action.error.data
            });
        }
        case UPDATE_SPECIES_FORMS: {
            const selectedFeature = assign({}, state.selectedFeature, action.feature);
            return assign({}, state, {
                selectedFeature: selectedFeature
            });
        }
        case NATURAL_FEATURE_POLYGON_REPLACED: {
            const selectedFeature = assign({}, state.selectedFeature, {polygon: action.geometry});
            return assign({}, state, {
                selectedFeature: selectedFeature
            });
        }
        case NATURAL_FEATURE_MARKER_REPLACED: {
            const selectedFeature = assign({}, state.selectedFeature, {geom: action.geometry});
            return assign({}, state, {
                selectedFeature: selectedFeature
            });
        }
        default:
            return state;
    }
}

module.exports = naturalfeatures;
