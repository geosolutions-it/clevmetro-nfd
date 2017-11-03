/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/

const React = require('react');
const PropTypes = require('prop-types');
const assign = require('object-assign');
const {connect} = require('react-redux');

const {Glyphicon, Tabs, Tab, Button} = require('react-bootstrap');
const Dock = require('react-dock');

const {toggleControl} = require('../../MapStore2/web/client/actions/controls');
const {toggleFeatureType} = require('../actions/featuresearch');
const featuresearch = require('../reducers/featuresearch');

const FeatureTypeComponents = require('./featuretypes');
const Spinner = require('react-spinkit');

const Utils = require('../utils/nfdUtils');

class FeaturesSearchPanel extends React.Component {
    static propTypes = {
        height: PropTypes.number,
        width: PropTypes.number,
        dockProps: PropTypes.object,
        active: PropTypes.bool,
        dockSize: PropTypes.number,
        onClose: PropTypes.func,
        toggleFeatureType: PropTypes.func,
        activeFt: PropTypes.string,
        featureTypes: PropTypes.array,
        isLoading: PropTypes.bool
    };
    static contextTypes = {
        messages: PropTypes.object
    };
    static defaultProps = {
        height: 798,
        width: 800,
        eventsLoading: false,
        dockProps: {
            dimMode: "none",
            fluid: true,
            position: "right",
            zIndex: 1030
        },
        dockSize: 0.35,
        onClose: () => {},
        toggleFeatureType: () => {},
        activeFt: 'animal',
        featureTypes: []
    }
    renderLoading() {
        return (<div className="ft-plugin-loading"><Spinner spinnerName="circle" noFadeIn overrideSpinnerClassName="spinner"/></div>);
    }
    renderHeader() {
        return (
            <div className="nfd-header">
            <Glyphicon glyph="1-close" className="no-border btn-default" onClick={() => this.props.onClose()} style={{cursor: "pointer"}}/>
            {this.props.isLoading ? this.renderLoading() : null}
            </div>);
    }
    renderTabs() {
        const {featureTypes, width, height, dockSize} = this.props;
        const tabRows = Math.ceil((featureTypes.length) / Math.floor((width * dockSize) / 58));
        return featureTypes.filter(ft => FeatureTypeComponents[ft]).map((ft, idx) => {
            const FeatureType = FeatureTypeComponents[ft];
            return (
            <Tab key={idx} eventKey={ft} title={<Glyphicon className="icon24" glyph={ft}/>}>
                <FeatureType height={height - 40 - (51 * tabRows)}/>
            </Tab>);
        });
    }
    render() {
        const {activeFt, dockProps, active, dockSize, toggleFeatureType: tfTt} = this.props;
        return active ? (<Dock {...dockProps} isVisible={active} size={dockSize}>
            {this.renderHeader()}
            <div className="lists-container">
                <Tabs id="featuretypes-tab" activeKey={activeFt} onSelect={tfTt}>
                {this.renderTabs()}
                </Tabs>
            </div>
            </Dock>) : null;
    }
}

class ToggleFeaturesPanel extends React.Component {
    static propTypes = {
       onToggle: PropTypes.func,
       active: PropTypes.bool
    };
    static defaultProps = {
        onToggle: () => {},
        active: false
    }
    render() {
        return (
            <Button
                active={this.props.active}
                onClick={this.props.onToggle}
                id="features-button"
                className="square-button"
                bsStyle="primary"
            ><Glyphicon glyph="search"/></Button>);
    }
}
const ToggleFeaturesPanelTool = connect((state) => ({
        active: state.controls && state.controls.features && !!state.controls.features.enabled
    }), {
        onToggle: toggleControl.bind(null, 'features', 'enabled')
    })(ToggleFeaturesPanel);

const FeaturesPlugin = connect((state) => ({
    dockSize: state.naturalfeatures.dockSize,
    active: state.controls && state.controls.features && state.controls.features.enabled,
    height: state.map && state.map.present && state.map.present.size && state.map.present.size.height || 798,
    width: state.map && state.map.present && state.map.present.size && state.map.present.size.width || 0,
    activeFt: state.featuresearch && state.featuresearch.activeFt,
    featureTypes: state.featuresearch && state.featuresearch.featureTypes || [],
    isLoading: state.featuresearch && state.featuresearch.loading ? Utils.isLoading(state.featuresearch.loading) : false
}), {
    onClose: toggleControl.bind(null, 'features'),
    toggleFeatureType
})(FeaturesSearchPanel);

module.exports = {
    FeaturesPlugin: assign(ToggleFeaturesPanelTool, {
        OmniBar: {
            name: 'featurespanel',
            position: 2,
            tool: true,
            tools: [FeaturesPlugin],
            priority: 1
        }
    }),
    epics: require('../epics/featuresearch'),
    reducers: {featuresearch}
};
