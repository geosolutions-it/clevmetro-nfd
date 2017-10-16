/**
 * Copyright 2016, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const React = require('react');
const ReactDOM = require('react-dom');
const {connect} = require('react-redux');
const appReducers = {
    naturalfeatures: require('./reducers/naturalfeatures'),
    selection: require('../MapStore2/web/client/reducers/selection')
};

const dEpics = require('./epics/naturalfeatures');
require('./components/map/LeafletClusterMarker.js');

const StandardApp = require('../MapStore2/web/client/components/app/StandardApp');

const {pages, pluginsDef, initialState, storeOpts} = require('./appConfig');
const axios = require('../MapStore2/web/client/libs/ajax');
const Cookies = require('cookies-js');

if (Cookies.get('csrftoken')) {
    axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
}
const themeCfg = {
    path: '/static/js'
};
const StandardRouter = connect((state) => ({
    locale: state.locale || {},
    themeCfg,
    pages
}))(require('../MapStore2/web/client/components/app/StandardRouter'));

const appStore = require('../MapStore2/web/client/stores/StandardStore').bind(null, initialState, appReducers, {...dEpics});

const initialActions = [];

const appConfig = {
    storeOpts,
    appStore,
    pluginsDef,
    initialActions,
    appComponent: StandardRouter
};

ReactDOM.render(
    <StandardApp {...appConfig}/>,
    document.getElementById('container')
);
