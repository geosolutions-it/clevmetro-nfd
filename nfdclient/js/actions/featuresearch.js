/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const TOGGLE_FEATURETYPE = 'TOGGLE_FEATURETYPE';
const LOAD_LIST = 'LOAD_LIST';
const LIST_LOADED = 'LIST_LOADED';
const LIST_LOAD_ERROR = 'LIST_LOAD_ERROR';
const LIST_LOADING = 'LIST_LOADING';
const SELECT_FEATURE = 'SELECT_FEATURE';
const ZOOM_TO_NFD_FEATURE = 'ZOOM_TO_NFD_FEATURE';
const SEARCH_SPECIES = 'SEARCH_SPECIES';
const SEARCH_SPECIES_RESULT = 'SEARCH_SPECIES_RESULT';
const SEARCH_SPECIES_ERROR = 'SEARCH_SPECIES_ERROR';
const SET_FILTER_PROP = 'SET_FILTER_PROP';
const RESET_FEATURETYPE_FILTERS = 'RESET_FEATURETYPE_FILTERS';

function resetFtFilters(fttype) {
    return {
        type: RESET_FEATURETYPE_FILTERS,
        fttype
    };
}

function setFilterProp(fttype, prop, value) {
    return {
        type: SET_FILTER_PROP,
        fttype, prop, value
    };
}
function onSearchSepciesError(featureType, e) {
    return {
        type: SEARCH_SPECIES_ERROR,
        e,
        featureType
    };
}

function onSearchSepciesResult(featureType, options) {
    return {
        type: SEARCH_SPECIES_RESULT,
        options,
        featureType
    };
}

function searchSpecies(featureType, query) {
    return {
        type: SEARCH_SPECIES,
        query,
        featureType
    };
}

function zooToFeature(feature, zoom = 16) {
    return {
        type: ZOOM_TO_NFD_FEATURE,
        feature,
        zoom
    };
}
function selectFeature(nfId, properties) {
    return {
        type: SELECT_FEATURE,
        nfId, properties
    };
}

function onListLoading(loading = true, fttype = 'all') {
    return {
        type: LIST_LOADING,
        loading,
        fttype
    };
}

function onLoadListError(fttype, error) {
    return {
        type: LIST_LOAD_ERROR,
        fttype,
        error
    };
}

function listLoaded(fttype, data, page = 0, filter = {}) {
    return {
        type: LIST_LOADED,
        fttype,
        features: data.results.features || [],
        total: data.count,
        page,
        filter
    };
}
function loadList(fttype, page = 1) {
    return {
        type: LOAD_LIST,
        fttype,
        page
    };
}

function toggleFeatureType(activekey) {
    return {
        type: TOGGLE_FEATURETYPE,
        activekey
    };
}

module.exports = {
    TOGGLE_FEATURETYPE, toggleFeatureType,
    LOAD_LIST, loadList,
    LIST_LOADED, listLoaded,
    LIST_LOAD_ERROR, onLoadListError,
    LIST_LOADING, onListLoading,
    SELECT_FEATURE, selectFeature,
    ZOOM_TO_NFD_FEATURE, zooToFeature,
    SEARCH_SPECIES, searchSpecies,
    SEARCH_SPECIES_RESULT, onSearchSepciesResult,
    SEARCH_SPECIES_ERROR, onSearchSepciesError,
    SET_FILTER_PROP, setFilterProp,
    RESET_FEATURETYPE_FILTERS, resetFtFilters
};
