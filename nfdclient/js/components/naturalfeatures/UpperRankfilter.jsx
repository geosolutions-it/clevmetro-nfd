/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/
const React = require('react');
const PropTypes = require('prop-types');
const isMobile = require('ismobilejs');
const {FormControl} = require('react-bootstrap');


class TextField extends React.Component {
    static propTypes = {
        value: React.PropTypes.string,
        placeholder: PropTypes.string,
        horizontal: PropTypes.bool,
        onChange: PropTypes.func
    };
    static defaultProps = {
      horizontal: false,
      feature: {},
      onChange: () => {}
    }
    state = {
        full: false
    }
    render = () => {
        return (<div className={this.state.full ? 'input-full' : ''} onClick={this.fullClick} >
                    <FormControl
                    onKeyDown={this.handleKeyDown}
                    inputRef={this.addRef}
                    value={this.props.value}
                    onChange={this.handleChange}
                    onFocus={this.enterFull}
                    componentClass="input"
                    placeholder="Search any ranks..."
                    type="text"/>
            </div>);

    }
    handleChange = (e) => {
        const {onChange} = this.props;
        const val = e.target.value === '' ? null : e.target.value;
        onChange(val);
    }
    handleKeyDown = (e) => {
        if (isMobile.any && (e.keyCode === 13) && this.input) {
            this.exitFull();
        }
    }
    addRef = (ref) => {
        if (isMobile.any) {
            this.input = ref;
            if (this.state.full && this.input) {
                this.input.focus();
            }
        }
    }
    enterFull = () => {
        if (isMobile.any && !this.state.full) {
            this.setState(() => ({full: true}));
        }
        return true;
    }
    exitFull = () => {
        if (isMobile.any) {
            this.input.blur();
            this.setState(() => ({full: false}));
        }
    }
    fullClick = (e) => {
        if (this.state.full && e.target.className && e.target.className === 'input-full') {
            this.exitFull();
        }
    }
}

module.exports = TextField;
