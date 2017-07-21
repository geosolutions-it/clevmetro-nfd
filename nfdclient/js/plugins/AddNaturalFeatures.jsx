/*
 * Copyright 2016, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');
const {connect} = require('react-redux');
const assign = require('object-assign');

const {toggleControl} = require('../../MapStore2/web/client/actions/controls');
const {createNaturalFeature/*, addNaturalFeature*/, naturalFeatureCreated, getSpecie, activateFeatureInsert} = require('../actions/naturalfeatures');
const {changeDrawingStatus, endDrawing} = require('../../MapStore2/web/client/actions/draw');

const Message = require('../../MapStore2/web/client/components/I18N/Message');

const {DropdownButton, MenuItem, Glyphicon} = require('react-bootstrap');

const SmartDockedNaturalFeatures = connect((state) => ({
    isVisible: state.controls.addnaturalfeatures && state.controls.addnaturalfeatures.enabled,
    forms: state.naturalfeatures.forms,
    featuretype: state.naturalfeatures.featuretype,
    featuresubtype: state.naturalfeatures.featuresubtype,
    currentFeature: state.naturalfeatures.selectedFeature,
    errors: state.naturalfeatures.errors,
    dockSize: state.naturalfeatures.dockSize,
    mode: state.naturalfeatures.mode,
    isAdmin: true
}), {
    onToggle: toggleControl.bind(null, 'addnaturalfeatures', null),
    onUpdate: naturalFeatureCreated.bind(null),
    getSpecie: getSpecie.bind(null),
    onChangeDrawingStatus: changeDrawingStatus,
    onEndDrawing: endDrawing
})(require('../components/naturalfeatures/DockedNaturalFeatures'));
require('../components/naturalfeatures/DockedNaturalFeatures.css');

const AddNaturalFeatures = React.createClass({
    propTypes: {
        active: React.PropTypes.string,
        onToggleNewNaturalFeature: React.PropTypes.func,
        glyph: React.PropTypes.string,
        buttonStyle: React.PropTypes.string,
        menuOptions: React.PropTypes.object,
        buttonClassName: React.PropTypes.string,
        menuButtonStyle: React.PropTypes.object,
        disabled: React.PropTypes.bool,
        visible: React.PropTypes.bool
    },
    getDefaultProps() {
        return {
            onToggleNewNaturalFeature: () => {},
            glyph: "paw",
            buttonStyle: "primary",
            menuOptions: {},
            buttonClassName: "square-button",
            disabled: false,
            visible: false
        };
    },
    render() {
        return (
            this.props.visible ?
            (<div>
                <DropdownButton id="addnf-menu-button" className={this.props.buttonClassName} pullRight bsStyle={this.props.buttonStyle} title={<Glyphicon glyph={this.props.glyph} />}>
                    {/* <MenuItem disabled={true} onClick={() => this.props.onToggleNewNaturalFeature({"featuretype": "plant", "featuresubtype": "co"})}><Message msgId="naturalfeatures.conifer"/></MenuItem>
                    <MenuItem disabled={true} onClick={() => this.props.onToggleNewNaturalFeature({"featuretype": "plant", "featuresubtype": "fe"})}><Message msgId="naturalfeatures.fern"/></MenuItem>
                    <MenuItem disabled={true} onClick={() => this.props.onToggleNewNaturalFeature({"featuretype": "plant", "featuresubtype": "fl"})}><Message msgId="naturalfeatures.flowering_plant"/></MenuItem>
                    <MenuItem disabled={true} onClick={() => this.props.onToggleNewNaturalFeature({"featuretype": "plant", "featuresubtype": "pl"})}><Message msgId="naturalfeatures.plant_generic"/></MenuItem>
                    <MenuItem disabled={true} onClick={() => this.props.onToggleNewNaturalFeature({"featuretype": "plant", "featuresubtype": "mo"})}><Message msgId="naturalfeatures.moss"/></MenuItem>
                    <MenuItem disabled={true} onClick={() => this.props.onToggleNewNaturalFeature({"featuretype": "fungus", "featuresubtype": "fu"})}><Message msgId="naturalfeatures.fungus"/></MenuItem> */}
                    <MenuItem onClick={() => this.props.onToggleNewNaturalFeature({"featuretype": "slimemold", "featuresubtype": "sl"})}><Message msgId="naturalfeatures.slimemold"/></MenuItem>
                    <MenuItem onClick={() => this.props.onToggleNewNaturalFeature({"featuretype": "animal", "featuresubtype": "ln"})}><Message msgId="naturalfeatures.land_animal"/></MenuItem>
                    <MenuItem onClick={() => this.props.onToggleNewNaturalFeature({"featuretype": "animal", "featuresubtype": "lk"})}><Message msgId="naturalfeatures.pond_lake_animal"/></MenuItem>
                    <MenuItem onClick={() => this.props.onToggleNewNaturalFeature({"featuretype": "animal", "featuresubtype": "st"})}><Message msgId="naturalfeatures.stream_animal"/></MenuItem>
                    <MenuItem onClick={() => this.props.onToggleNewNaturalFeature({"featuretype": "animal", "featuresubtype": "we"})}><Message msgId="naturalfeatures.wetland_animal"/></MenuItem>
                    {/*<MenuItem disabled={true} onClick={() => this.props.onToggleNewNaturalFeature({"featuretype": "naturalarea", "featuresubtype": "na"})}><Message msgId="naturalfeatures.naturalarea"/></MenuItem>*/}
                </DropdownButton>
                <SmartDockedNaturalFeatures mode="add"/>
            </div>) : null
        );
    }
});

module.exports = {
    AddNaturalFeaturesPlugin: assign(connect((state) => ({
        active: state.controls && state.controls.addnaturalfeatures && state.controls.addnaturalfeatures.active,
        disabled: state.controls && state.controls.addnaturalfeatures && state.controls.addnaturalfeatures.disabled,
        visible: true
    }), {
        onToggleNewNaturalFeature: activateFeatureInsert
    })(AddNaturalFeatures), {
        OmniBar: {
            name: "addnf",
            position: 5,
            tool: true,
            priority: 1
        }
    }),
    reducers: {
        naturalfeatures: require('../reducers/naturalfeatures')
    }
};
