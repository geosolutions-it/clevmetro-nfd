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
const GET_ANIMALS = 'GET_ANIMALS';
const GET_PLANTS = 'GET_PLANTS';
const GET_FUNGUS = 'GET_FUNGUS';
const GET_NATURAL_AREAS = 'GET_NATURAL_AREAS';
const GET_SLIME_MOLDS = 'GET_SLIME_MOLDS';
const NATURAL_FEATURE_SELECTED = 'NATURAL_FEATURE_TYPE_SELECTED';
const NATURAL_FEATURE_ERROR = 'NATURAL_FEATURE_ERROR';
const NATURAL_FEATURE_LOADED = 'NATURAL_FEATURE_LOADED';
const UPDATE_NATURAL_FEATURE_FORM = 'UPDATE_NATURAL_FEATURE_FORM';
const GET_NATURAL_FEATURE_TYPE = 'GET_NATURAL_FEATURE_TYPE';
const NATURAL_FEATURE_TYPE_LOADED = 'NATURAL_FEATURE_TYPE_LOADED';
const NATURAL_FEATURE_ADDED = 'NATURAL_FEATURE_ADDED';
const NATURAL_FEATURE_TYPE_ERROR = 'NATURAL_FEATURE_TYPE_ERROR';
const UPDATE_NATURAL_FEATURE = 'UPDATE_NATURAL_FEATURE';
const CREATE_NATURAL_FEATURE = 'CREATE_NATURAL_FEATURE';
const SAVE_NATURAL_FEATURE = 'SAVE_NATURAL_FEATURE';
const DELETE_NATURAL_FEATURE = 'DELETE_NATURAL_FEATURE';
const NATURAL_FEATURE_MARKER_ADDED = 'NATURAL_FEATURE_MARKER_ADDED';
const NATURAL_FEATURE_POLYGON_ADDED = 'NATURAL_FEATURE_POLYGON_ADDED';

const Api = require('../api/naturalfeaturesdata');
const {setControlProperty} = require('../../MapStore2/web/client/actions/controls');
const {changeDrawingStatus/*, endDrawing*/} = require('../../MapStore2/web/client/actions/draw');
const {changeLayerProperties} = require('../../MapStore2/web/client/actions/layers');

const normalizeInfo = (resp) => {
    const feature = {};
    for (let key in resp.formvalues) {
        if (key !== 'id' || key !== 'version') {
            feature[key] = resp.formvalues[key];
        }
    }
    return feature;
};

const createEmptyFeature = (featureType) => {
    const emptyFeature = {};
    featureType.map((section) => {
        section.formitems.map((item) => {
            emptyFeature[item.key] = null;
        });
    });
    return emptyFeature;
};

const formatFeature = (featuretype, featuresubtype, properties) => {
    let feature = {
        id: properties.id,
        featuretype: featuretype,
        featuresubtype: featuresubtype,
        formvalues: properties
    };

    return feature;
};

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
        type: GET_ANIMALS,
        url
    };
}

function getPlants(url) {
    return {
        type: GET_PLANTS,
        url
    };
}

function getFungus(url) {
    return {
        type: GET_FUNGUS,
        url
    };
}

function getNaturalAreas(url) {
    return {
        type: GET_NATURAL_AREAS,
        url
    };
}

function getSlimeMolds(url) {
    return {
        type: GET_SLIME_MOLDS,
        url
    };
}

function getNaturalFeatureType(url) {
    return {
        type: GET_NATURAL_FEATURE_TYPE,
        url
    };
}

function naturalFeatureTypeLoaded(forms, featuretype, featuresubtype, mode) {
    return {
        type: NATURAL_FEATURE_TYPE_LOADED,
        forms,
        featuretype,
        featuresubtype,
        mode
    };
}

function naturalFeatureTypeError(error) {
    return {
        type: NATURAL_FEATURE_TYPE_ERROR,
        error
    };
}

function updateNaturalFeatureForm(feature) {
    return {
        type: UPDATE_NATURAL_FEATURE_FORM,
        feature
    };
}

