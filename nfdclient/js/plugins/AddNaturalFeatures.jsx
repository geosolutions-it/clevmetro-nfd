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
const {addNaturalFeature, saveNaturalFeature} = require('../actions/naturalfeatures');
const {changeDrawingStatus, endDrawing} = require('../../MapStore2/web/client/actions/draw');

const Message = require('../../MapStore2/web/client/components/I18N/Message');

const {DropdownButton, MenuItem, Glyphicon} = require('react-bootstrap');

const SmartDockedNaturalFeatures = connect((state) => ({
    isVisible: state.controls.addnaturalfeatures && state.controls.addnaturalfeatures.enabled,
    naturalFeatureType: state.naturalfeatures.naturalFeatureType,
    currentFeature: state.naturalfeatures.newFeature,
    dockSize: state.naturalfeatures.dockSize,
    mode: state.naturalfeatures.mode,
    isAdmin: true
}), {
    onToggle: toggleControl.bind(null, 'addnaturalfeatures', null),
    onSave: saveNaturalFeature.bind(null),
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
                    <MenuItem onClick={() => this.props.onToggleNewNaturalFeature("refinerias.43")}><Message msgId="naturalfeatures.animals"/></MenuItem>
                    <MenuItem onClick={() => this.props.onToggleNewNaturalFeature("mushrooms")}><Message msgId="naturalfeatures.mushrooms"/></MenuItem>
                    <MenuItem onClick={() => this.props.onToggleNewNaturalFeature("plants")}><Message msgId="naturalfeatures.plants"/></MenuItem>
                    <MenuItem onClick={() => this.props.onToggleNewNaturalFeature("naturalarea")}><Message msgId="naturalfeatures.naturalarea"/></MenuItem>
                    <MenuItem onClick={() => this.props.onToggleNewNaturalFeature("slimemold")}><Message msgId="naturalfeatures.slimemold"/></MenuItem>
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
        onToggleNewNaturalFeature: addNaturalFeature
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
