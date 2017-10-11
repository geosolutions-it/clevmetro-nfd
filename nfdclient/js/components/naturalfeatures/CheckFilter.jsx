/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/

const React = require('react');
const PropTypes = require('prop-types');
const {Glyphicon} = require('react-bootstrap');

class CheckFilter extends React.Component {
    static propTypes = {
      value: PropTypes.bool,
      onChange: PropTypes.func,
      label: PropTypes.string
    }
    static defaultProps = {
      onChange: () => {}
    }
    render() {
        const {value, label} = this.props;
        return (
            <div className="checkbox d-checkbox-invisible">
                <label>
                    <input type="checkbox" onChange={this.handleChange} checked={value} />
                    <Glyphicon className="event-check" glyph={value ? 'check' : 'unchecked'}/>&nbsp;
                    {label}
                </label>
            </div>
            );
    }
    handleChange = () => {
        this.props.onChange(!this.props.value);
    }
}

module.exports = CheckFilter;