function reloadFeatureType(featuretype) {
    return (dispatch) => {
        if (featuretype === 'plant') {
            dispatch(getPlants('https://geosolutions.scolab.eu/nfdapi/layers/plant/'));
        } else if (featuretype === 'animal') {
            dispatch(getAnimals('https://geosolutions.scolab.eu/nfdapi/layers/animal/'));
        } else if (featuretype === 'fungus') {
            dispatch(getFungus('https://geosolutions.scolab.eu/nfdapi/layers/fungus/'));
        } else if (featuretype === 'slimemold') {
            dispatch(getSlimeMolds('https://geosolutions.scolab.eu/nfdapi/layers/slimemold/'));
        } else if (featuretype === 'naturalarea') {
            dispatch(getNaturalAreas('https://geosolutions.scolab.eu/nfdapi/layers/naturalarea/'));
        }
    };
}

function getFeatureInfo(properties, nfid) {
    return (dispatch) => {
        return Api.getFeatureInfo(properties.featuretype, nfid).then((resp) => {
            if (resp) {
                let feature = normalizeInfo(resp);
                dispatch(setControlProperty('addnaturalfeatures', 'enabled', false));
                dispatch(updateNaturalFeatureForm(feature));
                dispatch(setControlProperty('vieweditnaturalfeatures', 'enabled', true));
            }
        }).catch((error) => {
            dispatch(naturalFeatureTypeError('Error from REST SERVICE: ' + error.message));
        });
    };
}

