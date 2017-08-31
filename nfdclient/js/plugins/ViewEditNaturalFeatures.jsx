/*
 * Copyright 2016, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const React = require('react');
const {connect} = require('react-redux');

const {toggleControl} = require('../../MapStore2/web/client/actions/controls');
const {updateNaturalFeature, deleteNaturalFeature, getSpecies, nextVersion, previousVersion} = require('../actions/naturalfeatures');
const {changeDrawingStatus, endDrawing} = require('../../MapStore2/web/client/actions/draw');
const {isWriter, isPublisher} = require('./naturalfeatures/securityutils.js');

const DockedNaturalFeatures = require('../components/naturalfeatures/DockedNaturalFeatures');
const SmartDockedNaturalFeatures = connect((state) => ({
    isVisible: state.controls.vieweditnaturalfeatures && state.controls.vieweditnaturalfeatures.enabled,
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
    onToggle: toggleControl.bind(null, 'vieweditnaturalfeatures', null),
    onUpdate: updateNaturalFeature.bind(null),
    onDelete: deleteNaturalFeature.bind(null),
    getSpecies: getSpecies.bind(null),
    onChangeDrawingStatus: changeDrawingStatus,
    onEndDrawing: endDrawing,
    previousVersion: previousVersion,
    nextVersion: nextVersion
})(DockedNaturalFeatures);

const ViewEditNaturalFeaturesPlugin = React.createClass({
    render() {
        return (
            <div id="docked-tutorial">
                <SmartDockedNaturalFeatures mode="viewedit"/>
            </div>
        );
    }
});

module.exports = {
    ViewEditNaturalFeaturesPlugin,
    reducers: {
        naturalfeatures: require('../reducers/naturalfeatures')
    }
};
