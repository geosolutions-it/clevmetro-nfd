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
const {toggleControl} = require('../../MapStore2/web/client/actions/controls');
const {
    GET_ANIMALS,
    GET_PLANTS,
    GET_NATURAL_AREAS,
    GET_FUNGUS,
    GET_SLIME_MOLDS,
    NFD_LOGIN_SUCCESS,
    ADD_FEATURE,
    getData,
    naturalFeaturesLoaded,
    naturalFeaturesLoading,
    naturalFeaturesError,
    naturalFeatureGeomAdded,
    USER_NOT_AUTHENTICATED_ERROR,
    showLogin,
    END_EDITING,
    NF_CLICKED,
    naturalFeatureSelected,
    viewFeature,
    editFeature
} = require('../actions/naturalfeatures');
const {isWriter, isPublisher} = require('../plugins/naturalfeatures/securityutils.js');
const {END_DRAWING, changeDrawingStatus} = require('../../MapStore2/web/client/actions/draw');
const Utils = require('../utils/nfdUtils');

const getAnimalsEpic = (action$, store) =>
    action$.ofType(GET_ANIMALS)
    .audit(() => {
        const isMapConfigured = (store.getState()).mapInitialConfig && true;
        return isMapConfigured && Rx.Observable.of(isMapConfigured) || action$.ofType('MAP_CONFIG_LOADED');
    })
    .switchMap(action =>
        Rx.Observable.defer(() => Api.getData(action.url))
        .retry(1)
        .map(val => [
            changeLayerProperties('animal', {features: val.features}),
            naturalFeaturesLoaded(val.features, action.url)
        ])
        .mergeAll()
        .startWith(naturalFeaturesLoading())
        .catch(e => Rx.Observable.of(naturalFeaturesError(e)))
    );

const getPlantsEpic = (action$, store) =>
    action$.ofType(GET_PLANTS)
    .audit(() => {
        const isMapConfigured = (store.getState()).mapInitialConfig && true;
        return isMapConfigured && Rx.Observable.of(isMapConfigured) || action$.ofType('MAP_CONFIG_LOADED');
    })
    .switchMap(action =>
        Rx.Observable.defer(() => Api.getData(action.url))
        .retry(1)
        .map(val => [
            changeLayerProperties('plant', {features: val.features}),
            naturalFeaturesLoaded(val.features, action.url)
        ])
        .mergeAll()
        .startWith(naturalFeaturesLoading())
        .catch(e => Rx.Observable.of(naturalFeaturesError(e)))
    );

const getFungusEpic = (action$, store) =>
    action$.ofType(GET_FUNGUS)
    .audit(() => {
        const isMapConfigured = (store.getState()).mapInitialConfig && true;
        return isMapConfigured && Rx.Observable.of(isMapConfigured) || action$.ofType('MAP_CONFIG_LOADED');
    })
    .switchMap(action =>
        Rx.Observable.defer(() => Api.getData(action.url))
        .retry(1)
        .map(val => [
            changeLayerProperties('fungus', {features: val.features}),
            naturalFeaturesLoaded(val.features, action.url)
        ])
        .mergeAll()
        .startWith(naturalFeaturesLoading())
        .catch(e => Rx.Observable.of(naturalFeaturesError(e)))
    );

const getNaturalAreasEpic = (action$, store) =>
    action$.ofType(GET_NATURAL_AREAS)
    .audit(() => {
        const isMapConfigured = (store.getState()).mapInitialConfig && true;
        return isMapConfigured && Rx.Observable.of(isMapConfigured) || action$.ofType('MAP_CONFIG_LOADED');
    })
    .switchMap(action =>
        Rx.Observable.defer(() => Api.getData(action.url))
        .retry(1)
        .map(val => [
            changeLayerProperties('naturalarea', {features: val.features}),
            naturalFeaturesLoaded(val.features, action.url)
        ])
        .mergeAll()
        .startWith(naturalFeaturesLoading())
        .catch(e => Rx.Observable.of(naturalFeaturesError(e)))
    );

