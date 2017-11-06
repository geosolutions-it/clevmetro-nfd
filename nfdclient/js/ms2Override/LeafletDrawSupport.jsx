/**
 * Copyright 2016, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');
const L = require('leaflet');
require('leaflet-draw');
const {isObject} = require('lodash');
const {connect} = require('react-redux');
const {editClicked} = require('../actions/naturalfeatures');
// const isMobile = require('ismobilejs');

// const CoordinatesUtils = require('../../MapStore2/web/client/utils/CoordinatesUtils');
const Utils = require('../utils/nfdUtils');
const LeafletDrawSupport = React.createClass({
    propTypes: {
        map: React.PropTypes.object,
        drawOwner: React.PropTypes.string,
        drawStatus: React.PropTypes.string,
        drawMethod: React.PropTypes.string,
        features: React.PropTypes.array,
        onChangeDrawingStatus: React.PropTypes.func,
        onEndDrawing: React.PropTypes.func,
        messages: React.PropTypes.object,
        options: React.PropTypes.object,
        onClick: React.PropTypes.func
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
        const {options} = this.props;
        const featuretype = (options && options.properties || {}).featuretype;
        const {options: newOptions} = newProps;
        const newFeaturetype = (newOptions && newOptions.properties || {}).featuretype;
        switch (newProps.drawStatus) {
            case ("start"):
                if (newProps.drawMethod !== "MarkerReplace" && newProps.drawMethod !== "Polygon" ) {
                    this.clean();
                }
                this.addDrawInteraction(newProps);
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
                if (featuretype && featuretype !== newFeaturetype) {
                    this.clean();
                }
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
    onClick: function() {
        const {options, onClick} = this.props;
        const id = options && options.properties && options.properties.id;
        if (onClick) {
            onClick(id);
        }
    },
    render() {
        return null;
    },
    addMarkerLayer: function(style) {
        let icon;
        if (this.drawMarkerLayer) {
            return;
        }
        if (style.iconUrl) {
            icon = new L.Icon({
                iconUrl: style.iconUrl,
                iconAnchor: [12, 40]
            });
        }else if (style.html) {
            icon = L.divIcon(style.html);
        }
        let vector = L.geoJson(null, {
            pointToLayer: function(feature, latLng) {
                var marker;
                // let center = CoordinatesUtils.reproject({x: latLng.lng, y: latLng.lat}, feature.projection, "EPSG:4326");
                if (icon) {
                    marker = L.marker(latLng, {
                        icon: icon
                    });
                } else {
                    marker = L.circleMarker(latLng, {
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
        this.drawMarkerLayer.on('click', this.onClick);
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
            let icon;
            if (newProps.options.icon.html) {
                icon = L.divIcon(newProps.options.icon.html);
            }else if (newProps.options.icon.iconUrl) {
                icon = new L.Icon({
                    iconUrl: newProps.options.icon.html.iconUrl,
                    iconAnchor: [12, 40]
                });
            }
            this.drawControl = new L.Draw.Marker(this.props.map, {
                icon,
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
    cleanMarkerLayer: function() {
        this.removeDrawInteraction();

        if (this.drawMarkerLayer) {
            this.drawMarkerLayer.off('click', this.onClick);
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
            let feature = {geometry: isObject(props.geom) ? props.geom : JSON.parse(props.geom), properties: props, type: "Feature", projection: "EPSG:4326"};
            this.addMarkerLayer(Utils.getIcon(props.featuretype));
            this.drawMarkerLayer.clearLayers();
            this.drawMarkerLayer.addData(feature);
        }
    },
    drawPolygon: function(props) {
        this.addPolygonLayer();
        this.drawPolygonLayer.clearLayers();
        if (props.polygon) {
            let feature = {geometry: isObject(props.polygon) ? props.polygon : JSON.parse(props.polygon), properties: props, type: "Feature", projection: "EPSG:4326"};
            this.drawPolygonLayer.addData(feature);
        } else if (props.geometry) {
            this.drawPolygonLayer.addData(props);
        }
    }
});

module.exports = connect(()=> ({}), {onClick: editClicked})(LeafletDrawSupport);
