/**
 * Copyright 2016, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const axios = require('../../MapStore2/web/client/libs/ajax');
const ConfigUtils = require('../../MapStore2/web/client/utils/ConfigUtils');
const assign = require('object-assign');
const dataCache = {};

const Api = {
    addBaseUrl: function(options) {
        return assign(options, {baseURL: ConfigUtils.getDefaults().geoStoreUrl});
    },
    getData: function(url) {
        /*const cached = dataCache[url];
        if (cached && new Date().getTime() < cached.timestamp + (ConfigUtils.getConfigProp('cacheDataExpire') || 60) * 1000) {
            return new Promise((resolve) => {
                resolve(cached.data);
            });
        }*/
        return axios.get(url).then((response) => {
            dataCache[url] = {
                timestamp: new Date().getTime(),
                data: response.data
            };
            return response.data;
        });
    },
    updateNaturalFeature: function(featuretype, feature) {
        let url = 'https://dev.nfd.geo-solutions.it/nfdapi/layers/' + featuretype + '/' + feature.id + '/';
        return axios.put(url, feature).then(function(response) {return response.data; });
    },
    deleteNaturalFeature: function(layerId, nfid) {
        let url = 'https://dev.nfd.geo-solutions.it/nfdapi/layers/' + layerId + '/' + nfid + '/';
        return axios.delete(url).then(function(response) {return response.data; });
    },
    getFeatureType: function(layerId, nfid) {
        let url = 'https://dev.nfd.geo-solutions.it/nfdapi/featuretypes/' + layerId + '/' + nfid + '/';
        return axios.get(url).then(function(response) {return response.data; });
    },
    getFeatureInfo: function(layerId, nfid) {
        let url = 'https://dev.nfd.geo-solutions.it/nfdapi/layers/' + layerId + '/' + nfid + '/';
        return axios.get(url).then(function(response) {return response.data; });
    },
    getSpecie: function(id) {
        let url = 'https://dev.nfd.geo-solutions.it/nfdapi/species/' + id + '/';
        return axios.get(url).then(function(response) {return response.data; });
    },
    createNewFeature: function(feature) {
        let url = 'https://dev.nfd.geo-solutions.it/nfdapi/layers/' + feature.featuretype + '/';
        return axios.post(url, feature).then(function(response) {return response.data; });
    }
};

module.exports = Api;