const getSlimeMoldsEpic = (action$, store) =>
    action$.ofType(GET_SLIME_MOLDS)
    .audit(() => {
        const isMapConfigured = (store.getState()).mapInitialConfig && true;
        return isMapConfigured && Rx.Observable.of(isMapConfigured) || action$.ofType('MAP_CONFIG_LOADED');
    })
    .switchMap(action =>
        Rx.Observable.defer(() => Api.getData(action.url))
        .retry(1)
        .map(val => [
            changeLayerProperties('slimemold', {features: val.features}),
            naturalFeaturesLoaded(val.features, action.url)
        ])
        .mergeAll()
        .startWith(naturalFeaturesLoading())
        .catch(e => Rx.Observable.of(naturalFeaturesError(e)))
    );

// Load features for all reatureTypes
const getDataEpic = action$ =>
    action$.ofType(NFD_LOGIN_SUCCESS).
    switchMap(() => Rx.Observable.of(getData()));

const unauthorizedUserErrorEpic = action$ =>
    action$.ofType(USER_NOT_AUTHENTICATED_ERROR)
    .map(() =>
        showLogin());

/**
 * @memberof epics.naturalfeatures
 * @param {external:Observable} action$ manages `NATURAL_FEATURE_CREATED`
 * @return {external:Observable}
 */
const addNaturalFeatureGeometryEpic = (action$) =>
    action$.ofType(END_DRAWING)
        .switchMap((action) => {
            return Rx.Observable.from([naturalFeatureGeomAdded(action.geometry)]);
        });
const activateFeatureInsert = (action$) =>
    action$.ofType(ADD_FEATURE)
    .switchMap(({properties}) => {
        return Rx.Observable.of(changeDrawingStatus("start", "Marker", "dockednaturalfeatures", [], {properties, icon: Utils.getIconUrl(properties.featuretype)}));
    });
const cleanDraw = (action$, store) =>
        action$.ofType(END_EDITING)
        .switchMap(() => {
            const {controls} = store.getState();
            const control = controls.addnaturalfeatures && controls.addnaturalfeatures.enabled ? 'addnaturalfeatures' : 'vieweditnaturalfeatures';
            return Rx.Observable.from([changeDrawingStatus("clean", null, "dockednaturalfeatures", [], {}), toggleControl(control)]);
        });
const activeFeatureEdit = (action$, store) =>
     action$.ofType(NF_CLICKED, 'SELECT_FEATURE')
        .filter(() => {
            const {naturalfeatures} = store.getState();
            return naturalfeatures.mode !== 'ADD' && naturalfeatures.mode !== 'EDIT';
        })
        .switchMap((a) => {
            // TODO: Recover the json geom form the layer and add to props
            // const {flat: layers} = (store.getState()).layers;
            // const layer = layers.filter(l => l.id === a.properties.featuretype).pop();
            // const feature = (layer && layer.features || []).filter(f => f.id === a.properties.id).pop();
            // const geom = feature && feature.geometry;
            // const props = {...a.properties, geom};
            const modeAction = isPublisher(store.getState(), a.properties.featuretype) || isWriter(store.getState(), a.properties.featuretype) ? editFeature() : viewFeature();
            return Rx.Observable.from([naturalFeatureSelected(a.properties, a.nfId, a.layer), modeAction]);
        });
    // const removeAddEditedFeature = (action$, store) =>
    //     action$.ofType()
module.exports = {
    getDataEpic,
    unauthorizedUserErrorEpic,
    getAnimalsEpic,
    getPlantsEpic,
    getFungusEpic,
    getNaturalAreasEpic,
    getSlimeMoldsEpic,
    addNaturalFeatureGeometryEpic,
    activateFeatureInsert,
    cleanDraw,
    activeFeatureEdit
};
