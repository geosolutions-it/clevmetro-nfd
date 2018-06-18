/*
 * Copyright 2018, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');
const {connect} = require('react-redux');
const Message = require('../../MapStore2/web/client/components/I18N/Message');
const {Grid, ButtonToolbar, Button, Row, Col, FormGroup, Checkbox, ControlLabel} = require('react-bootstrap');
const {isArray, isString} = require('lodash');
const Modal = require('../../MapStore2/web/client/components/misc/Modal');
const {initializeReportFilters, updateReportOptions, downloadReportWithFilter} = require('../actions/exportfeatures');
const defaultFilters = require('./reportconfiguration/defaultFilters');
const FilterForm = require('./reportconfiguration/FilterForm');
const Spinner = require('react-spinkit');

const ReportConfiguration = React.createClass({
    propTypes: {
        defaultFilters: React.PropTypes.object,
        onChange: React.PropTypes.func,
        onInit: React.PropTypes.func,
        filters: React.PropTypes.object,
        reportOptions: React.PropTypes.object,
        onDownload: React.PropTypes.func,
        downloading: React.PropTypes.bool
    },
    getDefaultProps() {
        return {
            defaultFilters,
            onChange: () => {},
            onInit: () => {},
            onDownload: () => {}
        };
    },
    componentWillMount() {
        this.props.onInit(this.props.defaultFilters);
    },
    render() {
        return (
            <Modal
                show={this.props.reportOptions}
                className="nf-report-configuration-modal">
                <Modal.Header
                    closeButton
                    onHide={() => this.props.onChange({ downloaded: true })}>
                    <div style={{fontSize: 18}}>
                        <Message msgId="clevmetro.reportDownloadConfiguration"/>
                    </div>
                </Modal.Header>
                <Modal.Body>
                    <Grid fluid>
                        <Row>
                            <Col xs={12}>
                                <div className="form-title" style={{marginTop: 10}}><Message msgId="clevmetro.reportFilters"/></div>
                            </Col>
                            {this.props.filters && this.props.filters.row && this.props.filters.row
                            .filter(filter => !filter.error && (!filter.only || this.props.reportOptions && filter.only && filter.only === this.props.reportOptions.downloadReportUrl))
                            .map(filter =>
                                <Col xs={12}>
                                    {isString(filter.code) ? <ControlLabel>
                                        <Message msgId={'clevmetro.' + filter.code} />
                                    </ControlLabel> : <ControlLabel>
                                        <Message msgId={'clevmetro.' + filter.id} />
                                    </ControlLabel>}
                                    {isArray(filter.type) ? filter.type.map((type, idx) => (
                                        <FilterForm
                                            desc={filter.code && filter.code[idx]}
                                            code={filter.code && filter.code[idx]}
                                            type={type}
                                            disabled={this.props.downloading}
                                            loading={filter.loading}
                                            options={filter.options}
                                            onChange={this.props.onChange}
                                            reportOptions={this.props.reportOptions || {}}/>
                                    ))
                                    :
                                    <FilterForm
                                        name={filter.name}
                                        code={filter.code}
                                        type={filter.type}
                                        disabled={this.props.downloading}
                                        loading={filter.loading}
                                        options={filter.options}
                                        onChange={this.props.onChange}
                                        reportOptions={this.props.reportOptions || {}}/>}
                                </Col>
                            )}
                        </Row>
                        <Row>
                            <Col xs={12}>
                                <div className="form-title" style={{marginTop: 10}}><Message msgId="clevmetro.reportColumns"/></div>
                            </Col>
                            <FormGroup>
                                    {this.props.filters && this.props.filters.col && this.props.filters.col.map(field => (
                                        <Col xs={12}>
                                            {field.options && field.options.map(option => (
                                                <Checkbox
                                                    disabled={this.props.downloading}
                                                    checked={!this.props.reportOptions
                                                        || this.props.reportOptions && this.props.reportOptions[option.code] === undefined
                                                        || this.props.reportOptions && this.props.reportOptions[option.code]}
                                                    onClick={() => this.props.onChange({
                                                        [option.code]: !(!this.props.reportOptions
                                                        || this.props.reportOptions && this.props.reportOptions[option.code] === undefined
                                                        || this.props.reportOptions && this.props.reportOptions[option.code])
                                                    })}>
                                                    {option.name}
                                                </Checkbox>
                                            ))}
                                        </Col>
                                    ))}
                            </FormGroup>
                        </Row>
                    </Grid>
                </Modal.Body>
                <Modal.Footer>
                    <ButtonToolbar
                        className="pull-right">
                        <Button
                            bsStyle="primary"
                            disabled={this.props.downloading}
                            onClick={() => this.props.onChange({ downloaded: true })}>
                            <Message msgId="close"/>
                        </Button>
                        {this.props.reportOptions && this.props.reportOptions.featureType && <Button
                            bsStyle="primary"
                            disabled={this.props.downloading}
                            onClick={() => this.props.onDownload(this.props.reportOptions.featureType)}>
                            <Message msgId="download"/>
                            {this.props.downloading && <Spinner spinnerName="circle" noFadeIn overrideSpinnerClassName="spinner"/>}
                        </Button>}
                    </ButtonToolbar>
                </Modal.Footer>
            </Modal>
        );
    }
});

const ReportConfigurationPlugin = connect((state = {}) => ({
    filters: state.exportfeatures && state.exportfeatures && state.exportfeatures.reportFilters || {},
    reportOptions: state.exportfeatures && state.exportfeatures && state.exportfeatures.reportOptions,
    downloading: state.exportfeatures && state.exportfeatures.downloading
}), {
    onInit: initializeReportFilters,
    onChange: updateReportOptions,
    onDownload: downloadReportWithFilter
})(ReportConfiguration);

module.exports = {
    ReportConfigurationPlugin,
    reducers: {
        naturalfeatures: require('../reducers/naturalfeatures')
    }
};
