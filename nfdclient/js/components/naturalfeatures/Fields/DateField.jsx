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
const DatePicker = require("react-bootstrap-date-picker");
const {getLabel, getValue} = require('./FieldsUtils');

class DateField extends React.Component {
    static propTypes = {
        item: PropTypes.object.isRequired,
        feature: PropTypes.object,
        editable: PropTypes.bool,
        horizontal: PropTypes.bool,
        onChange: PropTypes.func,
        isMobile: PropTypes.bool
    }
    static defaultProps = {
      editable: false,
      horizontal: false,
      feature: {},
      isMobile: false,
      onChange: () => {}
    }
    componentDidMount() {
        const el = document.getElementById(`datepicker.${this.props.item.key}`);
        if (this.props.isMobile && el) {
            el.setAttribute('readonly', true);
        }
    }
    componentDidUpdate() {
        const el = document.getElementById(`datepicker.${this.props.item.key}`);
        if (this.props.isMobile && el) {
            el.setAttribute('readonly', true);
        }
    }
    renderVertical = () => {
        const {item, editable, feature} = this.props;
        const readonly = !editable || !!item.readonly;
        return (
            <FormGroup controlId={`datepicker.${item.key}`}>
                <ControlLabel className={readonly && "readonly" || ""}>{getLabel(item)}</ControlLabel>
                <DatePicker
                    dateFormat="YYYY-MM-DD"
                    disabled={readonly}
                    value={getValue(feature, item.key, null)}
                    onChange={this.handleChange}/>
            </FormGroup>);
    }
    renderHorizontal = () => {
        const {item, editable, feature} = this.props;
        const readonly = !editable || !!item.readonly;
        return (
            <FormGroup controlId={`datepicker.${item.key}`}>
                <Col xs={4} className="label-col">
                    <ControlLabel className={readonly && "readonly" || ""}>{getLabel(item)}</ControlLabel>
                </Col>
                <Col xs={8}>
                    <DatePicker
                        dateFormat="YYYY-MM-DD"
                        disabled={readonly}
                        value={getValue(feature, item.key, null)}
                        onChange={this.handleChange}/>
                </Col>
            </FormGroup>);
    }
    render() {
        return this.props.horizontal && this.renderHorizontal() || this.renderVertical();
    }
    handleChange = (iso, fdate) => {
        const {onChange, item} = this.props;
        onChange(item.key, fdate);
    }
}

module.exports = DateField;
