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
const Select = require('react-select');
require('react-select/dist/react-select.css');

/* TODO we have to decide how to pass the value to the backend for multiple values
*
* old version
    handleChange = (e) => {
        const {onChange, item} = this.props;
        const val = e.target.value === '' ? null : e.target.value;
        onChange(item.key, val);
*/


class SelectField extends React.Component {
    static propTypes = {
        item: PropTypes.object.isRequired,
        feature: PropTypes.object,
        editable: PropTypes.bool,
        horizontal: PropTypes.bool,
        isMobile: PropTypes.bool,
        multi: PropTypes.bool,
        onChange: PropTypes.func
    }
    static defaultProps = {
      editable: false,
      horizontal: false,
      isMobile: false,
      multi: false,
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
    getSelect = (item, feature, readonly) => {
        return (<Select
                    searchable={false}
                    multi={this.props.multi}
                    className="nfd-select"
                    labelKey="value"
                    valueKey="key"
                    disabled={readonly}
                    value={getValue(feature, item.key)}
                    onChange={this.handleChange}
                    options={item.values && item.values.items || []}
                />);
    }
    renderVertical = () => {
        const {item, editable, feature} = this.props;
        const readonly = !editable || !!item.readonly;
        return (
            <FormGroup controlId={item.key}>
                <ControlLabel className={readonly && "readonly" || ""}>{getLabel(item)}</ControlLabel>
                {this.getSelect(item, feature, readonly)}
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
                    {this.getSelect(item, feature, readonly)}
                </Col>
            </FormGroup>);
    }
    render() {
        return this.props.horizontal && this.renderHorizontal() || this.renderVertical();
    }
    handleChange = (option) => {
        const {onChange, item, multi} = this.props;
        if (!multi) {
            onChange(item.key, option ? option.key : null);
        }else {
            onChange(item.key, option.length > 0 ? option : null);
        }
    }
}

module.exports = SelectField;
