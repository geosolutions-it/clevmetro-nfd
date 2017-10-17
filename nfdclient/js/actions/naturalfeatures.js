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
const UPDATE_SPECIES_FORMS = 'UPDATE_SPECIES_FORMS';
const GET_NATURAL_FEATURE_TYPE = 'GET_NATURAL_FEATURE_TYPE';
const NATURAL_FEATURE_TYPE_LOADED = 'NATURAL_FEATURE_TYPE_LOADED';
const NATURAL_FEATURE_ADDED = 'NATURAL_FEATURE_ADDED';
const NATURAL_FEATURE_TYPE_ERROR = 'NATURAL_FEATURE_TYPE_ERROR';
const UPDATE_NATURAL_FEATURE = 'UPDATE_NATURAL_FEATURE';
const CREATE_NATURAL_FEATURE = 'CREATE_NATURAL_FEATURE';
const DELETE_NATURAL_FEATURE = 'DELETE_NATURAL_FEATURE';
const NATURAL_FEATURE_MARKER_ADDED = 'NATURAL_FEATURE_MARKER_ADDED';
const NATURAL_FEATURE_POLYGON_REPLACED = 'NATURAL_FEATURE_POLYGON_REPLACED';
const NATURAL_FEATURE_MARKER_REPLACED = 'NATURAL_FEATURE_MARKER_REPLACED';
const UPDATE_NATURAL_FEATURE_ERROR = 'UPDATE_NATURAL_FEATURE_ERROR';
const CREATE_NATURAL_FEATURE_ERROR = 'CREATE_NATURAL_FEATURE_ERROR';
const NFD_LOGIN_SUCCESS = 'NFD_LOGIN_SUCCESS';
const USER_NOT_AUTHENTICATED_ERROR = 'USER_NOT_AUTHENTICATED_ERROR';

const Api = require('../api/naturalfeaturesdata');
const {setControlProperty} = require('../../MapStore2/web/client/actions/controls');
const {changeDrawingStatus} = require('../../MapStore2/web/client/actions/draw');
const {changeLayerProperties} = require('../../MapStore2/web/client/actions/layers');
const {loginFail, logout} = require('../../MapStore2/web/client/actions/security');
const assign = require('object-assign');

const ADD_FEATURE = 'ADD_FEATURE';
const EDIT_FEATURE = 'EDIT_FEATURE';
const VIEW_FEATURE = 'VIEW_FEATURE';
const END_EDITING = 'END_EDITING';
const NF_CLICKED = 'NF_CLICKED';
const CANCEL_EDITING = 'CANCEL_EDITING';
const EDIT_FEATURE_CLICKED = 'EDIT_FEATURE_CLICKED';

function editClicked(ftId) {
    return {
        type: EDIT_FEATURE_CLICKED,
        ftId
    };
}

function endEditing() {
    return {
        type: END_EDITING
    };
}
function viewFeature() {
    return {
        type: VIEW_FEATURE
    };
}
function onNfClick(properties, nfId, layer) {
    return {
        type: NF_CLICKED,
        properties,
        nfId,
        layer
    };
}
function cancel() {
    return {
        type: CANCEL_EDITING
    };
}
function editFeature(properties) {
    return {
        type: EDIT_FEATURE,
        properties
    };
}

function addFeature(properties) {
    return {
        type: ADD_FEATURE,
        properties
    };
}


const normalizeInfo = (resp) => {
    return resp;
};

