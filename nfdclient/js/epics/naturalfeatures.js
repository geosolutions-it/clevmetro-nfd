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
// const assign = require('object-assign');
const {setControlProperty} = require('../../MapStore2/web/client/actions//controls');
// const axios = require('../../MapStore2/web/client/libs/ajax');

const {
    GET_ANIMALS,
    GET_PLANTS,
    GET_NATURAL_AREAS,
    GET_MUSHROOMS,
    GET_SLIME_MOLDS,
    // NATURAL_FEATURE_SELECTED,
    NATURAL_FEATURE_LOADED,
    NATURAL_FEATURE_TYPE_LOADED,
    // CREATE_NATURAL_FEATURE,
    NATURAL_FEATURE_CREATED,
    naturalFeaturesLoaded,
    naturalFeaturesLoading,
    naturalFeaturesError,
    // naturalFeatureTypeError,
    // naturalFeatureTypeLoaded,
    naturalFeatureLoaded,
    updateNaturalFeatureForm,
    naturalFeatureCreated,
    naturalFeatureGeometryAdded
} = require('../actions/naturalfeatures');

const {END_DRAWING} = require('../../MapStore2/web/client/actions/draw');
/*
const types = {
    // string
    // 'xsd:ENTITIES': 'string',
    // 'xsd:ENTITY': 'string',
    // 'xsd:ID': 'string',
    // 'xsd:IDREF': 'string',
    // 'xsd:IDREFS': 'string',
    // 'xsd:language': 'string',
    // 'xsd:Name': 'string',
    // 'xsd:NCName': 'string',
    // 'xsd:NMTOKEN': 'string',
    // 'xsd:NMTOKENS': 'string',
    'xsd:normalizedString': 'string',
    // 'xsd:QName': 'string',
    'xsd:string': 'string',
    // 'xsd:token': 'string',

    // date
    'xsd:date': 'date',
    'xsd:dateTime': 'date',
    // 'xsd:duration': 'date',
    // 'xsd:gDay': 'date',
    // 'xsd:gMonth': 'date',
    // 'xsd:gMonthDay': 'date',
    // 'xsd:gYear': 'date',
    // 'xsd:gYearMonth': 'date',
    // 'xsd:time': 'date',

    // number
    // 'xsd:byte': 'number',
    'xsd:decimal': 'number',
    'xsd:int': 'number',
    'xsd:integer': 'number',
    'xsd:long': 'number',
    'xsd:negativeInteger': 'number',
    'xsd:nonNegativeInteger': 'number',
    'xsd:nonPositiveInteger': 'number',
    'xsd:positiveInteger': 'number',
    'xsd:short': 'number',
    'xsd:unsignedLong': 'number',
    'xsd:unsignedInt': 'number',
    'xsd:unsignedShort': 'number',
    // 'xsd:unsignedByte': 'number',

    // from old object
    'xsd:number': 'number',

    // misc
    // 'xsd:anyURI': 'string',
    // 'xsd:base64Binary': 'number',
    'xsd:boolean': 'boolean',
    'xsd:double': 'number',
    // 'xsd:hexBinary': 'string',
    // 'xsd:NOTATION': 'string',
    'xsd:float': 'number'
};*/

