/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const assign = require('object-assign');
const {isObject} = require('lodash');

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
    NF_CLICKED,
    ADD_IMAGE,
    REMOVE_IMAGE,
    IMAGE_UPLOADED,
    FEATURE_PROPERTY_CHANGE,
    NATURAL_FEATURES_LOADING
} = require('../actions/naturalfeatures');


function naturalfeatures(state = {}, action) {
    switch (action.type) {
        case "CLEAN_FORM": {
            return assign({}, state, {featuretype: undefined, featuresubtype: undefined, selectedFeature: {}, newFeature: {}, errors: {}, forms: [], images: []});
        }
        case "LOGOUT": {
            return assign({}, state, {featuretype: undefined, featuresubtype: undefined, selectedFeature: {}, newFeature: {}, errors: {}, mode: undefined, loading: false, forms: [], images: []});
        }
        case NATURAL_FEATURE_TYPE_LOADED: {
            return assign({}, state, {
                forms: action.forms,
                featuretype: action.featuretype,
                featuresubtype: action.featuresubtype
            });
        }
        case UPDATE_NATURAL_FEATURE_FORM: {
            let newF = isObject(action.feature.geom) ? action.feature : assign({}, action.feature, {geom: JSON.parse(action.feature.geom)});
            newF = assign({}, newF, {"location.lat": newF.geom && newF.geom.coordinates[1], "location.lng": newF.geom && newF.geom.coordinates[0]});
            return assign({}, state, {
                selectedFeature: newF,
                images: newF.images || [],
                errors: {}
            });
        }
        case CREATE_NATURAL_FEATURE_ERROR:
        case UPDATE_NATURAL_FEATURE_ERROR: {
            if (action.error.response.status >= 500) {
                return assign({}, state, {
                    errors: { badrequest: [action.error.statusText] }
                });
            }
            return assign({}, state, {
                errors: action.error.response.data
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
            const selectedFeature = assign({}, state.selectedFeature, {geom: action.geometry, "location.lng": action.geometry && action.geometry.coordinates[0], "location.lat": action.geometry && action.geometry.coordinates[1]});
            return assign({}, state, {
                selectedFeature: selectedFeature
            });
        }
        case FEATURE_PROPERTY_CHANGE: {

            let selectedFeature = assign({}, state.selectedFeature, {[action.property]: action.value});
            if (action.property === "location.lng" || action.property === "location.lat") {
                const lat = action.property === "location.lat" ? parseFloat(action.value) : selectedFeature.geom.coordinates[1];
                const lng = action.property === "location.lng" ? parseFloat(action.value) : selectedFeature.geom.coordinates[0];
                const geom = assign({}, selectedFeature.geom, {coordinates: [lng, lat]});
                selectedFeature = assign({}, selectedFeature, {geom});
            }
            return assign({}, state, {selectedFeature});
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
        case ADD_IMAGE: {
            const image = assign({}, action.image, {loading: true});
            const images = [image].concat((state.selectedFeature.images || []));
            const selectedFeature = assign({}, state.selectedFeature, {images});
            return assign({}, state, {selectedFeature});
        }
        case IMAGE_UPLOADED: {
            const images = action.images.concat(state.selectedFeature.images.slice(1));
            const selectedFeature = assign({}, state.selectedFeature, {images});
            return assign({}, state, {selectedFeature});
        }
        case REMOVE_IMAGE: {
            const images = state.selectedFeature.images.filter((a, idx) => idx !== action.idx);
            const selectedFeature = assign({}, state.selectedFeature, {images});
            return assign({}, state, {selectedFeature});
        }
        case NATURAL_FEATURES_LOADING: {
            return assign({}, state, {loading: action.loading});
        }
        default:
            return state;
    }
}

module.exports = naturalfeatures;
