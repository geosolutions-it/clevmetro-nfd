/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/

const Layers = require('../../../MapStore2/web/client/utils/leaflet/Layers');
const L = require('leaflet');
require('leaflet.markercluster');
require('leaflet.markercluster/dist/MarkerCluster.Default.css');
require('leaflet.markercluster/dist/MarkerCluster.css');

const defaultStyle = {
    radius: 5,
    color: "red",
    weight: 1,
    opacity: 1,
    fillOpacity: 0
};

const assign = require('object-assign');

const createClusterMarkerLayer = function(options) {
    const {hideLoading} = options;
    const layer = L.markerClusterGroup({
        chunkedLoading: true,
        hideLoading: hideLoading,
        iconCreateFunction: function(cluster) {
            return L.divIcon({
                        html: `<div><span>${cluster.getChildCount()}</span></div>`,
                        className: `marker-cluster marker-cluster-${options.id}`,
                        iconSize: [40, 40],
                        iconAnchor: [20, 20]
                    });
        }
    });
    layer.setOpacity = (opacity) => {
        const style = assign({}, layer.options.style || defaultStyle, {opacity: opacity, fillOpacity: opacity});
        layer.setStyle(style);
    };

    return layer;
};

Layers.registerType('clustermarker', {
    create: (options) => {
        return createClusterMarkerLayer(options);
    },
    render: () => {
        return null;
    }
});
