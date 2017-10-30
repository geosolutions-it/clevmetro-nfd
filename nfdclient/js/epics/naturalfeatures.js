/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const Rx = require('rxjs');
const Api = require('../api/naturalfeaturesdata');
const {changeLayerProperties} = require('../../MapStore2/web/client/actions/layers');
const {toggleControl, setControlProperty} = require('../../MapStore2/web/client/actions/controls');
const {error} = require('../../MapStore2/web/client/actions/notifications');
const {
    CREATE_NATURAL_FEATURE, NFD_LOGIN_SUCCESS, ADD_FEATURE,
    NATURAL_FEATURES_LOADED, LOAD_NATURAL_FEATURES, naturalFeaturesLoaded, naturalFeaturesLoading, naturalFeaturesError, naturalFeatureGeomAdded,
    USER_NOT_AUTHENTICATED_ERROR, showLogin, END_EDITING, NF_CLICKED, EDIT_FEATURE, endEditing, naturalFeatureSelected, viewFeature, CANCEL_EDITING, EDIT_FEATURE_CLICKED, createNaturalFeatureSuccess, NATURAL_FEATURE_CREATED, userNotAuthenticatedError, createNaturalFeatureError, imageUploaded, removeImage,
    IMAGE_ERROR,
    CREATE_NATURAL_FEATURE_ERROR, UPDATE_NATURAL_FEATURE_ERROR
} = require('../actions/naturalfeatures');
const {SELECT_FEATURE} = require('../actions/featuresearch');

const {END_DRAWING, changeDrawingStatus} = require('../../MapStore2/web/client/actions/draw');
const Utils = require('../utils/nfdUtils');

const {warning} = require('../../MapStore2/web/client/actions/notifications');

const fetchFeatures = (featureType) => {
    return Rx.Observable.defer(() => Api.getData(`/nfdapi/layers/${featureType}/`))
                .retry(1)
                .map(val => naturalFeaturesLoaded(featureType, val.features))
                .catch(e => Rx.Observable.of(naturalFeaturesError(featureType, e)));
};

