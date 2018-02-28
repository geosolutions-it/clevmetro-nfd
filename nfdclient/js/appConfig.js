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
            controls: {
                LoginForm: {
                    enabled: false
                }
            },
            naturalfeatures: {
                forms: [],
                featuretype: "",
                featuresubtype: "",
                selectedFeature: {},
                newFeature: {},
                errors: {},
                dockSize: 0.35
            },
            featuresearch: {
                featureTypes: ['animal', 'plant', 'fungus', 'slimemold', 'naturalarea'],
                pageSize: 10,
                defaultOperator: '>'
            }
        },
        mobile: {
            naturalfeatures: {
                dockSize: 1.0
            },
            featuresearch: {
                featureTypes: ['animal', 'plant', 'fungus', 'slimemold', 'naturalarea'],
                pageSize: 10,
                defaultOperator: '>'
            }
        }
    },
    storeOpts: {
        persist: {
            whitelist: ['security']
        }
    }
};
