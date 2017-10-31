/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/
const React = require('react');
const PropTypes = require('prop-types');
const {FormGroup, ControlLabel, FormControl, Col} = require('react-bootstrap');
const {getLabel, getValue} = require('./FieldsUtils');

class TextField extends React.Component {
    static propTypes = {
        item: PropTypes.object.isRequired,
        feature: PropTypes.object,
        editable: PropTypes.bool,
        horizontal: PropTypes.bool,
        onChange: PropTypes.func
    }
    static defaultProps = {
      editable: false,
      horizontal: false,
      feature: {},
      onChange: () => {}
    }
    renderVertical = () => {
        const {item, editable, feature} = this.props;
        const readonly = !editable || !!item.readonly;
        return (
            <FormGroup controlId={item.key}>
                <ControlLabel className={readonly && "readonly" || ""}>{getLabel(item)}</ControlLabel>
                <FormControl
                    value={getValue(feature, item.key)}
                    readOnly={readonly}
                    onChange={this.handleChange}
                    componentClass="input"
                    type="text"/>
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
                    <FormControl
                    value={getValue(feature, item.key)}
                    readOnly={readonly}
                    onChange={this.handleChange}
                    componentClass="input"
                    type="text"/>
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

module.exports = TextField;
