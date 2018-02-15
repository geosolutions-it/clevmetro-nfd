/**
 * Copyright 2018, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

var Layers = require('../../MapStore2/web/client/utils/leaflet/Layers');
var L = require('leaflet');

Layers.registerType('clevmetro', (opt) => {
    const clevUrls = {
        Map: 'https://api.mapbox.com/styles/v1/cleveland-metroparks/cisvvmgwe00112xlk4jnmrehn/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiY2xldmVsYW5kLW1ldHJvcGFya3MiLCJhIjoiWHRKaDhuRSJ9.FGqNSOHwiCr2dmTH2JTMAA',
        Arial: 'https://api.mapbox.com/styles/v1/cleveland-metroparks/cjcutetjg07892ro6wunp2da9/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiY2xldmVsYW5kLW1ldHJvcGFya3MiLCJhIjoiWHRKaDhuRSJ9.FGqNSOHwiCr2dmTH2JTMAA'
    };
    return L.tileLayer(clevUrls[opt.name], opt);
});
