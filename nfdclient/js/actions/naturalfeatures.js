/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const NATURAL_FEATURES_ERROR = 'NATURAL_FEATURES_ERROR';
const NATURAL_FEATURES_LOADING = 'NATURAL_FEATURES_LOADING';
const NATURAL_FEATURES_LOADED = 'NATURAL_FEATURES_LOADED';
const GET_NATURAL_FEATURES = 'GET_NATURAL_FEATURES';
const NATURAL_FEATURE_SELECTED = 'NATURAL_FEATURE_TYPE_SELECTED';
const NATURAL_FEATURE_ERROR = 'NATURAL_FEATURE_ERROR';
const NATURAL_FEATURE_LOADED = 'NATURAL_FEATURE_LOADED';
const UPDATE_NATURAL_FEATURE_FORM = 'UPDATE_NATURAL_FEATURE_FORM';
const GET_NATURAL_FEATURE_TYPE = 'GET_NATURAL_FEATURE_TYPE';
const NATURAL_FEATURE_TYPE_LOADED = 'NATURAL_FEATURE_TYPE_LOADED';
const NATURAL_FEATURE_TYPE_ERROR = 'NATURAL_FEATURE_TYPE_ERROR';
const UPDATE_NATURAL_FEATURE = 'UPDATE_NATURAL_FEATURE';
const CREATE_NATURAL_FEATURE = 'CREATE_NATURAL_FEATURE';
const NATURAL_FEATURE_CREATED = 'NATURAL_FEATURE_CREATED';
const SAVE_NATURAL_FEATURE = 'SAVE_NATURAL_FEATURE';
const DELETE_NATURAL_FEATURE = 'DELETE_NATURAL_FEATURE';
const NATURAL_FEATURE_MARKER_ADDED = 'NATURAL_FEATURE_MARKER_ADDED';
const NATURAL_FEATURE_POLYGON_ADDED = 'NATURAL_FEATURE_POLYGON_ADDED';

const Api = require('../api/naturalfeaturesdata');
const {setControlProperty} = require('../../MapStore2/web/client/actions/controls');

function naturalFeaturesError(error) {
    return {
        type: NATURAL_FEATURES_ERROR,
        error
    };
}

function naturalFeaturesLoading() {
    return {
        type: NATURAL_FEATURES_LOADING
    };
}

function naturalFeaturesLoaded(data, url) {
    return {
        type: NATURAL_FEATURES_LOADED,
        data,
        url
    };
}

function getAnimals(url) {
    return {
        type: GET_NATURAL_FEATURES,
        url
    };
}

function getMushrooms(url) {
    return {
        type: GET_NATURAL_FEATURES,
        url
    };
}

function getNaturalFeatureType(url) {
    return {
        type: GET_NATURAL_FEATURE_TYPE,
        url
    };
}

function naturalFeatureTypeLoaded(featureType, properties, mode) {
    return {
        type: NATURAL_FEATURE_TYPE_LOADED,
        featureType,
        properties,
        mode
    };
}

function naturalFeatureTypeError(error) {
    return {
        type: NATURAL_FEATURE_TYPE_ERROR,
        error
    };
}

function naturalFeatureSelected(properties, msId) {
    return {
        type: NATURAL_FEATURE_SELECTED,
        properties,
        msId
    };
}

function naturalFeatureLoaded(feature) {
    return {
        type: NATURAL_FEATURE_LOADED,
        feature
    };
}

function naturalFeatureError(error) {
    return {
        type: NATURAL_FEATURE_ERROR,
        error
    };
}

function createNaturalFeature(msId) {
    return {
        type: CREATE_NATURAL_FEATURE,
        msId
    };
}

function naturalFeatureCreated(featureType) {
    return {
        type: NATURAL_FEATURE_CREATED,
        featureType
    };
}

function addNaturalFeature(msId) {
    return (dispatch) => {
        dispatch(createNaturalFeature(msId));
        dispatch(setControlProperty('addnaturalfeatures', 'enabled', true));
    };
}

function naturalFeatureMarkerAdded(geometry) {
    return {
        type: NATURAL_FEATURE_MARKER_ADDED,
        geometry
    };
}

function naturalFeaturePolygonAdded(geometry) {
    return {
        type: NATURAL_FEATURE_POLYGON_ADDED,
        geometry
    };
}

function saveNaturalFeatureLoading(feature) {
    return {
        type: SAVE_NATURAL_FEATURE,
        status: "loading",
        feature
    };
}

