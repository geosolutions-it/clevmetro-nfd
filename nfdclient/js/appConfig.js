/**
 * Copyright 2016, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

module.exports = {
    pages: [{
        name: "main",
        path: "/*",
        component: require('./pages/Main')
    }],
    pluginsDef: require('./plugins.js'),
    initialState: {
        defaultState: {
            naturalfeatures: {
                naturalFeatureType: [],
                selectedFeature: {},
                newFeature: {},
                dockSize: 0.35
            }
        },
        mobile: {
            naturalfeatures: {
                dockSize: 1.0
            }
        }
    }
};