const createEmptyFormValues = (featureType) => {
    const formvalues = {};
    featureType.map((section) => {
        section.formitems.map((item) => {
            formvalues[item.key] = null;
        });
    });
    return formvalues;
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

function updateSpeciesForms(feature) {
    return {
        type: UPDATE_SPECIES_FORMS,
        feature
    };
}

function userNotAuthenticatedError(error) {
    return {
        type: USER_NOT_AUTHENTICATED_ERROR,
        status: "error",
        error
    };
}

function reloadFeatureType(featuretype) {
    return (dispatch) => {
        if (featuretype === 'plant') {
            dispatch(getPlants('/nfdapi/layers/plant/'));
        } else if (featuretype === 'animal') {
            dispatch(getAnimals('/nfdapi/layers/animal/'));
        } else if (featuretype === 'fungus') {
            dispatch(getFungus('/nfdapi/layers/fungus/'));
        } else if (featuretype === 'slimemold') {
            dispatch(getSlimeMolds('/nfdapi/layers/slimemold/'));
        } else if (featuretype === 'naturalarea') {
            dispatch(getNaturalAreas('/nfdapi/layers/naturalarea/'));
        }
    };
}

function getFeatureInfo(properties, nfid, action) {
    return (dispatch) => {
        return Api.getFeatureInfo(properties.featuretype, nfid).then((resp) => {
            if (resp) {
                let feature = normalizeInfo(resp);
                dispatch(updateNaturalFeatureForm(feature));
                dispatch(action);
                dispatch(changeDrawingStatus("selectionGeomLoaded", "Marker", "dockednaturalfeatures", [], {properties: resp}));
            }
        }).catch((error) => {
            if (error.status === 401) {
                return dispatch(userNotAuthenticatedError(error));
            }
            return dispatch(naturalFeatureTypeError('Error from REST SERVICE: ' + error.message));
        });
    };
}

function getSpecies(id) {
    return (dispatch) => {
        return Api.getSpecies(id).then((resp) => {
            if (resp) {
                dispatch(updateSpeciesForms(resp));
            }
        }).catch((error) => {
            if (error.status === 401) {
                return dispatch(userNotAuthenticatedError(error));
            }
            return dispatch(naturalFeatureTypeError('Error from REST SERVICE: ' + error.message));
        });
    };
}

function naturalFeatureSelected(properties, nfid, action) {
    return (dispatch) => {
        return Api.getFeatureSubtype(properties.featuresubtype).then((resp) => {
            if (resp.forms && resp.forms[0]) {
                dispatch(naturalFeatureTypeLoaded(resp.forms, resp.featuretype, resp.featuresubtype, "viewedit"));
                dispatch(getFeatureInfo(properties, nfid, action));
            }
        }).catch((error) => {
            if (error.status === 401) {
                return dispatch(userNotAuthenticatedError(error));
            }
            return dispatch(naturalFeatureTypeError('Error from REST SERVICE: ' + error.message));
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

function naturalFeatureMarkerAdded(feature) {
    let newFeat = feature;
    let featuresubtype = newFeat.featuresubtype;
    return (dispatch) => {
        return Api.getFeatureSubtype(featuresubtype).then((response) => {
            if (response.forms && response.forms[0]) {
                dispatch(naturalFeatureTypeLoaded(response.forms, response.featuretype, response.featuresubtype, "add"));
                newFeat = assign(createEmptyFormValues(response.forms), newFeat);
                dispatch(updateNaturalFeatureForm(newFeat));
            }
        }).catch((error) => {
            if (error.status === 401) {
                return dispatch(userNotAuthenticatedError(error));
            }
            return dispatch(naturalFeatureTypeError('Error from REST SERVICE: ' + error.message));
        });
    };
}

function naturalFeaturePolygonReplaced(geometry) {
    return {
        type: NATURAL_FEATURE_POLYGON_REPLACED,
        geometry
    };
}

function naturalFeatureMarkerReplaced(geometry) {
    return {
        type: NATURAL_FEATURE_MARKER_REPLACED,
        geometry
    };
}

function naturalFeatureGeomAdded(feature) {
    let newFeat = feature;
    if (feature.drawMethod === 'Marker') {
        return (dispatch) => {
            dispatch(naturalFeatureMarkerAdded(newFeat));
        };
    }
    if (feature.drawMethod === 'Polygon') {
        return (dispatch) => {
            dispatch(naturalFeaturePolygonReplaced(newFeat.geom));
        };
    }
    return (dispatch) => {
        dispatch(naturalFeatureMarkerReplaced(newFeat.geom));
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
        type: UPDATE_NATURAL_FEATURE_ERROR,
        status: "error",
        id,
        error
    };
}

function createNaturalFeatureLoading(id) {
    return {
        type: CREATE_NATURAL_FEATURE,
        status: "loading",
        id
    };
}

function createNaturalFeatureSuccess(id) {
    return {
        type: CREATE_NATURAL_FEATURE,
        status: "success",
        id
    };
}

function createNaturalFeatureError(feature, error) {
    return {
        type: CREATE_NATURAL_FEATURE_ERROR,
        status: "error",
        feature,
        error
    };
}

function naturalFeatureCreated(featuretype, featuresubtype, feature) {
    return (dispatch) => {
        dispatch(createNaturalFeatureLoading(feature));
        return Api.createNewFeature(feature).then((resp) => {
            if (resp) {
                dispatch(createNaturalFeatureSuccess(resp.id));
                dispatch(reloadFeatureType(resp.featuretype));
            }
        }).catch((error) => {
            if (error.status === 401) {
                return dispatch(userNotAuthenticatedError(error));
            }
            return dispatch(createNaturalFeatureError(-1, error));
        });
    };
}


function updateNaturalFeature(featuretype, featuresubtype, properties) {
    return (dispatch) => {
        dispatch(updateNaturalFeatureLoading(properties));
        return Api.updateNaturalFeature(featuretype, properties).then(() => {
            dispatch(updateNaturalFeatureSuccess(properties.id));
            dispatch(reloadFeatureType(featuretype));
        }).catch((error) => {
            if (error.status === 401) {
                return dispatch(userNotAuthenticatedError(error));
            }
            return dispatch(updateNaturalFeatureError(properties.id, error));
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
            dispatch(deleteNaturalFeatureSuccess(id));
            dispatch(reloadFeatureType(featuretype));
        }).catch((error) => {
            if (error.status === 401) {
                return dispatch(userNotAuthenticatedError(error));
            }
            return dispatch(deleteNaturalFeatureError(id, error));
        });
    };
}

function getData() {
    return (dispatch) => {
        dispatch(getAnimals('/nfdapi/layers/animal/'));
        dispatch(getPlants('nfdapi/layers/plant/'));
        dispatch(getNaturalAreas('/nfdapi/layers/naturalarea/'));
        dispatch(getFungus('/nfdapi/layers/fungus/'));
        dispatch(getSlimeMolds('/nfdapi/layers/slimemold/'));
    };
}

function loginSuccess(userDetails, username, password, authProvider) {
    sessionStorage.setItem('nfd-jwt-auth-token', userDetails.token);
    return {
        type: NFD_LOGIN_SUCCESS,
        userDetails: userDetails.user,
        username: userDetails.user.name,
        authProvider: authProvider
    };
}

function userLoginSubmit(username, password) {
    return (dispatch) => {
        Api.jwtLogin(username, password).then((response) => {
            dispatch(loginSuccess(response, username, password, "django-jwt"));
        }).catch((e) => {
            dispatch(loginFail(e));
        });
    };
}

function showLogin() {
    return (dispatch) => {
        dispatch(setControlProperty('LoginForm', 'enabled', true));
    };
}

function nfdLogout() {
    sessionStorage.setItem('nfd-jwt-auth-token', null);
    return (dispatch) => {
        dispatch(changeDrawingStatus('clean', null, 'dockednaturalfeatures', []));
        dispatch(logout(null));
        dispatch(changeLayerProperties("animal", {features: []}));
        dispatch(changeLayerProperties("fungus", {features: []}));
        dispatch(changeLayerProperties("plant", {features: []}));
        dispatch(changeLayerProperties("slimemold", {features: []}));
        dispatch(changeLayerProperties("naturalarea", {features: []}));
    };
}

function getVersion(featureType, featId, version) {
    return (dispatch) => {
        return Api.getVersion(featureType, featId, version).then((feature) => {
            if (feature) {
                // disptach(getVersionSuccess());
                dispatch(updateNaturalFeatureForm(feature));
                dispatch(changeDrawingStatus("selectionGeomLoaded", "MarkerReplace", "dockednaturalfeatures", [], {properties: feature}));
            }
        }).catch((error) => {
            if (error.status === 401) {
                return dispatch(userNotAuthenticatedError(error));
            }
            // return dispatch(getVersionError(featureType, featId, error));
        });
    };
}

function nextVersion(featureType, featId, currentVersion) {
    return getVersion(featureType, featId, currentVersion + 1);
}

function previousVersion(featureType, featId, currentVersion) {
    return getVersion(featureType, featId, currentVersion - 1);
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
    naturalFeatureCreated, naturalFeatureAdded,
    UPDATE_NATURAL_FEATURE, updateNaturalFeature,
    UPDATE_NATURAL_FEATURE_ERROR,
    CREATE_NATURAL_FEATURE_ERROR,
    CREATE_NATURAL_FEATURE,
    DELETE_NATURAL_FEATURE, deleteNaturalFeature,
    deleteNaturalFeatureLoading, deleteNaturalFeatureSuccess,
    deleteNaturalFeatureError,
    NATURAL_FEATURE_MARKER_ADDED, NATURAL_FEATURE_MARKER_REPLACED,
    NATURAL_FEATURE_POLYGON_REPLACED,
    getSpecies,
    updateSpeciesForms, UPDATE_SPECIES_FORMS,
    userLoginSubmit, NFD_LOGIN_SUCCESS, nfdLogout, getData,
    USER_NOT_AUTHENTICATED_ERROR,
    showLogin,
    nextVersion, previousVersion, naturalFeatureGeomAdded,
    addFeature, ADD_FEATURE,
    editFeature, EDIT_FEATURE,
    cancel, CANCEL_EDITING,
    endEditing, END_EDITING,
    onNfClick, NF_CLICKED,
    viewFeature, VIEW_FEATURE,
    editClicked, EDIT_FEATURE_CLICKED
};
