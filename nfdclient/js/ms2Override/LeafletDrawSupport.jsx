/**
 * Copyright 2016, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');
var L = require('leaflet');
require('leaflet-draw');
const isMobile = require('ismobilejs');

const CoordinatesUtils = require('../../MapStore2/web/client/utils/CoordinatesUtils');

const LeafletDrawSupport = React.createClass({
    propTypes: {
        map: React.PropTypes.object,
        drawOwner: React.PropTypes.string,
        drawStatus: React.PropTypes.string,
        drawMethod: React.PropTypes.string,
        features: React.PropTypes.array,
        onChangeDrawingStatus: React.PropTypes.func,
        onEndDrawing: React.PropTypes.func,
        messages: React.PropTypes.object
    },
    getDefaultProps() {
        return {
            map: null,
            drawOwner: null,
            drawStatus: null,
            drawMethod: null,
            features: null,
            onChangeDrawingStatus: () => {},
            onEndDrawing: () => {}
        };
    },
    componentWillReceiveProps(newProps) {
        let drawingStrings = this.props.messages || (this.context.messages) ? this.context.messages.drawLocal : false;
        if (drawingStrings) {
            L.drawLocal = drawingStrings;
        }
        if (this.props.drawStatus !== newProps.drawStatus || this.props.drawMethod !== newProps.drawMethod) {
            switch (newProps.drawStatus) {
                case ("start"):
                    if (isMobile.any) {
                        this.addMobileDrawInteraction(newProps);
                    } else {
                        this.addDrawInteraction(newProps);
                        // this.addMobileDrawInteraction(newProps);
                    }
                    break;
                case ("stop"):
                    this.removeDrawInteraction();
                    break;
                case ("clean"):
                    this.clean();
                    break;
                default :
                    return;
            }
        }
    },
    onDraw: {
        drawStart() {
            this.drawing = true;
        }
    },
    render() {
        return null;
    },
    addMarkerLayer: function(newProps) {
        // this.cleanMarkerLayer();

        let smallIcon = new L.Icon({
            iconUrl: newProps.options.icon,
            iconAnchor: [12, 40]
        });
        let vector = L.geoJson(null, {
            pointToLayer: function(feature, latLng) {
                let center = CoordinatesUtils.reproject({x: latLng.lng, y: latLng.lat}, feature.projection, "EPSG:4326");
                let marker = L.marker(L.latLng(center.y, center.x), {
                    icon: smallIcon
                });
                return marker;
            }
        });
        this.props.map.addLayer(vector);
        this.drawMarkerLayer = vector;
    },
    addDrawInteraction: function(newProps) {
        if (!this.drawMarkerLayer) {
            this.addMarkerLayer(newProps);
        }

        this.removeDrawInteraction();
        const customProps = newProps.options.properties;
        this.props.map.on('draw:created', function(evt) {
            this.drawing = false;
            const layer = evt.layer;
            // let drawn geom stay on the map
            let geoJesonFt = layer.toGeoJSON();
            if (evt.layerType === "marker") {
                geoJesonFt.projection = "EPSG:4326";
                geoJesonFt.radius = layer.getRadius ? layer.getRadius() : 0;
                geoJesonFt.properties.featuretype = customProps.featuretype;
                geoJesonFt.properties.featuresubtype = customProps.featuresubtype;
                this.drawMarkerLayer.addData(geoJesonFt);
            }
            let newFeature = {
                featuretype: customProps.featuretype,
                featuresubtype: customProps.featuresubtype,
                geom: {
                    type: "Point",
                    coordinates: geoJesonFt.geometry.coordinates
                }
            };
            this.props.onChangeDrawingStatus('stop', this.props.drawMethod, this.props.drawOwner);
            this.props.onEndDrawing(newFeature, this.props.drawOwner);
        }, this);
        this.props.map.on('draw:drawstart', this.onDraw.drawStart, this);

        if (newProps.drawMethod === 'Marker') {
            let NaturalFeatureMarker = L.Icon.extend({
                options: {
                    iconUrl: newProps.options.icon/*,
                    iconAnchor: [12, 40]*/
                }
            });
            this.drawControl = new L.Draw.Marker(this.props.map, {
                icon: new NaturalFeatureMarker(),
                repeatMode: true
            });
        }

        // start the draw control
        this.drawControl.enable(newProps);
    },
    addMobileDrawInteraction: function(newProps) {
        if (!this.drawMarkerLayer) {
            this.addMarkerLayer(newProps);
        }
        this.removeMobileDrawInteraction();
        navigator.geolocation.getCurrentPosition((currentPosition) => {
            this.drawing = false;
            let smallIcon = new L.Icon({
                iconUrl: newProps.options.icon/*,
                iconAnchor: [12, 40]*/
            });
            let marker = L.marker(L.latLng(currentPosition.coords.latitude, currentPosition.coords.longitude), {
                icon: smallIcon
            });// .addTo(this.props.map);
            // let drawn geom stay on the map
            let geoJesonFt = marker.toGeoJSON();

            geoJesonFt.projection = "EPSG:4326";
            geoJesonFt.radius = marker.getRadius ? marker.getRadius() : 0;
            geoJesonFt.properties.featuretype = newProps.options.properties.featuretype;
            geoJesonFt.properties.featuresubtype = newProps.options.properties.featuresubtype;
            this.drawMarkerLayer.addData(geoJesonFt);

            let newFeature = {
                featuretype: newProps.options.properties.featuretype,
                featuresubtype: newProps.options.properties.featuresubtype,
                geom: {
                    type: "Point",
                    coordinates: geoJesonFt.geometry.coordinates
                }
            };

            this.props.onChangeDrawingStatus('stop', this.props.drawMethod, this.props.drawOwner);
            this.props.onEndDrawing(newFeature, this.props.drawOwner);

        }, (error) => {
            if (error.code === 1) {
                console.log('Error');
            }
        });
    },
    removeDrawInteraction: function() {
        if (this.drawControl !== null && this.drawControl !== undefined) {
            // Needed if missin disable() isn't warking
            this.drawControl.setOptions({repeatMode: false});
            this.drawControl.disable();
            this.drawControl = null;
            this.props.map.off('draw:created');
            this.props.map.off('draw:drawstart', this.onDraw.drawStart, this);
        }
    },
    removeMobileDrawInteraction: function() {},
    cleanMarkerLayer: function() {
        this.removeDrawInteraction();

        if (this.drawMarkerLayer) {
            this.drawMarkerLayer.clearLayers();
            this.props.map.removeLayer(this.drawMarkerLayer);
            this.drawMarkerLayer = null;
        }
    },
    clean: function() {
        this.cleanMarkerLayer();
    }
});

module.exports = LeafletDrawSupport;
