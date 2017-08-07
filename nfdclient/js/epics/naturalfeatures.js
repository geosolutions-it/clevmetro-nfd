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

const {
    GET_ANIMALS,
    GET_PLANTS,
    GET_NATURAL_AREAS,
    GET_FUNGUS,
    GET_SLIME_MOLDS,
    NFD_LOGIN_SUCCESS,
    getData,
    naturalFeaturesLoaded,
    naturalFeaturesLoading,
    naturalFeaturesError,
    NATURAL_FEATURES_ERROR,
    naturalFeatureMarkerAdded
} = require('../actions/naturalfeatures');

const {
    showLogin
} = require('../plugins/login/index');

const {END_DRAWING} = require('../../MapStore2/web/client/actions/draw');

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

const getDataEpic = action$ =>
    action$.ofType(NFD_LOGIN_SUCCESS)
    .map(val => getData(val));

const getDataErrorEpic = action$ =>
    action$.ofType(NATURAL_FEATURES_ERROR)
    .map(val => showLogin(val));


/**
 * @memberof epics.naturalfeatures
 * @param {external:Observable} action$ manages `NATURAL_FEATURE_CREATED`
 * @return {external:Observable}
 */
const addNaturalFeatureGeometryEpic = (action$) =>
    action$.ofType(END_DRAWING)
        .switchMap((action) => {
            return Rx.Observable.from([naturalFeatureMarkerAdded(action.geometry)]);
        });

module.exports = {
    getDataEpic,
    getDataErrorEpic,
    getAnimalsEpic,
    getPlantsEpic,
    getFungusEpic,
    getNaturalAreasEpic,
    getSlimeMoldsEpic,
    addNaturalFeatureGeometryEpic
};
