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
const isMobile = require('ismobilejs');
const Select = require('react-select');

const {getLabel, getValue} = require('./FieldsUtils');

require('react-select/dist/react-select.css');


class SelectField extends React.Component {
    static propTypes = {
        item: PropTypes.object.isRequired,
        feature: PropTypes.object,
        editable: PropTypes.bool,
        horizontal: PropTypes.bool,
        isMobile: PropTypes.bool,
        onChange: PropTypes.func,
        hasError: PropTypes.bool
    }
    static defaultProps = {
      editable: false,
      horizontal: false,
      isMobile: false,
      feature: {},
      onChange: () => {},
      hasError: false
    }
    constructor(props) {
        super(props);
        this.state = {full: false};
    }
    getOptions(item) {
        return item.show_key_with_value && item.values.items.map(({key, value}) => ({key, value: `${key} - ${value}`})) || item.values.items;
    }
    getSelect = (item, feature, readonly) => {
        return (<Select
                    searchable={false}
                    multi={this.isMulti()}
                    className="nfd-select"
                    labelKey="value"
                    valueKey="key"
                    disabled={readonly}
                    value={getValue(feature, item.key)}
                    onChange={this.handleChange}
                    options={item.values && item.values.items && this.getOptions(item) || []}
                    onOpen={this.enterFull}
                    onClose={this.exitFull}
                />);
    }
    renderVertical = () => {
        const {item, editable, feature} = this.props;
        const readonly = !editable || !!item.readonly;
        const comp = (
            <FormGroup controlId={item.key}>
                <ControlLabel className={readonly && "readonly" || ""} style={{color: this.props.hasError && "red" || "auto"}}>{getLabel(item)}</ControlLabel>
                {this.getSelect(item, feature, readonly)}
            </FormGroup>);
        return this.state.full ? (<div className="spec-selector-full" onClick={this.clickExit}> {comp} </div>) : comp;
    }
    renderHorizontal = () => {
        const {item, editable, feature} = this.props;
        const readonly = !editable || !!item.readonly;
        const comp = (
            <FormGroup controlId={item.key}>
                <Col xs={5} className="label-col">
                   <ControlLabel className={readonly && "readonly" || ""} style={{color: this.props.hasError && "red" || "auto"}}>{getLabel(item)}</ControlLabel>
                </Col>
                <Col xs={7}>
                    {this.getSelect(item, feature, readonly)}
                </Col>
            </FormGroup>);
        return this.state.full ? (<div className="spec-selector-full" onClick={this.clickExit}> {comp} </div>) : comp;
    }
    render() {
        return this.props.horizontal && this.renderHorizontal() || this.renderVertical();
    }
    isMulti = () => this.props.item.type === "stringcombo_multiple"
    handleChange = (option) => {
        const {onChange, item} = this.props;
        if (!this.isMulti()) {
            onChange(item.key, option ? option.key : null);
        }else {
            onChange(item.key, option.length > 0 ? option.map(({key}) => key) : null);
        }
    }
    enterFull = () => {
        if (isMobile.any && !this.state.full) {
            this.setState(() => ({full: true}));
        }
    }
    clickExit = (e) => {
        if (e.target.className && e.target.className === 'spec-selector-full') {
            this.exitFull();
        }
    }
    exitFull = () => {
        if (this.state.full) {
            this.setState(() => ({full: false}));
        }
    }
}

module.exports = SelectField;
