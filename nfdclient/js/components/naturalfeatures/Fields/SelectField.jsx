/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/
const React = require('react');
const PropTypes = require('prop-types');
const {FormGroup, ControlLabel, Col} = require('react-bootstrap');
const {getLabel, getValue} = require('./FieldsUtils');

class SelectField extends React.Component {
    static propTypes = {
        item: PropTypes.object.isRequired,
        feature: PropTypes.object,
        editable: PropTypes.bool,
        horizontal: PropTypes.bool,
        isMobile: PropTypes.bool,
        onChange: PropTypes.func
    }
    static defaultProps = {
      editable: false,
      horizontal: false,
      isMobile: false,
      feature: {},
      onChange: () => {}
    }
    getOptions(values) {
        return values.items.map((item, index) => {
            return (
                <option style={{fontSize: "12px"}} value={item.key} key={index}>{item.value}</option>
            );
        });
    }
    renderVertical = () => {
        const {item, editable, feature} = this.props;
        const readonly = !editable || !!item.readonly;
        return (
            <FormGroup controlId={item.key}>
                <ControlLabel className={readonly && "readonly" || ""}>{getLabel(item)}</ControlLabel>
                <select
                    disabled={readonly}
                    className="form-control"
                    value={getValue(feature, item.key)}
                    onChange={this.handleChange}>
                        <option value="">---</option>
                        {this.getOptions(item.values)}
                </select>
            </FormGroup>);
    }
    renderHorizontal = () => {
        const {item, editable, feature} = this.props;
        const readonly = !editable || !!item.readonly;
        return (
            <FormGroup controlId={item.key}>
                <Col xs={5} className="label-col">
                   <ControlLabel className={readonly && "readonly" || ""}>{getLabel(item)}</ControlLabel>
                </Col>
                <Col xs={7}>
                    <select
                        disabled={readonly}
                        className="form-control"
                        value={getValue(feature, item.key)}
                        onChange={this.handleChange}>
                            <option value="">---</option>
                            {this.getOptions(item.values)}
                    </select>
                </Col>
            </FormGroup>);
    }
    render() {
        return this.props.horizontal && this.renderHorizontal() || this.renderVertical();
    }
    handleChange = (e) => {
        const {onChange, item} = this.props;
        const val = e.target.value === '' ? null : e.target.value;
        onChange(item.key, val);
    }
}

module.exports = SelectField;
