/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const assign = require('object-assign');
const {
 TOGGLE_FEATURETYPE,
 LIST_LOADED,
 LIST_LOAD_ERROR,
 LIST_LOADING,
 SEARCH_SPECIES_RESULT,
 SEARCH_SPECIES_ERROR,
 SET_FILTER_PROP,
 RESET_FEATURETYPE_FILTERS
} = require('../actions/featuresearch');

function featuresearch(state = {pageSize: 30, defualtOperator: '>'}, action) {
    let prop;
    switch (action.type) {
        case "LOGOUT": {
            let newState = assign({}, state, {loading: {}});
            (newState.featureTypes || []).forEach((ft) => {
                if (newState.hasOwnProperty(ft)) {
                    delete newState[ft];
                }
                if (newState.hasOwnProperty(`${ft}_filters`)) {
                    delete newState[`${ft}_filters`];
                }
            });
            return newState;
        }
        case TOGGLE_FEATURETYPE:
            return assign({}, state, {activeFt: action.activekey});
        case LIST_LOADED: {
            const {fttype, features, total, page, filter} = action;
            return assign({}, state, {[fttype]: {features, total, page, filter}});
        }
        case LIST_LOADING:
            return assign({}, state, {loading: assign({}, state.loading, {[action.fttype]: action.loading})});
        case LIST_LOAD_ERROR:
            return assign({}, state, {[action.fttype]: {error: action.error.statusText}});
        case SEARCH_SPECIES_RESULT:
            prop = `${action.featureType}_filters`;
            return assign({}, state, {[prop]: assign({}, state[prop], {species: action.options, selectedSpecies: undefined})});
        case SEARCH_SPECIES_ERROR:
            return assign({}, state, assign({}, state[`${action.featureType}_filter`], {species: []}));
        case SET_FILTER_PROP:
            prop = `${action.fttype}_filters`;
            return assign({}, state, {[prop]: assign({}, state[prop], {[action.prop]: action.value})});
        case RESET_FEATURETYPE_FILTERS:
            prop = `${action.fttype}_filters`;
            return assign({}, state, {[prop]: undefined});
        default:
            return state;
    }
}

module.exports = featuresearch;
