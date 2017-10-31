/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/
const React = require('react');
const PropTypes = require('prop-types');
const {FormGroup, Checkbox, Col} = require('react-bootstrap');
const {getLabel, getValue} = require('./FieldsUtils');

class BooleanField extends React.Component {
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
    renderVertical = () => {
        const {item, editable, feature} = this.props;
        const readonly = !editable || !!item.readonly;
        return (
            <FormGroup key={item.key} controlId={item.key}>
                <Checkbox
                    name={item.key}
                    checked={getValue(feature, item.key, false)}
                    disabled={readonly}
                    onChange={this.handleChange}>
                    <label className={readonly && "readonly" || ""}>
                        {getLabel(item)}
                    </label>
                </Checkbox>
            </FormGroup>);
    }
    renderHorizontal = () => {
        const {item, editable, feature} = this.props;
        const readonly = !editable || !!item.readonly;
        return (
            <FormGroup key={item.key} controlId={item.key}>
                <Col xs={12}>
                    <Checkbox
                        name={item.key}
                        checked={getValue(feature, item.key, false)}
                        disabled={readonly}
                        onChange={this.handleChange}>
                        <label className={readonly && "readonly" || ""}>
                            {getLabel(item)}
                        </label>
                    </Checkbox>
                </Col>
            </FormGroup>);
    }
    render() {
        return this.props.horizontal && this.renderHorizontal() || this.renderVertical();
    }
    handleChange = (e) => {
        const {onChange, item} = this.props;
        onChange(item.key, e.target.checked);
    }
}

module.exports = BooleanField;
