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
    UPDATE_NATURAL_FEATURE_ERROR
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
                selectedFeature: action.feature
            });
        }
        case UPDATE_NATURAL_FEATURE_ERROR: {
            return assign({}, state, {
                errors: action.error.data
            });
        }
        default:
            return state;
    }
}

module.exports = naturalfeatures;
