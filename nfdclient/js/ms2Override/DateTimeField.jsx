/**
 * Copyright 2016, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const React = require('react');
const isMobile = require('ismobilejs');
const Moment = require('moment');
const momentLocalizer = require('react-widgets/lib/localizers/moment');
var ReactDOM = require('react-dom');
momentLocalizer(Moment);

const {DateTimePicker} = require('react-widgets');
const {Row, Col} = require('react-bootstrap');

require('react-widgets/lib/less/react-widgets.less');

const DateField = React.createClass({
    propTypes: {
        timeEnabled: React.PropTypes.bool,
        dateFormat: React.PropTypes.string,
        operator: React.PropTypes.string,
        fieldName: React.PropTypes.string,
        fieldRowId: React.PropTypes.number,
        attType: React.PropTypes.string,
        fieldValue: React.PropTypes.object,
        fieldException: React.PropTypes.string,
        onUpdateField: React.PropTypes.func,
        onUpdateExceptionField: React.PropTypes.func
    },
    getDefaultProps() {
        return {
            timeEnabled: false,
            dateFormat: "L",
            operator: null,
            fieldName: null,
            fieldRowId: null,
            attType: null,
            fieldValue: null,
            fieldException: null,
            onUpdateField: () => {},
            onUpdateExceptionField: () => {}
        };
    },
    componentDidMount() {
        if (isMobile.any) {
            this.setInputOnMobile(this.start);
            this.setInputOnMobile(this.end);
            this.setInputOnMobile(this.date);
        }
    },
    componentDidUpdate() {
        if (isMobile.any) {
            this.setInputOnMobile(this.start);
            this.setInputOnMobile(this.end);
            this.setInputOnMobile(this.date);
        }
    },
    componentWillUnmount() {
        this.end = null;
        this.start = null;
        this.date = null;
    },
    startRef(el) {
        if (el) {
            this.start = el;
        }
    },
    endRef(el) {
        if (el) {
            this.end = el;
        }
    },
    dateRef(el) {
        if (el) {
            this.date = el;
        }
    },
    render() {
        let dateRow = this.props.operator === "><" ? (
                <div>
                    <Row>
                        <Col xs={12}>
                        <label>Start Date</label>
                            <DateTimePicker
                                ref={this.startRef}
                                inputProps={{readonly: isMobile.any}}
                                value={this.props.fieldValue ? this.props.fieldValue.startDate : null}
                                time={this.props.timeEnabled}
                                format={this.props.dateFormat}
                                onChange={(date) => this.updateValueState({startDate: date, endDate: this.props.fieldValue ? this.props.fieldValue.endDate : null})}/>
                        </Col>
                    </Row>
                    <Row>
                        <Col xs={12}>
                        <label>End Date</label>
                            <DateTimePicker
                                ref={this.endRef}
                                value={this.props.fieldValue ? this.props.fieldValue.endDate : null}
                                time={this.props.timeEnabled}
                                format={this.props.dateFormat}
                                onChange={(date) => this.updateValueState({startDate: this.props.fieldValue ? this.props.fieldValue.startDate : null, endDate: date})}/>
                        </Col>
                    </Row>
                </div>
            ) : (
                <Row>
                    <Col xs={12}>
                    <label>Date</label>
                        <DateTimePicker
                            ref={this.dateRef}
                            value={this.props.fieldValue ? this.props.fieldValue.startDate : null}
                            time={this.props.timeEnabled}
                            format={this.props.dateFormat}
                            onChange={(date) => this.updateValueState({startDate: date, endDate: null})}/>
                    </Col>
                </Row>
            );

        return (
            dateRow
        );
    },
    updateValueState(value) {
        if (value.startDate && value.endDate && (value.startDate > value.endDate)) {
            this.props.onUpdateExceptionField(this.props.fieldRowId, "queryform.attributefilter.datefield.wrong_date_range");
        } else {
            this.props.onUpdateExceptionField(this.props.fieldRowId, null);
        }

        this.props.onUpdateField(this.props.fieldRowId, this.props.fieldName, value, this.props.attType);
    },
    setInputOnMobile(r) {
        if (isMobile.any && r && r.refs && r.refs.inner && r.refs.inner.refs && r.refs.inner.refs.valueInput) {
            let el = ReactDOM.findDOMNode(r.refs.inner.refs.valueInput);
            if (el) {
                el.setAttribute('readonly', true);
                el = null;
            }
        }
    }
});

module.exports = DateField;
