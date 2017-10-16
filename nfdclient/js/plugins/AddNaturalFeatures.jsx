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
const {naturalFeatureCreated, getSpecies, addFeature, cancel} = require('../actions/naturalfeatures');
const {changeDrawingStatus, endDrawing} = require('../../MapStore2/web/client/actions/draw');

const Message = require('../../MapStore2/web/client/components/I18N/Message');

const {DropdownButton, MenuItem, Glyphicon} = require('react-bootstrap');

const {isWriter, isPublisher} = require('./naturalfeatures/securityutils.js');

const SmartDockedNaturalFeatures = connect((state) => ({
    isVisible: state.controls.addnaturalfeatures && state.controls.addnaturalfeatures.enabled,
    forms: state.naturalfeatures.forms,
    featuretype: state.naturalfeatures.featuretype,
    featuresubtype: state.naturalfeatures.featuresubtype,
    currentFeature: state.naturalfeatures.selectedFeature,
    errors: state.naturalfeatures.errors,
    dockSize: state.naturalfeatures.dockSize,
    mode: state.naturalfeatures.mode,
    isAdmin: state.naturalfeatures.is_admin || false,
    isWriter: isWriter(state),
    isPublisher: isPublisher(state)
}), {
    onToggle: toggleControl.bind(null, 'addnaturalfeatures', null),
    onUpdate: naturalFeatureCreated.bind(null),
    getSpecies: getSpecies.bind(null),
    onChangeDrawingStatus: changeDrawingStatus,
    onEndDrawing: endDrawing,
    cancel
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
        visible: React.PropTypes.bool,
        plant_writer: React.PropTypes.bool,
        animal_writer: React.PropTypes.bool,
        slimemold_writer: React.PropTypes.bool,
        fungus_writer: React.PropTypes.bool,
        naturalarea_writer: React.PropTypes.bool
    },
    getDefaultProps() {
        return {
            onToggleNewNaturalFeature: () => {},
            glyph: "paw",
            buttonStyle: "primary",
            menuOptions: {},
            buttonClassName: "square-button",
            disabled: false,
            visible: false,
            plant_writer: false,
            animal_writer: false,
            slimemold_writer: false,
            fungus_writer: false,
            naturalarea_writer: false
        };
    },
    render() {
        return (
            <div>
                <DropdownButton disabled={this.props.disabled} id="addnf-menu-button" className={this.props.buttonClassName} pullRight bsStyle={this.props.buttonStyle} title={<Glyphicon glyph={this.props.glyph} />}>
                    {this.props.plant_writer &&
                        <MenuItem onClick={() => this.props.onToggleNewNaturalFeature({"featuretype": "plant", "featuresubtype": "co"})}><Message msgId="naturalfeatures.conifer"/></MenuItem>
                    }
                    {this.props.plant_writer &&
                        <MenuItem onClick={() => this.props.onToggleNewNaturalFeature({"featuretype": "plant", "featuresubtype": "fe"})}><Message msgId="naturalfeatures.fern"/></MenuItem>
                    }
                    {this.props.plant_writer &&
                        <MenuItem onClick={() => this.props.onToggleNewNaturalFeature({"featuretype": "plant", "featuresubtype": "fl"})}><Message msgId="naturalfeatures.flowering_plant"/></MenuItem>
                    }
                    {this.props.plant_writer && false &&
                        <MenuItem onClick={() => this.props.onToggleNewNaturalFeature({"featuretype": "plant", "featuresubtype": "pl"})}><Message msgId="naturalfeatures.plant_generic"/></MenuItem>
                    }
                    {this.props.plant_writer &&
                        <MenuItem onClick={() => this.props.onToggleNewNaturalFeature({"featuretype": "plant", "featuresubtype": "mo"})}><Message msgId="naturalfeatures.moss"/></MenuItem>
                    }
                    {this.props.fungus_writer &&
                        <MenuItem onClick={() => this.props.onToggleNewNaturalFeature({"featuretype": "fungus", "featuresubtype": "fu"})}><Message msgId="naturalfeatures.fungus"/></MenuItem>
                    }
                    {this.props.slimemold_writer &&
                        <MenuItem onClick={() => this.props.onToggleNewNaturalFeature({"featuretype": "slimemold", "featuresubtype": "sl"})}><Message msgId="naturalfeatures.slimemold"/></MenuItem>
                    }
                    {this.props.animal_writer &&
                        <MenuItem onClick={() => this.props.onToggleNewNaturalFeature({"featuretype": "animal", "featuresubtype": "ln"})}><Message msgId="naturalfeatures.land_animal"/></MenuItem>
                    }
                    {this.props.animal_writer &&
                        <MenuItem onClick={() => this.props.onToggleNewNaturalFeature({"featuretype": "animal", "featuresubtype": "lk"})}><Message msgId="naturalfeatures.pond_lake_animal"/></MenuItem>
                    }
                    {this.props.animal_writer &&
                        <MenuItem onClick={() => this.props.onToggleNewNaturalFeature({"featuretype": "animal", "featuresubtype": "st"})}><Message msgId="naturalfeatures.stream_animal"/></MenuItem>
                    }
                    {this.props.animal_writer &&
                        <MenuItem onClick={() => this.props.onToggleNewNaturalFeature({"featuretype": "animal", "featuresubtype": "we"})}><Message msgId="naturalfeatures.wetland_animal"/></MenuItem>
                    }
                    {this.props.naturalarea_writer &&
                        <MenuItem onClick={() => this.props.onToggleNewNaturalFeature({"featuretype": "naturalarea", "featuresubtype": "na"})}><Message msgId="naturalfeatures.naturalarea"/></MenuItem>
                    }
                </DropdownButton>
                { this.props.active ? (<SmartDockedNaturalFeatures/>) : null}
            </div>);
    }
});

module.exports = {
    AddNaturalFeaturesPlugin: assign(connect((state) => ({
        active: state.controls.addnaturalfeatures && state.controls.addnaturalfeatures.enabled,
        disabled: state.naturalfeatures && state.naturalfeatures.mode !== 'VIEW' && state.naturalfeatures.selectedFeature && (state.naturalfeatures.selectedFeature.geom || state.naturalfeatures.selectedFeature.id),
        plant_writer: state.security.user && state.security.user.plant_writer,
        animal_writer: state.security.user && state.security.user.animal_writer,
        slimemold_writer: state.security.user && state.security.user.slimemold_writer,
        fungus_writer: state.security.user && state.security.user.fungus_writer,
        naturalarea_writer: state.security.user && state.security.user.naturalarea_writer
    }), {
        onToggleNewNaturalFeature: addFeature
    })(AddNaturalFeatures), {
        OmniBar: {
            name: "addnf",
            position: 5,
            tool: true,
            priority: 1
        }
    }),
    reducers: {
        naturalfeatures: require('../reducers/naturalfeatures'),
        security: require('../reducers/security')
    }
};
