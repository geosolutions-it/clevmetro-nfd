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
const toBlob = require('canvas-to-blob');

const dataCache = {};
const getAccept = (format) => {
    switch (format) {
        case 'csv':
            return {'Accept': 'text/csv'};
        case 'xlsx':
            return {'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'};
        case 'shp':
            return {'Accept': 'application/zip'};
        default :
            return {'Accept': 'application/zip'};
    }
};
let getOptions = () => {
    const token = sessionStorage.getItem('nfd-jwt-auth-token');
    if (token !== null) {
        return {headers: {'Authorization': "JWT " + token}};
    }
    return {};
};

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
        return axios.get(url, getOptions()).then((response) => {
            dataCache[url] = {
                timestamp: new Date().getTime(),
                data: response.data
            };
            return response.data;
        });
    },
    updateNaturalFeature: function(featuretype, feature) {
        let url = '/nfdapi/layers/' + featuretype + '/' + feature.id + '/';
        return axios.put(url, feature, getOptions()).then(function(response) {return response.data; });
    },
    deleteNaturalFeature: function(layerId, nfid) {
        let url = '/nfdapi/layers/' + layerId + '/' + nfid + '/';
        return axios.delete(url, getOptions()).then(function(response) {return response.data; });
    },
    getFeatureSubtype: function(featuresubtype) {
        let url = '/nfdapi/featuretypes/' + featuresubtype + '/';
        const cached = dataCache[url];
        if (cached && new Date().getTime() < cached.timestamp + (ConfigUtils.getConfigProp('cacheDataExpire') || 600) * 1000) {
            return new Promise((resolve) => {
                resolve(cached.data);
            });
        }
        return axios.get(url, getOptions()).then(function(response) {
            dataCache[url] = {
                timestamp: new Date().getTime(),
                data: response.data
            };
            return response.data;
        });
    },
    getFeatureType: function(ftype, nfid) {
        let url = '/nfdapi/featuretypes/' + ftype + '/' + nfid + '/';
        return axios.get(url, getOptions()).then(function(response) {return response.data; });
    },
    getFeatureInfo: function(layerId, nfid) {
        let url = '/nfdapi/layers/' + layerId + '/' + nfid + '/';
        return axios.get(url, getOptions()).then(function(response) {return response.data; });
    },
    getSpecies: function(id) {
        let url = '/nfdapi/species/' + id + '/';
        return axios.get(url, getOptions()).then(function(response) {return response.data; });
    },
    searchSpecies: function(query) {
        let url = '/nfdapi/species/?search=' + query;
        return axios.get(url, getOptions()).then(function(response) {return response.data; });
    },
    createNewFeature: function(feature) {
        let url = '/nfdapi/layers/' + feature.featuretype + '/';
        return axios.post(url, feature, getOptions()).then(function(response) {return response.data; });
    },
    jwtLogin: function(user, password) {
        let url = '/nfdapi/api-token-auth/';
        return axios.post(url, {"username": user, "password": password}).then(function(response) {return response.data; });
    },
    getVersion: function(layerId, nfid, version) {
        let url = '/nfdapi/layers/' + layerId + '/' + nfid + '/version/' + version + '/';
        return axios.get(url, getOptions()).then((response) => {
            return response.data;
        });
    },
    uploadImage: function(image) {
        const url = '/nfdapi/images/';
        let data = new FormData();
        const blob = toBlob(image.dataUrl);
        data.append("image", blob, image.name);
        return axios.post(url, data, getOptions()).then(function(response) {return response.data; });
    },
    exportFeature: function(featureType, id, format) {
        let url = `/nfdapi/layers/${featureType}/${id}/?format=${format}`;
        const headers = assign({}, (getOptions()).headers, getAccept(format));
        return axios.get(url, {headers, responseType: 'arraybuffer', timeout: 60000});
    },
    exportFeatureList: function(featureType, format, filter, page) {
        let url = `/nfdapi/list/${featureType}/?format=${format}${page}${filter}`;
        const headers = assign({}, (getOptions()).headers, getAccept(format));
        return axios.get(url, {headers, responseType: 'arraybuffer', timeout: 60000});
    }
};

module.exports = Api;
