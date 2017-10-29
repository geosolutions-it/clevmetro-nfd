/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');
const PropTypes = require('prop-types');
const assign = require('object-assign');
const {Button, Glyphicon} = require('react-bootstrap');
const {connect} = require('react-redux');
const {toggleControl} = require('../../MapStore2/web/client/actions/controls');
class ToggleAddEditPanel extends React.Component {
    static propTypes = {
       onToggle: PropTypes.func,
       mode: PropTypes.string,
       disabled: PropTypes.bool
    };
    static defaultProps = {
        onToggle: () => {},
        disabled: false
    }
    onToggle = () => {
        const {mode, onToggle} = this.props;
        if (mode) {
            const control = mode === 'ADD' ? 'addnaturalfeatures' : 'vieweditnaturalfeatures';
            onToggle(control);
        }
    }
    render() {
        const {disabled} = this.props;
        return (
            <Button
                disabled={disabled}
                onClick={this.onToggle}
                id="add-edit-button"
                className="square-button"
                bsStyle="primary"
            ><Glyphicon glyph="list-alt"/></Button>);
    }
}


const ToggleAddEditPanelPlugin = connect((state) => ({
    mode: state.naturalfeatures && state.naturalfeatures.mode,
    disabled: !(state.naturalfeatures && state.naturalfeatures.selectedFeature && (state.naturalfeatures.selectedFeature.geom || state.naturalfeatures.selectedFeature.id))
}), {
    onToggle: toggleControl
})(ToggleAddEditPanel);


module.exports = {
 ToggleAddEditPanelPlugin: assign(ToggleAddEditPanelPlugin, {
         OmniBar: {
             name: 'toggleeditpanel',
             position: 6,
             tool: true,
             priority: 1
         }
     }),
     reducers: {}
};