function saveNaturalFeatureSuccess(feature) {
    return {
        type: SAVE_NATURAL_FEATURE,
        status: "success",
        feature
    };
}

function saveNaturalFeatureError(feature, error) {
    return {
        type: SAVE_NATURAL_FEATURE,
        status: "error",
        feature,
        error
    };
}

function saveNaturalFeature(feature) {
    return (dispatch) => {
        if (feature) {
            dispatch(saveNaturalFeatureLoading(feature));
            return Api.saveNaturalFeature(feature).then((resp) => {
                dispatch(saveNaturalFeatureSuccess(resp));
            }).catch((error) => {
                dispatch(saveNaturalFeatureError(feature, error));
            });
        }
    };
}

function updateNaturalFeatureForm(feature) {
    return {
        type: UPDATE_NATURAL_FEATURE_FORM,
        feature
    };
}

function updateNaturalFeatureLoading(feature) {
    return {
        type: UPDATE_NATURAL_FEATURE,
        status: "loading",
        feature
    };
}

function updateNaturalFeatureSuccess(feature) {
    return {
        type: UPDATE_NATURAL_FEATURE,
        status: "success",
        feature
    };
}

function updateNaturalFeatureError(feature, error) {
    return {
        type: UPDATE_NATURAL_FEATURE,
        status: "error",
        feature,
        error
    };
}

function updateNaturalFeature(feature) {
    return (dispatch) => {
        if (feature) {
            dispatch(updateNaturalFeatureLoading(feature));
            return Api.updateNaturalFeature(feature).then((resp) => {
                dispatch(updateNaturalFeatureSuccess(resp));
            }).catch((error) => {
                dispatch(updateNaturalFeatureError(feature, error));
            });
        }
    };
}

function deleteNaturalFeatureLoading(feature) {
    return {
        type: DELETE_NATURAL_FEATURE,
        status: "loading",
        feature
    };
}

function deleteNaturalFeatureSuccess(feature) {
    return {
        type: DELETE_NATURAL_FEATURE,
        status: "success",
        feature
    };
}

function deleteNaturalFeatureError(feature, error) {
    return {
        type: DELETE_NATURAL_FEATURE,
        status: "error",
        feature,
        error
    };
}

function deleteNaturalFeature(feature) {
    return (dispatch) => {
        if (feature) {
            dispatch(deleteNaturalFeatureLoading(feature));
            return Api.deleteNaturalFeature(feature).then((resp) => {
                dispatch(deleteNaturalFeatureSuccess(resp));
            }).catch((error) => {
                dispatch(deleteNaturalFeatureError(feature, error));
            });
        }
    };
}

module.exports = {
    NATURAL_FEATURES_ERROR, naturalFeaturesError,
    NATURAL_FEATURES_LOADING, naturalFeaturesLoading,
    NATURAL_FEATURES_LOADED, naturalFeaturesLoaded,
    GET_NATURAL_FEATURES, getAnimals, getMushrooms,
    NATURAL_FEATURE_SELECTED, naturalFeatureSelected,
    NATURAL_FEATURE_LOADED, naturalFeatureLoaded,
    NATURAL_FEATURE_ERROR, naturalFeatureError,
    UPDATE_NATURAL_FEATURE_FORM, updateNaturalFeatureForm,
    GET_NATURAL_FEATURE_TYPE, getNaturalFeatureType,
    NATURAL_FEATURE_TYPE_LOADED, naturalFeatureTypeLoaded,
    NATURAL_FEATURE_TYPE_ERROR, naturalFeatureTypeError,
    CREATE_NATURAL_FEATURE, addNaturalFeature, createNaturalFeature,
    NATURAL_FEATURE_CREATED, naturalFeatureCreated,
    SAVE_NATURAL_FEATURE, saveNaturalFeature,
    saveNaturalFeatureLoading, saveNaturalFeatureSuccess,
    saveNaturalFeatureError,
    UPDATE_NATURAL_FEATURE, updateNaturalFeature,
    updateNaturalFeatureLoading, updateNaturalFeatureSuccess,
    updateNaturalFeatureError,
    DELETE_NATURAL_FEATURE, deleteNaturalFeature,
    deleteNaturalFeatureLoading, deleteNaturalFeatureSuccess,
    deleteNaturalFeatureError,
    NATURAL_FEATURE_MARKER_ADDED, naturalFeatureMarkerAdded,
    NATURAL_FEATURE_POLYGON_ADDED, naturalFeaturePolygonAdded
};
