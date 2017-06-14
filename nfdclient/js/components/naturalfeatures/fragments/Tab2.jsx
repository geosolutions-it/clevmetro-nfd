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

const Tab2 = React.createClass({
    propTypes: {
        field4: React.PropTypes.string,
        field5: React.PropTypes.string
    },
    render() {
        return (
            <form>
                <FormGroup>
                    <ControlLabel>"Field 4"</ControlLabel>
                    <FormControl
                        value={this.props.field4}
                        key="field4"
                        type="text"/>
                </FormGroup>
                <FormGroup>
                    <ControlLabel>"Field 5"</ControlLabel>
                    <FormControl
                        value={this.props.field5}
                        key="field5"
                        type="text"/>
                </FormGroup>
            </form>
        );
    }
});

module.exports = Tab2;
