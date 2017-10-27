const PropTypes = require('prop-types');
const React = require('react');
const {Button, Glyphicon} = require('react-bootstrap');
const Spinner = require('react-spinkit');

const Dialog = require('../../MapStore2/web/client/components/misc/Dialog');
const Message = require('../../MapStore2/web/client/components/I18N/Message');
const DownloadOptions = require('./DownloadOptions');
const assign = require('object-assign');

class DownloadDialog extends React.Component {
    static propTypes = {
        closeGlyph: PropTypes.string,
        enabled: PropTypes.bool,
        loading: PropTypes.bool,
        onClose: PropTypes.func,
        onExport: PropTypes.func,
        onDownloadOptionChange: PropTypes.func,
        downloadOptions: PropTypes.object,
        formats: PropTypes.array
    };

    static defaultProps = {
        onExport: () => {},
        onClose: () => {},
        onDownloadOptionChange: () => {},
        downloadOptions: {},
        showSinglePage: false,
        closeGlyph: "1-close",
        formats: [
            {name: "csv", label: "csv"},
            {"name": "xlsx", "label": "excel"},
            {name: "shp", label: "shape-zip"}
        ]
    };

    onClose = () => {
        this.props.onClose();
    };

    renderIcon = () => {
        return this.props.loading ? <div style={{"float": "left", marginRight: 6}}><Spinner spinnerName="circle" noFadeIn overrideSpinnerClassName="spinner"/></div> : <Glyphicon glyph="download" />;
    };

    render() {
        return this.props.enabled ? (<Dialog id="mapstore-export" style={{display: this.props.enabled ? "block" : "none"}} modal={true}>
            <span role="header">
                <span className="about-panel-title"><Message msgId="export.title" /></span>
                <button onClick={this.props.onClose} className="settings-panel-close close">{this.props.closeGlyph ? <Glyphicon glyph={this.props.closeGlyph}/> : <span>×</span>}</button>
                </span>
            <div role="body">
                <DownloadOptions
                    downloadOptions={this.props.downloadOptions}
                    onChange={this.props.onDownloadOptionChange}
                    formats={this.props.formats}/>
                </div>
            <div role="footer">
                <Button
                    bsStyle="primary"
                    className="download-button"
                    disabled={!this.props.downloadOptions.selectedFormat || this.props.loading}
                    onClick={this.handelExport}>
                     {this.renderIcon()} <Message msgId="export.export" />
                </Button>
            </div>
        </Dialog>) : null;
    }
    handelExport = () => {
        const {downloadOptions, onExport} = this.props;
        onExport(assign({}, downloadOptions));
    }
}

module.exports = DownloadDialog;
