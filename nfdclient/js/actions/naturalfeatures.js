/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/
const assign = require('object-assign');

const Api = require('../api/naturalfeaturesdata');
const {setControlProperty} = require('../../MapStore2/web/client/actions/controls');
const {changeDrawingStatus} = require('../../MapStore2/web/client/actions/draw');
const {changeLayerProperties} = require('../../MapStore2/web/client/actions/layers');
const {loginFail, logout} = require('../../MapStore2/web/client/actions/security');

const LOAD_NATURAL_FEATURES = 'LOAD_NATURAL_FEATURES';
const NATURAL_FEATURES_ERROR = 'NATURAL_FEATURES_ERROR';
const NATURAL_FEATURES_LOADING = 'NATURAL_FEATURES_LOADING';
const NATURAL_FEATURES_LOADED = 'NATURAL_FEATURES_LOADED';

const NATURAL_FEATURE_SELECTED = 'NATURAL_FEATURE_TYPE_SELECTED';
const NATURAL_FEATURE_ERROR = 'NATURAL_FEATURE_ERROR';
const NATURAL_FEATURE_LOADED = 'NATURAL_FEATURE_LOADED';

const UPDATE_NATURAL_FEATURE_FORM = 'UPDATE_NATURAL_FEATURE_FORM';
const UPDATE_SPECIES_FORMS = 'UPDATE_SPECIES_FORMS';

const NATURAL_FEATURE_TYPE_LOADED = 'NATURAL_FEATURE_TYPE_LOADED';
const NATURAL_FEATURE_ADDED = 'NATURAL_FEATURE_ADDED';
const NATURAL_FEATURE_TYPE_ERROR = 'NATURAL_FEATURE_TYPE_ERROR';

const UPDATE_NATURAL_FEATURE = 'UPDATE_NATURAL_FEATURE';
const UPDATE_NATURAL_FEATURE_ERROR = 'UPDATE_NATURAL_FEATURE_ERROR';
const CREATE_NATURAL_FEATURE = 'CREATE_NATURAL_FEATURE';
const CREATE_NATURAL_FEATURE_ERROR = 'CREATE_NATURAL_FEATURE_ERROR';
const NATURAL_FEATURE_CREATED = 'NATURAL_FEATURE_CREATED';
const DELETE_NATURAL_FEATURE = 'DELETE_NATURAL_FEATURE';

const NATURAL_FEATURE_MARKER_ADDED = 'NATURAL_FEATURE_MARKER_ADDED';
const NATURAL_FEATURE_POLYGON_REPLACED = 'NATURAL_FEATURE_POLYGON_REPLACED';
const NATURAL_FEATURE_MARKER_REPLACED = 'NATURAL_FEATURE_MARKER_REPLACED';

const NFD_LOGIN_SUCCESS = 'NFD_LOGIN_SUCCESS';
const USER_NOT_AUTHENTICATED_ERROR = 'USER_NOT_AUTHENTICATED_ERROR';

const ADD_FEATURE = 'ADD_FEATURE';
const EDIT_FEATURE = 'EDIT_FEATURE';
const VIEW_FEATURE = 'VIEW_FEATURE';
const END_EDITING = 'END_EDITING';
const CANCEL_EDITING = 'CANCEL_EDITING';
const NF_CLICKED = 'NF_CLICKED';
const EDIT_FEATURE_CLICKED = 'EDIT_FEATURE_CLICKED';
const ADD_IMAGE = 'ADD_IMAGE';
const IMAGE_ERROR = 'IMAGE_ERROR';
const REMOVE_IMAGE = 'REMOVE_IMAGE';
const IMAGE_UPLOADED = 'IMAGE_UPLOADED';
const FEATURE_PROPERTY_CHANGE = 'FEATURE_PROPERTY_CHANGE';

function onFeaturePropertyChange(property, value) {
    return {
        type: FEATURE_PROPERTY_CHANGE,
        property,
        value
    };
}


function imageUploaded(images) {
    return {
        type: IMAGE_UPLOADED,
        images
    };
}

