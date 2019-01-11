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
        isMobile: PropTypes.bool,
        onChange: PropTypes.func,
        hasError: PropTypes.bool
    };
    static defaultProps = {
      editable: false,
      horizontal: false,
      isMobile: false,
      feature: {},
      onChange: () => {},
      hasError: false
    }
    state = {
        full: false
    }
    renderVertical = () => {
        const {item, editable, feature} = this.props;
        const readonly = !editable || !!item.readonly;
        const type = item.type === 'string' && 'textarea' || item.type;
        const comp = (
            <FormGroup controlId={item.key}>
                <ControlLabel className={readonly && "readonly" || ""} style={{color: this.props.hasError && "red" || "auto"}}>{getLabel(item)}</ControlLabel>
                <FormControl
                    onKeyDown={this.handleKeyDown}
                    inputRef={this.addRef}
                    value={getValue(feature, item.key)}
                    readOnly={readonly}
                    rows={3}
                    onChange={this.handleChange}
                    componentClass={item.type === "textarea" && item.type || "input"}
                    onFocus={this.enterFull}
                    type={type}/>
            </FormGroup>);
        return this.state.full ? (<div className="input-full" onClick={this.fullClick}> {comp} <div type="button" className="btn btn-default back-button"><span className="glyphicon glyphicon-backward" aria-hidden="true"/></div></div>) : comp;
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
                    <FormControl
                    onKeyDown={this.handleKeyDown}
                    inputRef={this.addRef}
                    value={getValue(feature, item.key)}
                    readOnly={readonly}
                    rows={3}
                    onChange={this.handleChange}
                    onFocus={this.enterFull}
                    componentClass={item.type === "textarea" && item.type || "input"}
                    type="text"/>
                </Col>
            </FormGroup>);
        return this.state.full ? (<div className="input-full" onClick={this.fullClick}> {comp} <div type="button" className="btn btn-default back-button"><span className="glyphicon glyphicon-backward"/></div></div>) : comp;
    }
    render() {
        return this.props.horizontal && this.renderHorizontal() || this.renderVertical();
    }
    handleChange = (e) => {
        const {onChange, item} = this.props;
        const val = e.target.value === '' ? null : e.target.value;
        onChange(item.key, val);
    }
    handleKeyDown = (e) => {
        const {isMobile} = this.props;
        if (isMobile && (e.keyCode === 13) && this.input) {
            this.exitFull();
        }
    }
    addRef = (ref) => {
        const {isMobile} = this.props;
        if (isMobile) {
            this.input = ref;
            if (this.state.full && this.input) {
                this.input.focus();
            }
        }
    }
    enterFull = () => {
        const {isMobile} = this.props;
        if (isMobile && !this.state.full) {
            this.setState(() => ({full: true}));
        }
        return true;
    }
    exitFull = () => {
        const {isMobile} = this.props;
        if (isMobile) {
            this.input.blur();
            this.setState(() => ({full: false}));
        }
    }
    fullClick = (e) => {
        if (this.state.full && e.target.className && (e.target.className === 'input-full' || e.target.className.indexOf('back-button') !== -1 || e.target.className.indexOf('glyphicon') !== -1)) {
            this.exitFull();
        }
    }
}

module.exports = TextField;
