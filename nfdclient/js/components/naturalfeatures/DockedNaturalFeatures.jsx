/**
 * Copyright 2015, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const React = require('react');
const Dock = require('react-dock');
const Spinner = require('react-spinkit');
const {Glyphicon, Tabs, Tab, FormControl, ControlLabel, Table, Button, Checkbox} = require('react-bootstrap');
const DatePicker = require("react-bootstrap-date-picker");
const {asyncContainer, Typeahead} = require("react-bootstrap-typeahead");
const AsyncTypeahead = asyncContainer(Typeahead);

const ConfirmDialog = require('../../../MapStore2/web/client/components/misc/ConfirmDialog');
const Message = require('../../../MapStore2/web/client/components/I18N/Message');
const ToggleButton = require('../../../MapStore2/web/client/components/buttons/ToggleButton');
const {isEmpty} = require('lodash');
const NfdImage = require('./NfdImage');
require('react-selectize/themes/index.css');
require('./DockedNaturalFeatures.css');
const Utils = require("../../utils/nfdUtils");
const Api = require('../../api/naturalfeaturesdata');

const DockedNaturalFeatures = React.createClass({
    propTypes: {
        isLoading: React.PropTypes.bool,
        isMobile: React.PropTypes.bool,
        height: React.PropTypes.number,
        width: React.PropTypes.number,
        forms: React.PropTypes.array,
        featuretype: React.PropTypes.string,
        featuresubtype: React.PropTypes.string,
        currentFeature: React.PropTypes.object,
        errors: React.PropTypes.object,
        isVisible: React.PropTypes.bool,
        onToggle: React.PropTypes.func,
        onSave: React.PropTypes.func,
        onUpdate: React.PropTypes.func,
        onDelete: React.PropTypes.func,
        dockSize: React.PropTypes.number,
        previousVersion: React.PropTypes.func,
        nextVersion: React.PropTypes.func,
        mode: React.PropTypes.string,
        addPointGlyph: React.PropTypes.string,
        addPointEnabled: React.PropTypes.bool,
        addPolygonGlyph: React.PropTypes.string,
        addPolygonEnabled: React.PropTypes.bool,
        getMyLocationEnabled: React.PropTypes.bool,
        onChangeDrawingStatus: React.PropTypes.func,
        getSpecies: React.PropTypes.func,
        cancel: React.PropTypes.func,
        selectedSpecie: React.PropTypes.number,
        images: React.PropTypes.array,
        onError: React.PropTypes.func,
        addImage: React.PropTypes.func,
        removeImage: React.PropTypes.func,
        dockProps: React.PropTypes.object,
        exportFt: React.PropTypes.func,
        onFeaturePropertyChange: React.PropTypes.func,
        editFeature: React.PropTypes.func,
        isEditable: React.PropTypes.bool
    },
    getDefaultProps() {
        return {
            forms: [],
            currentFeature: {},
            errors: {},
            dockProps: {
                dimMode: "none",
                fluid: true,
                position: "right",
                zIndex: 1030
            },
            isVisible: false,
            dockSize: 0.35,
            addPointGlyph: "1-point-add",
            addPolygonGlyph: "1-polygon-add",
            isEditable: false,
            setDockSize: () => {},
            onToggle: () => {},
            onSave: () => {},
            onUpdate: () => {},
            onDelete: () => {},
            getSpecies: () => {},
            previousVersion: () => {},
            nextVersion: () => {},
            onChangeDrawingStatus: () => {},
            cancel: () => {},
            exportFt: () => {},
            onFeaturePropertyChange: () => {},
            editFeature: () => {}
        };
    },
    getInitialState() {
        return {showConfirm: false};
    },
    onClose: function() {
        this.props.onToggle();
    },
    onAddPointClick: function() {
        this.props.onChangeDrawingStatus("start", "MarkerReplace", "dockednaturalfeatures", [], {properties: this.props.currentFeature, icon: Utils.getIcon(this.props.featuretype)});
    },
    onAddPolygonClick: function() {
        this.props.onChangeDrawingStatus("start", "Polygon", "dockednaturalfeatures", [], {properties: this.props.currentFeature});
    },
    getOptions(values) {
        return values.items.map((item, index) => {
            return (
                <option style={{fontSize: "12px"}} value={item.key} key={index}>{item.value}</option>
            );
        });
    },
    getLabel(item) {
        return `${item.mandatory ? '* ' : ''}${item.label}`;
    },
    getValue(key, defaultValue = '') {
        return !isEmpty(this.props.currentFeature) && this.props.currentFeature[key] || defaultValue;
    },
    renderTabContent(tab, tabindex, tabContentHeigth) {
        const isEditable = this.props.mode !== 'VIEW';
        let searchDiv;
        let tabName = tab.formlabel;
        let items = tab.formitems.map((item) => {
            if (item.type === 'string') {
                return (
                    <tr style={{width: "100%"}} key={item.key + "-row"}>
                        <td style={{width: "40%"}}>
                            <ControlLabel>{this.getLabel(item)}</ControlLabel>
                        </td>
                        <td style={{width: "60%"}}>
                            <FormControl
                                style={{width: "100%", height: "24px", fontSize: "12px"}}
                                value={this.getValue(item.key)}
                                readOnly={!isEditable || !!item.readonly}
                                onChange={this.handleChange}
                                key={item.key}
                                name={item.key}
                                componentClass="input"
                                type="text"/>
                        </td>
                    </tr>
                );
            } else if (item.type === 'stringcombo') {
                return (
                    <tr style={{width: "100%"}} key={item.key + "-row"}>
                        <td style={{width: "40%"}}>
                            <ControlLabel>{this.getLabel(item)}</ControlLabel>
                        </td>
                        <td style={{width: "60%"}}>
                            <select disabled={!isEditable || !!item.readonly} style={{height: "24px", fontSize: "12px"}} name={item.key} className="form-control" value={this.getValue(item.key)} onChange={this.handleChange}>
                                    <option value="">---</option>
                                    {this.getOptions(item.values)}
                            </select>
                        </td>
                    </tr>
                );
            } else if (item.type === 'integer') {
                return (
                    <tr style={{width: "100%"}} key={item.key + "-row"}>
                        <td style={{width: "40%"}}>
                            <ControlLabel>{this.getLabel(item)}</ControlLabel>
                        </td>
                        <td style={{width: "60%"}}>
                            <FormControl
                                style={{width: "100%", height: "24px", fontSize: "12px"}}
                                value={this.getValue(item.key)}
                                readOnly={!isEditable || !!item.readonly}
                                onChange={this.handleChange}
                                key={item.key}
                                name={item.key}
                                componentClass="input"
                                min="0"
                                step="1"
                                type="number"/>
                        </td>
                    </tr>
                );
            } else if (item.type === 'double') {
                return (
                    <tr style={{width: "100%"}} key={item.key + "-row"}>
                        <td style={{width: "40%"}}>
                            <ControlLabel>{this.getLabel(item)}</ControlLabel>
                        </td>
                        <td style={{width: "60%"}}>
                            <FormControl
                                style={{width: "100%", height: "24px", fontSize: "12px"}}
                                value={this.getValue(item.key)}
                                readOnly={!isEditable || !!item.readonly}
                                onChange={this.handleChange}
                                key={item.key}
                                name={item.key}
                                componentClass="input"
                                min="0"
                                step="any"
                                type="number"/>
                        </td>
                    </tr>
                );
            } else if (item.type === 'boolean') {
                return (
                    <tr style={{width: "100%"}} key={item.key + "-row"}>
                        <td style={{width: "40%"}}>
                            <ControlLabel>{this.getLabel(item)}</ControlLabel>
                        </td>
                        <td style={{width: "60%"}}>
                            <Checkbox name={item.key} checked={this.getValue(item.key, false)} disabled={!isEditable || !!item.readonly} onChange={this.handleBooleanChange}/>
                        </td>
                    </tr>
                    );
            } else if (item.type === 'date') {
                return (
                    <tr style={{width: "100%"}} key={item.key + "-row"}>
                        <td style={{width: "40%"}}>
                            <ControlLabel>{this.getLabel(item)}</ControlLabel>
                        </td>
                        <td style={{width: "60%"}}>
                            <DatePicker dateFormat="YYYY-MM-DD" disabled={!isEditable || !!item.readonly} style={{height: "24px"}} value={this.getValue(item.key, null)} onChange={(iso, fdate) => this.handleDateChange(item.key, fdate)}/>
                        </td>
                    </tr>
                    );
            }
        });

        searchDiv = tabindex <= 2 && this.props.mode !== 'VIEW' && this.props.featuresubtype !== 'na';
        return (
            <div className="nf-tab-content" style={{height: tabContentHeigth, overflow: "auto"}}>
                {searchDiv ?
                    (<AsyncTypeahead
                        {...this.state}
                        labelKey="name"
                        bsSize="small"
                        maxResults={20}
                        onSearch={this._handleSearch}
                        placeholder="Search for a specie..."
                        renderMenuItemChildren={this._renderMenuItemChildren}
                        selected={this.props.selectedSpecie}
                        onChange={this._handleSpeciesChange}
                    />)
                    :
                    (<div></div>)
                }
                <Table style={{width: "100%", marginTop: "10px"}} responsive striped condensed bordered>
                    <caption style={{display: "table-caption", textAlign: "center", backgroundColor: "#ccc", color: "#ffffff"}}>{tabName}</caption>
                    <tbody style={{width: "100%"}}>{items}</tbody>
                </Table>
                {(tab.formname === 'location') ? this.renderDrawTools() : null}
            </div>
        );
    },
    renderTabs(tabContentHeigth) {
        let tabs = [];
        this.props.forms.map((tab, index) => {
            let i = index + 1;
            let key = "tab-" + i;
            let tabIcon = Utils.getFormIcon(tab.formname);
            tabs.push(
                <Tab eventKey={i} key={key} title={<Glyphicon glyph={tabIcon} style={{cursor: "pointer", fontSize: "24px"}}/>}>
                    {this.renderTabContent(tab, i, tabContentHeigth)}
                </Tab>
            );
        });
        if (tabs.length > 0) {
            tabs.push(
                <Tab eventKey={(tabs.length + 1)} key="resources" title={<Glyphicon glyph="camera" style={{cursor: "pointer", fontSize: "24px"}}/>}>
                    <div className="nf-tab-content" style={{height: tabContentHeigth, overflow: "hidden"}}>
                        <NfdImage height={tabContentHeigth}
                            isMobile={this.props.isMobile}
                            disabled={this.props.mode === 'VIEW'}
                            onError={this.props.onError}
                            addImage={this.props.addImage}
                            removeImage={this.props.removeImage}
                            images={this.props.images}/>
                    </div>
                </Tab>
            );
        }
        return tabs;
    },
    renderButtons() {
        let buttons = [<Button key="cancel" bsSize="small"
                    bsStyle="primary"
                    onClick={this.props.cancel}
                    disabled={false}
                    style={{marginRight: "2px"}}>
                    <Message msgId="cancel" />
                </Button>];
        if (this.props.mode === 'EDIT') {
            return buttons.concat([<Button key="delete" bsSize="small"
                bsStyle="primary"
                onClick={() => {this.setState({showConfirm: true}); }}
                style={{marginRight: "2px"}}
                disabled={false}>
                    <Message msgId="naturalfeatures.delete" />
                </Button>,
                <Button key="update" bsSize="small"
                    bsStyle="primary"
                    onClick={() => this.props.onUpdate(this.props.featuretype, this.props.featuresubtype, this.props.currentFeature)}
                    disabled={false}
                    style={{marginRight: "2px"}}>
                    <Message msgId="naturalfeatures.update" />
                </Button>]);
        }else if (this.props.mode === 'ADD') {
            return buttons.concat([<Button key="save" bsSize="small"
                    bsStyle="primary"
                    onClick={() => this.props.onUpdate(this.props.featuretype, this.props.featuresubtype, this.props.currentFeature)}
                    disabled={false}>
                    <Message msgId="naturalfeatures.save" />
                </Button>]);
        }
        return buttons.concat([<Button key="edit" bsSize="small"
                    bsStyle="primary"
                    disabled={!this.props.isEditable}
                    onClick={this.handleEdit}
                    style={{marginRight: "2px"}}>
                        <Message msgId="naturalfeatures.edit" />
                    </Button>, <Button key="exportFt" bsSize="small"
                    bsStyle="primary"
                    onClick={this.exportFt}
                    >
                    <Glyphicon glyph="download" style={{fontSize: 18}}/>
                </Button>]);
    },
    renderHistoric() {
        return (
            <div className="nf-historic">
                <Button key="previous" bsSize="small"
                    bsStyle="primary"
                    type="button"
                    onClick={() => {this.props.previousVersion(this.props.featuretype, this.props.currentFeature.id, this.props.currentFeature.version); document.activeElement.blur(); } }
                    disabled={ (this.props.currentFeature.version <= 1) }>
                    <Glyphicon glyph={"menu-left"}/>
                </Button>
                <span className="nf-historic-date">Version {this.props.currentFeature.version} / {this.props.currentFeature.total_versions}</span>
                <Button key="next" bsSize="small"
                    bsStyle="primary"
                    onClick={() => {this.props.nextVersion(this.props.featuretype, this.props.currentFeature.id, this.props.currentFeature.version); document.activeElement.blur(); } }
                    disabled={ (this.props.currentFeature.version >= this.props.currentFeature.total_versions) }>
                    <Glyphicon glyph={"menu-right"}/>
                </Button>
            </div>
        );
    },
    renderDrawTools() {
        return (
          <div id="nfdraw-tools" className="nfdraw-tools">
              <span className="nfdraw-tools-title"><Message msgId="naturalfeatures.draw_loc" /></span>
              <div className="nfdraw-tools-buttons">
                  <ToggleButton
                      glyphicon={this.props.addPointGlyph}
                      style={{marginRight: "10px", padding: "9px"}}
                      pressed={this.props.addPointEnabled}
                      onClick={this.onAddPointClick} />
                  <ToggleButton
                      glyphicon={this.props.addPolygonGlyph}
                      style={{marginRight: "10px", padding: "9px"}}
                      pressed={this.props.addPolygonEnabled}
                      onClick={this.onAddPolygonClick} />
              </div>
          </div>
        );
    },
    renderErrors() {
        let errorItems = [];
        for (let key in this.props.errors) {
            if (key) {
                let e = key + ': ' + this.props.errors[key][0];
                errorItems.push(<li>{e}</li>);
            }
        }
        return (<ul>{errorItems}</ul>);
    },
    renderLoading() {
        return (<div className="ft-plugin-loading"><Spinner spinnerName="circle" noFadeIn overrideSpinnerClassName="spinner"/></div>);
    },
    renderHeader() {
        const subTitle = Utils.getPrettyFeatureSubType(this.props.featuresubtype);
        const title = this.props.featuretype && `${Utils.getPrettyFeatureType(this.props.featuretype)}${subTitle.length > 0 ? `(${subTitle})` : ''}`;
        return (
            <div className="nfd-header">
            <Glyphicon glyph="1-close" className="no-border btn-default" onClick={this.onClose} style={{cursor: "pointer"}}/>
            <div className="nfd-form-title">{title}</div>
            {this.props.isLoading ? this.renderLoading() : null}
            </div>);
    },
    render() {
        const {forms = [], width, height, dockSize, mode, dockProps, isVisible} = this.props;
        const tabRows = Math.ceil((forms.length + 1) / Math.floor((width * dockSize) / 58));
        const footerHeight = (mode === 'EDIT') ? 70 : 41;
        const tabContentHeigth = height - 40 - footerHeight - (45 * tabRows) + 1;
        return (
            <Dock {...dockProps} size={dockSize}
                isVisible={isVisible}>
                {this.renderHeader()}
                <Tabs defaultActiveKey={1} id="naturalfeature-tabs" ref={(tabs) => { this.tabs = tabs; }}>
                        {this.renderTabs(tabContentHeigth)}
                </Tabs>
                <div className="dock-panel-footer" style={{height: footerHeight}}>
                    {(mode === 'EDIT') ? this.renderHistoric() : null}
                    <div className="dock-panel-footer-buttons">
                    {this.renderButtons()}
                    </div>
                </div>
                {this.state.showConfirm ? this._renderConfirm() : null}
            </Dock>
        );
    },
    _renderMenuItemChildren(option) {
        return (
            <div key={option.id}>
                <span>{option.name}</span>
            </div>
        );
    },
    _handleSpeciesChange(e) {
        if (e.length === 1) {
            this.props.getSpecies(e[0].id);
        }
    },
    _handleSearch(query) {
        if (!query) {
            return;
        }
        Api.searchSpecies(query)
            .then(json => this.setState({options: json}));
    },
    handleVisibility(index, label) {
        if (this.props.mode === 'ADD') {
            if (label.target.className === "glyphicon glyphicon-camera") {
                document.getElementById("nfdraw-tools").style.display = "none";
            } else {
                document.getElementById("nfdraw-tools").style.display = "block";
            }
        }
    },
    handleChange(e) {
        if (e.target.value === '') {
            this.props.onFeaturePropertyChange(e.target.name, null);
            // this.props.currentFeature[e.target.name] = null;
        } else {
            this.props.onFeaturePropertyChange(e.target.name, e.target.value);
            // this.props.currentFeature[e.target.name] = e.target.value;
        }
    },
    exportFt() {
        this.props.exportFt('SINGLE', this.props.currentFeature.featuretype, this.props.currentFeature.id);
    },
    handleDelete() {
        this.props.onDelete(this.props.featuretype, this.props.currentFeature.id);
    },
    _renderConfirm() {
        return (<ConfirmDialog onConfirm={this.handleDelete} onClose={()=> {this.setState({showConfirm: false}); }} show={true} title={<Message msgId="naturalfeatures.deleteTitle" />} >
                    <Message msgId="naturalfeatures.deleteMsg"/>
                </ConfirmDialog>);
    },
    handleEdit() {
        return this.props.editFeature(this.props.currentFeature);
    },
    handleBooleanChange(e) {
        this.props.onFeaturePropertyChange(e.target.name, e.target.checked);
    },
    handleDateChange(key, formattedDate) {
        this.props.onFeaturePropertyChange(key, formattedDate);
    }

});

module.exports = DockedNaturalFeatures;
