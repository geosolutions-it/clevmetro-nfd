const PropTypes = require('prop-types');
/*
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const React = require('react');
const Select = require('react-select');
require('react-select/dist/react-select.css');
const {Glyphicon} = require('react-bootstrap');
const {get} = require('lodash');
const Message = require('../../MapStore2/web/client/components/I18N/Message');

module.exports = class extends React.Component {
    static propTypes = {
            downloadOptions: PropTypes.object,
            formats: PropTypes.array,
            onChange: PropTypes.func
    };

    static defaultProps = {
        downloadOptions: {},
        formats: []
    }

    getSelectedFormat = () => {
        return get(this.props, "downloadOptions.selectedFormat");
    }
    renderCheckbox = () => {
        const value = !!this.props.downloadOptions.singlePage;
        return (
            <div className="checkbox d-checkbox-invisible">
            <label>
                <Glyphicon onClick={this.onChangeSinglePage} className="event-check" glyph={value ? 'check' : 'unchecked'}/>&nbsp;
                <Message msgId="export.downloadonlycurrentpage" />
            </label>
        </div>);
    }
    render() {
        return (<form>
            <label><Message msgId="export.format" /></label>
            <Select
                clearable={false}
                value={this.getSelectedFormat()}
                onChange={(sel) => this.props.onChange("selectedFormat", sel.value)}
                options={this.props.formats.map(f => ({value: f.name, label: f.label || f.name}))} />
            {this.props.downloadOptions.type === 'LIST' ? this.renderCheckbox() : null }
        </form>);
    }
    onChangeSinglePage = () => {
        this.props.onChange("singlePage", !this.props.downloadOptions.singlePage );
    }
};