module.exports = {

updateFeatureTypeLayer: (action$) =>
    action$.ofType(NATURAL_FEATURES_LOADED)
    .switchMap((a) => Rx.Observable.of(changeLayerProperties(a.featureType, {features: a.features}))),

// Get fature for a featuretype
fetchNaturalFeatures: (action$) =>
    action$.ofType(LOAD_NATURAL_FEATURES, NATURAL_FEATURE_CREATED)
    .switchMap( a => fetchFeatures(a.featureType)
                    .startWith(naturalFeaturesLoading(true))
                    .concat([naturalFeaturesLoading(false)])),

// Load features for all featureTypes
getDataEpic: (action$, store) =>
    action$.ofType(NFD_LOGIN_SUCCESS).
    switchMap(() => {
        const {featureTypes = []} = (store.getState()).featuresearch;
        return Rx.Observable.from(featureTypes.map((ft) => fetchFeatures(ft))).mergeAll().
        startWith(naturalFeaturesLoading(true)).concat([naturalFeaturesLoading(false)]);
    }),

unauthorizedUserErrorEpic: action$ =>
    action$.ofType(USER_NOT_AUTHENTICATED_ERROR)
    .map(() =>
        showLogin()),

/**
 * @memberof epics.naturalfeatures
 * @param {external:Observable} action$ manages `NATURAL_FEATURE_CREATED`
 * @return {external:Observable}
 */
addNaturalFeatureGeometryEpic: (action$) =>
    action$.ofType(END_DRAWING)
        .switchMap((action) => {
            return Rx.Observable.from([naturalFeatureGeomAdded(action.geometry)].concat(action.geometry.drawMethod === 'Marker' ? [toggleControl('addnaturalfeatures', 'enabled', true)] : []));
        }),
// Activate drawing when user enter in add feature on error end editing
activateFeatureInsert: (action$) =>
    action$.ofType(ADD_FEATURE)
    .switchMap(({properties}) => {
        return action$.ofType('NATURAL_FEATURE_TYPE_ERROR').mapTo(endEditing()).takeUntil(action$.ofType('NATURAL_FEATURE_TYPE_LOADED')).startWith(changeDrawingStatus("start", "Marker", "dockednaturalfeatures", [], {properties, icon: Utils.getIcon(properties.featuretype)}));
    }),
// Reset the state on end editing
cleanDraw: (action$, store) =>
        action$.ofType(END_EDITING)
        .switchMap(() => {
            const {controls} = store.getState();
            const control = controls.addnaturalfeatures && controls.addnaturalfeatures.enabled ? 'addnaturalfeatures' : 'vieweditnaturalfeatures';
            return Rx.Observable.from([changeDrawingStatus("clean", null, "dockednaturalfeatures", [], {}), toggleControl(control)]);
        }),
// Start edit when e feature is clicked or selected from the list.
activeFeatureEdit: (action$, store) =>
    action$.ofType(NF_CLICKED, SELECT_FEATURE)
        .switchMap((a) => {
            const {naturalfeatures} = store.getState();
            const isEditing = naturalfeatures.mode === 'ADD' || naturalfeatures.mode === 'EDIT';
            if (isEditing) {
                return Rx.Observable.of(warning({title: "Warning", message: "End edit to select a different natural feature", autoDismiss: 2}));
            }
            return Rx.Observable.from([{type: "CLEAN_FORM"}, naturalFeatureSelected(a.properties, a.nfId), viewFeature(), setControlProperty('features', 'enabled', false), setControlProperty('vieweditnaturalfeatures', 'enabled', true)]);
        }),
// Open the form edit panel if It's close and a user clikcs on the feature that is currently editing
showEditPanel: (action$, store) =>
    action$.ofType(EDIT_FEATURE_CLICKED)
        .filter((a) => {
            const {vieweditnaturalfeatures: v, addnaturalfeatures: ad} = (store.getState()).controls;
            return (a.ftId && !(v && v.enabled)) || (!a.ftId && !(ad && ad.enabled));
        })
        .switchMap((a) => {
            const control = a.ftId ? 'vieweditnaturalfeatures' : 'addnaturalfeatures';
            return Rx.Observable.of(setControlProperty(control, 'enabled', true));
        }),
// Remove the edited feature from Its layer and when editing end if needed reads it
removeAddEditedFeature: (action$, store) =>
    action$.ofType(EDIT_FEATURE)
        .switchMap((a) => {
            const {flat: layers} = (store.getState()).layers;
            const layer = layers.filter(l => l.id === a.feature.featuretype).pop();
            const features = layer.features || [];
            const newFeatures = features.filter(f => f.id !== a.feature.id);
            return action$.ofType(CANCEL_EDITING).
                    switchMap(() => Rx.Observable.of(changeLayerProperties(layer.id, {features}))
                        .takeUntil(action$.ofType(END_EDITING)))
                    .startWith(changeLayerProperties(layer.id, {features: newFeatures}));
        }),
onCancel: action$ =>
        action$.ofType(CANCEL_EDITING)
        .mapTo(endEditing()),

addNaturalFeature: (action$) =>
    action$.ofType(CREATE_NATURAL_FEATURE)
    .switchMap( a => {
        return Rx.Observable.fromPromise(Api.createNewFeature(a.feature))
                .map((v) => createNaturalFeatureSuccess(a.featuretype, v.id))
                .startWith(naturalFeaturesLoading(true))
                .catch((e) => {
                    const action = e.status === 401 ? userNotAuthenticatedError(e) : createNaturalFeatureError(-1, e);
                    return Rx.Observable.of(action);
                })
                .concat([naturalFeaturesLoading(false)]);
    }),
showSaveUpdateDeleteErrors: action$ =>
    action$.ofType(CREATE_NATURAL_FEATURE_ERROR, UPDATE_NATURAL_FEATURE_ERROR)
    .switchMap( a => {
        if (a.error.status >= 500) {
            return Rx.Observable.of(error({title: 'Bad request', message: `Error: ${a.error.statusText}`}));
        }
        return Rx.Observable.from(Object.keys(a.error.data).map((k) => {
            return error({uid: k, title: 'Bad request', message: `${k}: ${a.error.data[k]}`});
        }));
    }),
uploadImage: (action$) =>
    action$.ofType('ADD_IMAGE').filter(a => a.image).
    switchMap( a => {
        return Rx.Observable.fromPromise(Api.uploadImage(a.image)).map(({images = []}) => (imageUploaded(images)))
        .startWith(naturalFeaturesLoading(true))
        .catch(e => Rx.Observable.from([error({title: 'Uploading', message: `Error: ${e.statusText}`}), removeImage(0)]))
        .concat([naturalFeaturesLoading(false)]);
    }),
// Sowhs error message if user tries to add wrong image
onImageEr: (action$) =>
    action$.ofType(IMAGE_ERROR)
    .map((a) => error({title: 'Wrong Image', message: `Wrong ${a.errors.join(" and ")}`}))
};
