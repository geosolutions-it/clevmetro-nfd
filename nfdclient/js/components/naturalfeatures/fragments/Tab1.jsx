/**
 * Copyright 2016, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

var React = require('react');
const {FormControl, FormGroup, ControlLabel} = require('react-bootstrap');

require('react-selectize/themes/index.css');

const Tab1 = React.createClass({
    propTypes: {
        field1: React.PropTypes.string,
        field2: React.PropTypes.string,
        field3: React.PropTypes.string
    },
    render() {
        return (
            <form>
                <FormGroup>
                    <ControlLabel>"Field 1"</ControlLabel>
                    <FormControl
                        value={this.props.field1}
                        key="field1"
                        type="text"/>
                </FormGroup>
                <FormGroup>
                    <ControlLabel>"Field 2"</ControlLabel>
                    <FormControl
                        value={this.props.field2}
                        key="field2"
                        type="text"/>
                </FormGroup>
                <FormGroup>
                    <ControlLabel>"Field 3"</ControlLabel>
                    <FormControl
                        value={this.props.field3}
                        key="field3"
                        type="text"/>
                </FormGroup>
            </form>
        );
    }
});

module.exports = Tab1;