// const fieldConfig = {};
/*const extractInfo = (data) => {
    return [{
            name: 'Who is this?',
            icon: 'question-sign',
            geometry: data.featureTypes[0].properties
                .filter((attribute) => attribute.type.indexOf('gml:') === 0)
                .map((attribute) => {
                    let conf = {
                        label: attribute.name,
                        attribute: attribute.name,
                        type: 'geometry',
                        valueId: "id",
                        valueLabel: "name",
                        values: []
                    };
                    conf = fieldConfig[attribute.name] ? {...conf, ...fieldConfig[attribute.name]} : conf;
                    return conf;
                }),
            attributes: data.featureTypes[0].properties
                .filter((attribute) => attribute.type.indexOf('gml:') !== 0 && types[attribute.type])
                .map((attribute) => {
                    let conf = {
                        label: attribute.name,
                        attribute: attribute.name,
                        type: types[attribute.type],
                        valueId: "id",
                        valueLabel: "name",
                        values: []
                    };
                    conf = fieldConfig[attribute.name] ? {...conf, ...fieldConfig[attribute.name]} : conf;
                    return conf;
                })
        }, {
            name: 'Where is this?',
            icon: 'star',
            geometry: data.featureTypes[0].properties
                .filter((attribute) => attribute.type.indexOf('gml:') === 0)
                .map((attribute) => {
                    let conf = {
                        label: attribute.name,
                        attribute: attribute.name,
                        type: 'geometry',
                        valueId: "id",
                        valueLabel: "name",
                        values: []
                    };
                    conf = fieldConfig[attribute.name] ? {...conf, ...fieldConfig[attribute.name]} : conf;
                    return conf;
                }),
            attributes: data.featureTypes[0].properties
                .filter((attribute) => attribute.type.indexOf('gml:') !== 0 && types[attribute.type])
                .map((attribute) => {
                    let conf = {
                        label: attribute.name,
                        attribute: attribute.name,
                        type: types[attribute.type],
                        valueId: "id",
                        valueLabel: "name",
                        values: []
                    };
                    conf = fieldConfig[attribute.name] ? {...conf, ...fieldConfig[attribute.name]} : conf;
                    return conf;
                })
        }];
};*/

const createEmptyFeature = (featureType) => {
    const emptyFeature = {};
    featureType.map((section) => {
        section.attributes.map((attr) => {
            emptyFeature[attr.attribute] = null;
        });
    });
    return emptyFeature;
};

/*const getLayerId = (properties) => {
    let layerId = "";
    if (properties.occurrence_cat[0] === 'plant') {
        layerId = 'plants';
    } else if (properties.occurrence_cat[0] === 'animal') {
        layerId = 'animals';
    }
    return layerId;
};*/

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
            // changeLayerProperties('animals', {features: val.features.map((f, idx) => (assign({}, f, {id: idx, ftype: 'animals'}))) || []}),
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

const getMushroomsEpic = (action$, store) =>
    action$.ofType(GET_MUSHROOMS)
    .audit(() => {
        const isMapConfigured = (store.getState()).mapInitialConfig && true;
        return isMapConfigured && Rx.Observable.of(isMapConfigured) || action$.ofType('MAP_CONFIG_LOADED');
    })
    .switchMap(action =>
        Rx.Observable.defer(() => Api.getData(action.url))
        .retry(1)
        .map(val => [
            changeLayerProperties('mushrooms', {features: val.features}),
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
            changeLayerProperties('natural_areas', {features: val.features}),
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
            changeLayerProperties('slime_molds', {features: val.features}),
            naturalFeaturesLoaded(val.features, action.url)
        ])
        .mergeAll()
        .startWith(naturalFeaturesLoading())
        .catch(e => Rx.Observable.of(naturalFeaturesError(e)))
    );

/*const getNaturalFeatureTypeEpic = (action$) =>
    action$.ofType(NATURAL_FEATURE_SELECTED, CREATE_NATURAL_FEATURE)
    .switchMap(action =>
        // return Rx.Observable.defer( () => axios.get('http://geosolutions.scolab.eu/nfdapi/featuretypes/' + getLayerId(action.properties) + '/' + action.nfid))
        Rx.Observable.defer(() => Api.getData('http://geosolutions.scolab.eu/nfdapi/featuretypes/' + getLayerId(action.properties) + '/' + action.nfid))
            .map((response) => {
                let mode;
                if (action.type === NATURAL_FEATURE_SELECTED) {
                    mode = "viewedit";
                } else if (action.type === CREATE_NATURAL_FEATURE) {
                    mode = "add";
                }
                if (typeof response.data === 'object' && response.data.forms && response.data.forms[0]) {
                    const featureType = response.data;
                    return Rx.Observable.from([naturalFeatureTypeLoaded(featureType, action.properties, mode)]);
                }
                try {
                    JSON.parse(response.data);
                } catch(e) {
                    return Rx.Observable.from([naturalFeatureTypeError('Error from REST SERVICE: ' + e.message)]);
                }
                return Rx.Observable.from([naturalFeatureTypeError('Error: naturalfeature types are empty')]);
            })
            .mergeAll()
            .catch(e => Rx.Observable.of(naturalFeatureTypeError(e.message)))
    );*/

