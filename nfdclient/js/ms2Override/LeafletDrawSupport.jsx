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
        // this.clean();
        let drawingStrings = this.props.messages || (this.context.messages) ? this.context.messages.drawLocal : false;
        if (drawingStrings) {
            L.drawLocal = drawingStrings;
        }
        switch (newProps.drawStatus) {
            case ("start"):
                if (isMobile.any) {
                    // this.addMobileDrawInteraction(newProps);
                    this.addDrawInteraction(newProps);
                } else {
                    this.addDrawInteraction(newProps);
                }
                break;
            case ("stop"):
                this.removeDrawInteraction();
                break;
            case ("clean"):
                this.clean();
                break;
            case ("featureSelected"):
                this.selectFeature(newProps.options.lflFeat);
                break;
            case ("featureDeselected"):
                this.deselectFeature();
                break;
            case ("selectionGeomLoaded"):
                this.drawMarker(newProps.options.properties);
                this.drawPolygon(newProps.options.properties);
                break;
            default :
                return;
        }
    },
    onDraw: {
        drawStart() {
            this.drawing = true;
        }
    },
    getSelectionIconUrl() {
        try {
            return this.selectionHighlightIcon.options.iconUrl;
        } catch (e) {
            console.log(e);
        }
        return null;
    },
    render() {
        return null;
    },
    addMarkerLayer: function(iconUrl) {
        var smallIcon;
        if (this.drawMarkerLayer) {
            return;
        }
        if (iconUrl) {
            smallIcon = new L.Icon({
                iconUrl: iconUrl,
                iconAnchor: [12, 40]
            });
        }
        let vector = L.geoJson(null, {
            pointToLayer: function(feature, latLng) {
                var marker;
                let center = CoordinatesUtils.reproject({x: latLng.lng, y: latLng.lat}, feature.projection, "EPSG:4326");
                if (smallIcon) {
                    marker = L.marker(L.latLng(center.y, center.x), {
                        icon: smallIcon
                    });
                } else {
                    marker = L.circleMarker(L.latLng(center.y, center.x), {
                        color: '#ff0000',
                        opacity: 0.6,
                        weight: 2,
                        fillColor: '#ff0000',
                        fillOpacity: 0.2
                    });
                }
                return marker;
            }
        });
        this.props.map.addLayer(vector);
        this.drawMarkerLayer = vector;
    },
    addPolygonLayer: function() {
        if (this.drawPolygonLayer) {
            return;
        }
        let vector = L.geoJson();
        this.props.map.addLayer(vector);
        this.drawPolygonLayer = vector;
    },
    addDrawInteraction: function(newProps) {
        const drawMethod = newProps.drawMethod;
        if (drawMethod.includes("Marker")) {
            this.addMarkerLayer(newProps.options.icon);
        }
        if (drawMethod === "Polygon") {
            this.addPolygonLayer();
        }

        this.removeDrawInteraction();
        const customProps = newProps.options.properties;
        this.props.map.on('draw:created', function(evt) {
            let geomType;
            this.drawing = false;
            const layer = evt.layer;
            // let drawn geom stay on the map
            let geoJsonFt = layer.toGeoJSON();
            if (evt.layerType === "marker") {
                if (drawMethod === "MarkerReplace") {
                    this.deselectFeature();
                    this.drawMarkerLayer.clearLayers();
                }
                geoJsonFt.projection = "EPSG:4326";
                geoJsonFt.radius = layer.getRadius ? layer.getRadius() : 0;
                geoJsonFt.properties.featuretype = customProps.featuretype;
                geoJsonFt.properties.featuresubtype = customProps.featuresubtype;
                this.drawMarkerLayer.addData(geoJsonFt);
                geomType = "Point";
            } else if (evt.layerType === "polygon") {
                geoJsonFt.projection = "EPSG:4326";
                geoJsonFt.properties.featuretype = customProps.featuretype;
                geoJsonFt.properties.featuresubtype = customProps.featuresubtype;
                this.drawPolygon(geoJsonFt);
                geomType = "Polygon";
            }
            let newFeature = {
                featuretype: customProps.featuretype,
                featuresubtype: customProps.featuresubtype,
                drawMethod: drawMethod,
                geom: {
                    type: geomType,
                    coordinates: geoJsonFt.geometry.coordinates
                }
            };
            this.props.onChangeDrawingStatus('stop', this.props.drawMethod, this.props.drawOwner);
            this.props.onEndDrawing(newFeature, this.props.drawOwner);
        }, this);
        this.props.map.on('draw:drawstart', this.onDraw.drawStart, this);

        if (newProps.drawMethod === 'Marker' || newProps.drawMethod === 'MarkerReplace') {
            let NaturalFeatureMarker = L.Icon.extend({
                options: {
                    iconUrl: newProps.options.icon,
                    iconAnchor: [12, 40]
                }
            });
            this.drawControl = new L.Draw.Marker(this.props.map, {
                icon: new NaturalFeatureMarker(),
                repeatMode: false
            });
        } else if (newProps.drawMethod === 'Polygon') {
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
        }

        // start the draw control
        this.drawControl.enable(newProps);
    },
    addMobileDrawInteraction: function(newProps) {
        if (!this.drawMarkerLayer) {
            this.addMarkerLayer(newProps.options.icon);
        }
        this.removeMobileDrawInteraction();
        navigator.geolocation.getCurrentPosition((currentPosition) => {
            this.drawing = false;
            let smallIcon = new L.Icon({
                iconUrl: newProps.options.icon,
                iconAnchor: [12, 40]
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
        if (this.drawPolygonLayer) {
            this.drawPolygonLayer.clearLayers();
            this.props.map.removeLayer(this.drawPolygonLayer);
            this.drawPolygonLayer = null;
        }
    },
    clean: function() {
        this.cleanMarkerLayer();
        this.deselectFeature();
    },
    selectFeature: function(feat) {
        this.deselectFeature();
        this.selectedLeafletFeat = feat;
        feat.setIcon(feat.highlightIcon);
        this.selectionHighlightIcon = feat.highlightIcon;
    },
    deselectFeature: function() {
        if (this.selectedLeafletFeat) {
            this.selectedLeafletFeat.setIcon(this.selectedLeafletFeat.regularIcon);
            this.selectedLeafletFeat = null;
        }
    },
    drawMarker: function(props) {
        if (props.geom) {
            try {
                let feature = {geometry: props.geom, properties: props, type: "Feature", projection: "EPSG:4326"};
                this.addMarkerLayer(this.getSelectionIconUrl());
                this.drawMarkerLayer.clearLayers();
                this.deselectFeature();
                this.drawMarkerLayer.addData(feature);
            } catch(e) {
                console.log(e);
            }
        }
    },
    drawPolygon: function(props) {
        this.addPolygonLayer();
        this.drawPolygonLayer.clearLayers();
        if (props.polygon) {
            try {
                let feature = {geometry: JSON.parse(props.polygon), properties: props, type: "Feature", projection: "EPSG:4326"};
                this.drawPolygonLayer.addData(feature);
            } catch(e) {
                console.log(e);
            }
        } else if (props.geometry) {
            this.drawPolygonLayer.addData(props);
        }
    }
});

module.exports = LeafletDrawSupport;
