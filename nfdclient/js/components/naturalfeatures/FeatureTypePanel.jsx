/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/

const React = require('react');
const PropTypes = require('prop-types');

const Utils = require('../../utils/nfdUtils');

const {Accordion, Panel, Glyphicon} = require('react-bootstrap');

const FeaturetypePanel = ({featureType: ft, children, toggleExport, activePanel, onPanelChange}) => {
    const renderPanelHeader = (title) => {
        return (<span><div className="nfd-panel-header">{title}</div></span>);
    };
    const childs = children ? React.Children.toArray(children) : [];
    return (
        <Accordion activeKey={activePanel} onSelect={onPanelChange}>
            <div className="nfd-panel-export" onClick={toggleExport}><Glyphicon glyph="download"/></div>
            <Panel eventKey="features" header={renderPanelHeader(Utils.getPrettyFeatureType(ft))} collapsible>
                {childs[0] ? React.cloneElement(childs[0], {featureType: ft}) : null}
            </Panel>
            <Panel eventKey="filters" header={renderPanelHeader("Filter")} collapsible>
                {childs[1] ? childs[1] : null}
            </Panel>
        </Accordion>);
};
FeaturetypePanel.propTypes = {
  featureType: PropTypes.string.isRequired,
  children: PropTypes.node,
  toggleExport: PropTypes.func,
  onPanelChange: PropTypes.func,
  activePanel: PropTypes.string
};
FeaturetypePanel.defaultProps = {
  toggleExport: () => {},
  activePanel: "features",
  onPanelChange: () => {}
};

module.exports = FeaturetypePanel;
