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
    NATURAL_FEATURE_MARKER_REPLACED,
    ADD_FEATURE,
    END_EDITING,
    EDIT_FEATURE,
    VIEW_FEATURE,
    NF_CLICKED
} = require('../actions/naturalfeatures');

function naturalfeatures(state = {}, action) {
    switch (action.type) {
        case "LOGOUT": {
            return assign({}, state, {featuretype: undefined, featuresubtype: undefined, selectedFeature: {}, newFeature: {}, error: {}, mode: undefined});
        }
        case NATURAL_FEATURE_TYPE_LOADED: {
            return assign({}, state, {
                forms: action.forms,
                featuretype: action.featuretype,
                featuresubtype: action.featuresubtype
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
        case ADD_FEATURE:
            return assign({}, state, {mode: 'ADD'});
        case EDIT_FEATURE:
            return assign({}, state, {mode: 'EDIT'});
        case VIEW_FEATURE:
            return assign({}, state, {mode: 'VIEW'});
        case END_EDITING:
            return assign({}, state, {mode: undefined, froms: [], featuretype: "", featuresubtype: "", selectedFeature: {}, errors: {}, newFeature: {}});
        case NF_CLICKED:
            return assign({}, state, {nfclicked: action.nfId});
        default:
            return state;
    }
}

module.exports = naturalfeatures;
