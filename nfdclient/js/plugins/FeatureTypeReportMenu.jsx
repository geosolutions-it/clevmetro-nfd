/*
 * Copyright 2016, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');
const {connect} = require('react-redux');
const assign = require('object-assign');


const {downloadReport} = require('../actions/exportfeatures');

const Message = require('../../MapStore2/web/client/components/I18N/Message');

const {DropdownButton, MenuItem, Glyphicon} = require('react-bootstrap');


const ReportMenu = React.createClass({
    propTypes: {
        onDownloadReport: React.PropTypes.func,
        glyph: React.PropTypes.string,
        buttonStyle: React.PropTypes.string,
        buttonClassName: React.PropTypes.string,
        menuButtonStyle: React.PropTypes.object,
        disabled: React.PropTypes.bool
    },
    getDefaultProps() {
        return {
            onDownloadReport: () => {},
            glyph: "1-pdf",
            buttonStyle: "primary",
            buttonClassName: "square-button",
            disabled: false
        };
    },
    render() {
        return (
            <div>
                <DropdownButton disabled={this.props.disabled} id="pdf-menu-button" className={this.props.buttonClassName} pullRight bsStyle={this.props.buttonStyle} title={<Glyphicon glyph={this.props.glyph} />}>
                        <MenuItem onClick={() => this.props.onDownloadReport("plant")}><Message msgId="naturalfeatures.plants"/></MenuItem>
                        <MenuItem onClick={() => this.props.onDownloadReport("fungus")}><Message msgId="naturalfeatures.fungus"/></MenuItem>
                        <MenuItem onClick={() => this.props.onDownloadReport("animal")}><Message msgId="naturalfeatures.animals"/></MenuItem>
                        <MenuItem onClick={() => this.props.onDownloadReport("slime_mold")}><Message msgId="naturalfeatures.slimemold"/></MenuItem>
                        <MenuItem onClick={() => this.props.onDownloadReport("naturalarea")}><Message msgId="naturalfeatures.naturalarea"/></MenuItem>
                </DropdownButton>
            </div>);
    }
});

module.exports = {
    FeatureTypeReportMenuPlugin: assign(connect(() => ({}), {
        onDownloadReport: downloadReport
    })(ReportMenu), {
        OmniBar: {
            name: "pdfFt",
            position: 6,
            tool: true,
            priority: 1
        }
    }),
    reducers: {
        naturalfeatures: require('../reducers/naturalfeatures'),
        security: require('../reducers/security')
    }
};