function removeImage(idx) {
    return {
        type: REMOVE_IMAGE,
        idx
    };
}
function imageError(errors) {
    return {
        type: IMAGE_ERROR,
        errors
    };
}
function addImage(image) {
    return {
        type: ADD_IMAGE,
        image
    };
}

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
function editFeature(feature) {
    return {
        type: EDIT_FEATURE,
        feature
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

function naturalFeaturesError(featureType, error) {
    return {
        type: NATURAL_FEATURES_ERROR,
        error,
        featureType
    };
}

function naturalFeaturesLoading(loading = true) {
    return {
        type: NATURAL_FEATURES_LOADING,
        loading
    };
}

function naturalFeaturesLoaded(featureType, features) {
    return {
        type: NATURAL_FEATURES_LOADED,
        featureType,
        features
    };
}
function getNaturalFeatures(featureType) {
    return {
        type: LOAD_NATURAL_FEATURES,
        featureType
    };
}

// FORM CONFIG LOADED
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

function getFeatureInfo(properties, nfid) {
    return (dispatch) => {
        return Api.getFeatureInfo(properties.featuretype, nfid).then((resp) => {
            if (resp) {
                let feature = normalizeInfo(resp);
                dispatch(updateNaturalFeatureForm(feature));
                dispatch(changeDrawingStatus("selectionGeomLoaded", "Marker", "dockednaturalfeatures", [], {properties: resp}));
                dispatch(naturalFeaturesLoading(false));
            }
        }).catch((error) => {
            if (error.status === 401) {
                dispatch(userNotAuthenticatedError(error));
            }else {
                dispatch(naturalFeatureTypeError('Error from REST SERVICE: ' + error.message));
            }
            dispatch(naturalFeaturesLoading(false));
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

function naturalFeatureSelected(properties, nfid) {
    return (dispatch) => {
        dispatch(naturalFeaturesLoading());
        return Api.getFeatureSubtype(properties.featuresubtype).then((resp) => {
            if (resp.forms && resp.forms[0]) {
                dispatch(naturalFeatureTypeLoaded(resp.forms, resp.featuretype, resp.featuresubtype, "viewedit"));
                dispatch(getFeatureInfo(properties, nfid));
            }
        }).catch((error) => {
            if (error.status === 401) {
                dispatch(userNotAuthenticatedError(error));
            }else {
                dispatch(naturalFeatureTypeError('Error from REST SERVICE: ' + error.message));
            }
            dispatch(naturalFeaturesLoading(false));
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
        dispatch({type: "CLEAN_FORM"});
        dispatch(naturalFeaturesLoading(true));
        return Api.getFeatureSubtype(featuresubtype).then((response) => {
            dispatch(naturalFeaturesLoading(false));
            if (response.forms && response.forms[0]) {
                dispatch(naturalFeatureTypeLoaded(response.forms, response.featuretype, response.featuresubtype, "add"));
                newFeat = assign(createEmptyFormValues(response.forms), newFeat);
                dispatch(updateNaturalFeatureForm(newFeat));
            }
        }).catch((error) => {
            if (error.status === 401) {
                dispatch(userNotAuthenticatedError(error));
            }else {
                dispatch(naturalFeatureTypeError('Error from REST SERVICE: ' + error.message));
            }
            dispatch(naturalFeaturesLoading(false));
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

function createNaturalFeatureSuccess(featureType, id) {
    return {
        type: NATURAL_FEATURE_CREATED,
        status: "success",
        id,
        featureType
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
function addNaturalFeature(featuretype, featuresubtype, feature) {
    return {
        type: CREATE_NATURAL_FEATURE,
        featuretype,
        featuresubtype, feature
    };
}

function updateNaturalFeature(featuretype, featuresubtype, properties) {
    return (dispatch) => {
        dispatch(naturalFeaturesLoading());
        return Api.updateNaturalFeature(featuretype, properties).then(() => {
            dispatch(updateNaturalFeatureSuccess(properties.id));
            dispatch(getNaturalFeatures(featuretype));
            dispatch(naturalFeaturesLoading(false));
        }).catch((error) => {
            if (error.status === 401) {
                dispatch(userNotAuthenticatedError(error));
            } else {
                dispatch(updateNaturalFeatureError(properties.id, error));
            }
            dispatch(naturalFeaturesLoading(false));
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
            dispatch(getNaturalFeatures(featuretype));
        }).catch((error) => {
            if (error.status === 401) {
                return dispatch(userNotAuthenticatedError(error));
            }
            return dispatch(deleteNaturalFeatureError(id, error));
        });
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
        dispatch(naturalFeaturesLoading());
        return Api.getVersion(featureType, featId, version).then((feature) => {
            dispatch(naturalFeaturesLoading(false));
            if (feature) {
                dispatch(updateNaturalFeatureForm(feature));
                dispatch(changeDrawingStatus("selectionGeomLoaded", "MarkerReplace", "dockednaturalfeatures", [], {properties: feature}));
            }
        }).catch((error) => {
            if (error.status === 401) {
                dispatch(userNotAuthenticatedError(error));
            }
            dispatch(naturalFeaturesLoading(false));
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
    NATURAL_FEATURE_SELECTED, naturalFeatureSelected,
    NATURAL_FEATURE_LOADED, naturalFeatureLoaded,
    NATURAL_FEATURE_ERROR, naturalFeatureError,
    UPDATE_NATURAL_FEATURE_FORM, updateNaturalFeatureForm,
    LOAD_NATURAL_FEATURES, getNaturalFeatures,
    NATURAL_FEATURE_TYPE_LOADED, naturalFeatureTypeLoaded,
    NATURAL_FEATURE_TYPE_ERROR, naturalFeatureTypeError, naturalFeatureAdded,
    UPDATE_NATURAL_FEATURE, updateNaturalFeature,
    UPDATE_NATURAL_FEATURE_ERROR,
    CREATE_NATURAL_FEATURE_ERROR,
    NATURAL_FEATURE_CREATED, createNaturalFeatureSuccess,
    CREATE_NATURAL_FEATURE, addNaturalFeature,
    DELETE_NATURAL_FEATURE, deleteNaturalFeature,
    deleteNaturalFeatureLoading, deleteNaturalFeatureSuccess,
    deleteNaturalFeatureError,
    NATURAL_FEATURE_MARKER_ADDED, NATURAL_FEATURE_MARKER_REPLACED,
    NATURAL_FEATURE_POLYGON_REPLACED,
    getSpecies,
    updateSpeciesForms, UPDATE_SPECIES_FORMS,
    userLoginSubmit, NFD_LOGIN_SUCCESS, nfdLogout,
    USER_NOT_AUTHENTICATED_ERROR,
    showLogin,
    nextVersion, previousVersion, naturalFeatureGeomAdded,
    addFeature, ADD_FEATURE,
    editFeature, EDIT_FEATURE,
    cancel, CANCEL_EDITING,
    endEditing, END_EDITING,
    onNfClick, NF_CLICKED,
    viewFeature, VIEW_FEATURE,
    editClicked, EDIT_FEATURE_CLICKED,
    ADD_IMAGE, addImage,
    IMAGE_ERROR, imageError,
    REMOVE_IMAGE, removeImage,
    userNotAuthenticatedError,
    createNaturalFeatureError,
    imageUploaded, IMAGE_UPLOADED,
    FEATURE_PROPERTY_CHANGE, onFeaturePropertyChange
};
