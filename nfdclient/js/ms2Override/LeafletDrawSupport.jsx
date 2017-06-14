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
                    this.addDrawInteraction(newProps);
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
        },
        created(evt) {
            this.drawing = false;
            const layer = evt.layer;
            // let drawn geom stay on the map
            let geoJesonFt = layer.toGeoJSON();
            if (evt.layerType === "polygon") {
                geoJesonFt.projection = "EPSG:4326";
                this.drawPolygonLayer.addData(geoJesonFt);

            } else if (evt.layerType === "marker") {
                geoJesonFt.projection = "EPSG:4326";
                geoJesonFt.radius = layer.getRadius ? layer.getRadius() : 0;
                this.drawMarkerLayer.addData(geoJesonFt);
            }

            this.props.onChangeDrawingStatus('stop', this.props.drawMethod, this.props.drawOwner);
            // this.props.onEndDrawing(geometry, this.props.drawOwner);
        }
    },
    render() {
        return null;
    },
    addMarkerLayer: function(newProps) {
        this.cleanMarkerLayer();

        let smallIcon = new L.Icon({
            iconUrl: newProps.options.icon,
            iconAnchor: [12, 40]
        });
        let vector = L.geoJson(null, {
            pointToLayer: function(feature, latLng) {
                let center = CoordinatesUtils.reproject({x: latLng.lng, y: latLng.lat}, feature.projection, "EPSG:4326");
                // return L.circle(L.latLng(center.y, center.x), feature.radius);
                return L.marker(L.latLng(center.y, center.x), {
                  icon: smallIcon
                });
            }
        });
        this.props.map.addLayer(vector);
        this.drawMarkerLayer = vector;
    },
    addPolygonLayer: function() {
        this.cleanPolygonLayer();

        let vector = L.geoJson(null, {});
        this.props.map.addLayer(vector);
        this.drawPolygonLayer = vector;
    },
    addDrawInteraction: function(newProps) {
        if (newProps.drawMethod === 'Polygon' && !this.drawPolygonLayer) {
            this.addPolygonLayer(newProps);
        } else if (newProps.drawMethod === 'Marker' && !this.drawMarkerLayer) {
            this.addMarkerLayer(newProps);
        } else if (newProps.drawMethod === 'Marker' && this.drawMarkerLayer) {
            this.drawMarkerLayer.clearLayers();
        } else if (newProps.drawMethod === 'Polygon' && this.drawPolygonLayer) {
            this.drawPolygonLayer.clearLayers();
        }

        this.removeDrawInteraction();

        this.props.map.on('draw:created', this.onDraw.created, this);
        this.props.map.on('draw:drawstart', this.onDraw.drawStart, this);

        if (newProps.drawMethod === 'Polygon') {
            this.drawControl = new L.Draw.Polygon(this.props.map, {
                shapeOptions: {
                    color: '#000000',
                    weight: 2,
                    fillColor: '#ffffff',
                    fillOpacity: 0.2,
                    dashArray: [5, 5],
                    guidelineDistance: 5
                },
                repeatMode: true
            });
        } else if (newProps.drawMethod === 'Marker') {
            let NaturalFeatureMarker = L.Icon.extend({
                options: {
                    iconUrl: newProps.options.icon,
                    iconAnchor: [12, 40]
                }
            });
            this.drawControl = new L.Draw.Marker(this.props.map, {
                icon: new NaturalFeatureMarker(),
                repeatMode: true
            });
        }

        // start the draw control
        this.drawControl.enable();
    },
    removeDrawInteraction: function() {
        if (this.drawControl !== null && this.drawControl !== undefined) {
            // Needed if missin disable() isn't warking
            this.drawControl.setOptions({repeatMode: false});
            this.drawControl.disable();
            this.drawControl = null;
            this.props.map.off('draw:created', this.onDraw.created, this);
            this.props.map.off('draw:drawstart', this.onDraw.drawStart, this);
        }
    },
    cleanMarkerLayer: function() {
        this.removeDrawInteraction();

        if (this.drawMarkerLayer) {
            this.drawMarkerLayer.clearLayers();
            this.props.map.removeLayer(this.drawMarkerLayer);
            this.drawMarkerLayer = null;
        }
    },
    cleanPolygonLayer: function() {
        this.removeDrawInteraction();

        if (this.drawPolygonLayer) {
            this.drawPolygonLayer.clearLayers();
            this.props.map.removeLayer(this.drawPolygonLayer);
            this.drawPolygonLayer = null;
        }
    },
    clean: function() {
        this.cleanMarkerLayer();
        this.cleanPolygonLayer();
    }
});

module.exports = LeafletDrawSupport;