const naturalFeatureSelectedEpic = action$ =>
    action$.ofType(NATURAL_FEATURE_TYPE_LOADED)
        .switchMap((action) => {
            /*return Rx.Observable.defer( () => axios.get(action.url + '?service=WFS&version=1.1.0&request=DescribeFeatureType&typeName=' + action.typeName + '&outputFormat=application/json'))
                .map((response) => {
                    if (typeof response.data === 'object' && response.data.featureTypes && response.data.featureTypes[0]) {
                        return Rx.Observable.from([naturalFeatureLoaded(response.data)]);
                    }
                    try {
                        JSON.parse(response.data);
                    } catch(e) {
                        return Rx.Observable.from([naturalFeatureError('Error from WFS: ' + e.message)]);
                    }
                    return Rx.Observable.from([naturalFeatureError('Error: feature types are empty')]);
                })
                .mergeAll()
                .catch(e => Rx.Observable.of(naturalFeatureError(e.message)));*/
            if (action.mode === 'viewedit') {
                return Rx.Observable.from([naturalFeatureLoaded(action.properties)]);
            } else if (action.mode === 'add') {
                return Rx.Observable.from([naturalFeatureCreated(action.featureType)]);
            }
        });

/**
 * @memberof epics.naturalfeatures
 * @param {external:Observable} action$ manages `NATURAL_FEATURE_LOADED`
 * @return {external:Observable}
 */
const naturalFeatureLoadedEpic = (action$) =>
    action$.ofType(NATURAL_FEATURE_LOADED)
        .switchMap((action) => {
            return Rx.Observable.merge(
                Rx.Observable.of(setControlProperty('addnaturalfeatures', 'enabled', false)),
                Rx.Observable.of(updateNaturalFeatureForm(action.feature)),
                Rx.Observable.of(setControlProperty('vieweditnaturalfeatures', 'enabled', true))
            );
        });

/**
 * @memberof epics.naturalfeatures
 * @param {external:Observable} action$ manages `NATURAL_FEATURE_CREATED`
 * @return {external:Observable}
 */
const naturalFeatureCreatedEpic = (action$) =>
    action$.ofType(NATURAL_FEATURE_CREATED)
        .switchMap((action) => {
            let emptyFeat = createEmptyFeature(action.featureType);
            return Rx.Observable.merge(
                Rx.Observable.of(updateNaturalFeatureForm(emptyFeat)),
                Rx.Observable.of(setControlProperty('addnaturalfeatures', 'enabled', true))
            );
        });

/**
 * @memberof epics.naturalfeatures
 * @param {external:Observable} action$ manages `NATURAL_FEATURE_CREATED`
 * @return {external:Observable}
 */
const addNaturalFeatureGeometryEpic = (action$) =>
    action$.ofType(END_DRAWING)
        .switchMap((action) => {
            return Rx.Observable.from([naturalFeatureGeometryAdded(action.geometry)]);
        });

module.exports = {
    getAnimalsEpic,
    getPlantsEpic,
    getMushroomsEpic,
    getNaturalAreasEpic,
    getSlimeMoldsEpic,
    naturalFeatureSelectedEpic,
    naturalFeatureLoadedEpic,
    // getNaturalFeatureTypeEpic,
    naturalFeatureCreatedEpic,
    addNaturalFeatureGeometryEpic
};
