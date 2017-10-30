/*
 * Copyright 2016, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const React = require('react');
const {connect} = require('react-redux');
const PropTypes = require('prop-types');
const {toggleControl} = require('../../MapStore2/web/client/actions/controls');
const {updateNaturalFeature, deleteNaturalFeature, getSpecies, nextVersion, previousVersion, cancel, imageError, addImage, removeImage, onFeaturePropertyChange, editFeature} = require('../actions/naturalfeatures');
const {onToggleExport} = require('../actions/exportfeatures');
const {changeDrawingStatus, endDrawing} = require('../../MapStore2/web/client/actions/draw');
const {isPublisher, isWriter} = require('./naturalfeatures/securityutils');

const DockedNaturalFeatures = require('../components/naturalfeatures/DockedNaturalFeatures');
const SmartDockedNaturalFeatures = connect((state) => ({
    height: state.map && state.map.present && state.map.present.size && state.map.present.size.height || 798,
    width: state.map && state.map.present && state.map.present.size && state.map.present.size.width || 0,
    isVisible: state.controls.vieweditnaturalfeatures && state.controls.vieweditnaturalfeatures.enabled,
    forms: state.naturalfeatures.forms,
    featuretype: state.naturalfeatures.featuretype,
    featuresubtype: state.naturalfeatures.featuresubtype,
    currentFeature: state.naturalfeatures.selectedFeature,
    errors: state.naturalfeatures.errors,
    dockSize: state.naturalfeatures.dockSize,
    mode: state.naturalfeatures.mode,
    images: state.naturalfeatures && state.naturalfeatures.selectedFeature && state.naturalfeatures.selectedFeature.images || [],
    isMobile: state.browser && state.browser.mobile,
    isEditable: isPublisher(state) || isWriter(state),
    isLoading: !!(state.naturalfeatures && state.naturalfeatures.loading)
}), {
    onToggle: toggleControl.bind(null, 'vieweditnaturalfeatures', null),
    onUpdate: updateNaturalFeature.bind(null),
    onDelete: deleteNaturalFeature.bind(null),
    getSpecies: getSpecies.bind(null),
    onChangeDrawingStatus: changeDrawingStatus,
    onEndDrawing: endDrawing,
    previousVersion: previousVersion,
    nextVersion: nextVersion,
    cancel,
    onError: imageError,
    addImage: addImage,
    removeImage: removeImage,
    exportFt: onToggleExport,
    onFeaturePropertyChange,
    editFeature
})(DockedNaturalFeatures);

class ViewEditNaturalFeatures extends React.Component {
    static propTypes = {
      isVisible: PropTypes.bool.isRequired
    }
    static defaultProps = {
      isVisible: false
    }
    render() {
        return this.props.isVisible ? (
            <div id="docked-tutorial">
                <SmartDockedNaturalFeatures mode="viewedit"/>
            </div>
        ) : null;
    }
}
const ViewEditNaturalFeaturesPlugin = connect((state) => ({
    isVisible: state.controls.vieweditnaturalfeatures && !!state.controls.vieweditnaturalfeatures.enabled || false
}))(ViewEditNaturalFeatures);

module.exports = {
    ViewEditNaturalFeaturesPlugin,
    reducers: {
        naturalfeatures: require('../reducers/naturalfeatures')
    }
};
