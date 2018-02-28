/**
 * Copyright 2015, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const { LOGIN_FAIL, LOGOUT, RESET_ERROR } = require('../../MapStore2/web/client/actions/security');
const {
    NFD_LOGIN_SUCCESS
} = require('../actions/naturalfeatures');

const assign = require('object-assign');

function getAttribute(details) {
    return [{"name": "name", "value": details.name}];
}

function security(state = {user: null, errorCause: null}, action) {
    switch (action.type) {
        case NFD_LOGIN_SUCCESS: {
            return assign({}, state, {
                user: assign({}, action.userDetails, {attribute: getAttribute(action.userDetails)}),
                token: action.token || '',
                authHeader: action.authHeader,
                loginError: null
            });
        }
        case LOGIN_FAIL:
            return assign({}, state, {
                loginError: action.error
            });
        case RESET_ERROR:
            return assign({}, state, {
                loginError: null
            });
        case LOGOUT:
            return assign({}, state, {
                user: null,
                token: null,
                authHeader: null,
                loginError: null
            });
        case "persist/REHYDRATE": {
            return action.payload && action.payload.security || {user: null, errorCause: null};
        }
        default:
            return state;
    }
}

module.exports = security;