function naturalFeatureSelected(properties, nfid) {
    return (dispatch) => {
        return Api.getFeatureType(properties.featuretype, nfid).then((resp) => {
            if (resp.forms && resp.forms[0]) {
                dispatch(naturalFeatureTypeLoaded(resp.forms, resp.featuretype, resp.featuresubtype, "viewedit"));
                dispatch(getFeatureInfo(properties, nfid));
            }
        }).catch((error) => {
            dispatch(naturalFeatureTypeError('Error from REST SERVICE: ' + error.message));
        });
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

function naturalFeatureAdded(error) {
    return {
        type: NATURAL_FEATURE_ADDED,
        error
    };
}

function createNaturalFeature(properties) {
    return (dispatch) => {
        if (properties.featuretype === 'plant') {
            dispatch(changeDrawingStatus("start", "Marker", "dockednaturalfeatures", [], {properties: properties, icon: '../../assets/img/marker-icon-green.png'}));
        } else if (properties.featuretype === 'animal') {
            dispatch(changeDrawingStatus("start", "Marker", "dockednaturalfeatures", [], {properties: properties, icon: '../../assets/img/marker-icon-purple.png'}));
        } else if (properties.featuretype === 'fungus') {
            dispatch(changeDrawingStatus("start", "Marker", "dockednaturalfeatures", [], {properties: properties, icon: '../../assets/img/marker-icon-yellow.png'}));
        } else if (properties.featuretype === 'slimemold') {
            dispatch(changeDrawingStatus("start", "Marker", "dockednaturalfeatures", [], {properties: properties, icon: '../../assets/img/marker-icon-marine.png'}));
        } else if (properties.featuretype === 'naturalarea') {
            dispatch(changeDrawingStatus("start", "Marker", "dockednaturalfeatures", [], {properties: properties, icon: '../../assets/img/marker-icon.png'}));
        }
    };
}

function naturalFeatureCreated(featuretype, featuresubtype, id) {
    return (dispatch) => {
        return Api.getFeatureType(featuretype, id).then((response) => {
            if (response.forms && response.forms[0]) {
                let emptyFeat = createEmptyFeature(response.forms);
                emptyFeat.id = id;
                emptyFeat.featuretype = featuretype;
                emptyFeat.featuresubtype = featuresubtype;
                dispatch(naturalFeatureTypeLoaded(response.forms, response.featuretype, response.featuresubtype, "add"));
                dispatch(setControlProperty('vieweditnaturalfeatures', 'enabled', false));
                dispatch(updateNaturalFeatureForm(emptyFeat));
                dispatch(setControlProperty('addnaturalfeatures', 'enabled', true));
            }
        }).catch((error) => {
            dispatch(naturalFeatureTypeError('Error from REST SERVICE: ' + error.message));
        });
    };
}

function naturalFeatureMarkerAdded(feature) {
    return (dispatch) => {
        dispatch(changeDrawingStatus("clean", "Marker", "dockednaturalfeatures", [], {}));
        return Api.createNewFeature(feature).then((resp) => {
            if (resp) {
                dispatch(reloadFeatureType(resp.featuretype));
                dispatch(naturalFeatureCreated(resp.featuretype, resp.featuresubtype, resp.id));
            }
        }).catch((error) => {
            dispatch(naturalFeatureTypeError('Error from REST SERVICE: ' + error.message));
        });
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

function updateNaturalFeatureLoading(id) {
    return {
        type: UPDATE_NATURAL_FEATURE,
        status: "loading",
        id
    };
}

function updateNaturalFeatureSuccess(id) {
    return {
        type: UPDATE_NATURAL_FEATURE,
        status: "success",
        id
    };
}

function updateNaturalFeatureError(id, error) {
    return {
        type: UPDATE_NATURAL_FEATURE,
        status: "error",
        id,
        error
    };
}

function updateNaturalFeature(featuretype, featuresubtype, properties) {
    return (dispatch) => {
        // dispatch(updateNaturalFeatureLoading(feature));
        const feature = formatFeature(featuretype, featuresubtype, properties);
        return Api.updateNaturalFeature(featuretype, feature).then(() => {
            dispatch(updateNaturalFeatureSuccess(properties.id));
            dispatch(reloadFeatureType(featuretype));
            dispatch(setControlProperty('vieweditnaturalfeatures', 'enabled', false));
        }).catch((error) => {
            dispatch(updateNaturalFeatureError(properties.id, error));
        });
    };
}

function deleteNaturalFeatureLoading(feature) {
    return {
        type: DELETE_NATURAL_FEATURE,
        status: "loading",
        feature
    };
}

function deleteNaturalFeatureSuccess(id) {
    return {
        type: DELETE_NATURAL_FEATURE,
        status: "success",
        id
    };
}

function deleteNaturalFeatureError(id, error) {
    return {
        type: DELETE_NATURAL_FEATURE,
        status: "error",
        id,
        error
    };
}

function deleteNaturalFeature(featuretype, id) {
    return (dispatch) => {
        return Api.deleteNaturalFeature(featuretype, id).then(() => {
            dispatch(changeLayerProperties(featuretype, {features: []}));
            dispatch(reloadFeatureType(featuretype));
            dispatch(setControlProperty('vieweditnaturalfeatures', 'enabled', false));
            dispatch(deleteNaturalFeatureSuccess(id));
        }).catch((error) => {
            dispatch(deleteNaturalFeatureError(id, error));
        });
    };
}

module.exports = {
    NATURAL_FEATURES_ERROR, naturalFeaturesError,
    NATURAL_FEATURES_LOADING, naturalFeaturesLoading,
    NATURAL_FEATURES_LOADED, naturalFeaturesLoaded,
    GET_ANIMALS, GET_PLANTS, GET_FUNGUS, GET_NATURAL_AREAS, GET_SLIME_MOLDS,
    getAnimals, getPlants, getFungus, getNaturalAreas, getSlimeMolds,
    NATURAL_FEATURE_SELECTED, naturalFeatureSelected,
    NATURAL_FEATURE_LOADED, naturalFeatureLoaded,
    NATURAL_FEATURE_ERROR, naturalFeatureError,
    UPDATE_NATURAL_FEATURE_FORM, updateNaturalFeatureForm,
    GET_NATURAL_FEATURE_TYPE, getNaturalFeatureType, reloadFeatureType,
    NATURAL_FEATURE_TYPE_LOADED, naturalFeatureTypeLoaded,
    NATURAL_FEATURE_TYPE_ERROR, naturalFeatureTypeError,
    CREATE_NATURAL_FEATURE, createNaturalFeature, naturalFeatureCreated, naturalFeatureAdded,
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
