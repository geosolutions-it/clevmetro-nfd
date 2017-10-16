/**
 * Copyright 2015, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const React = require('react');
const Dock = require('react-dock');
const {Glyphicon, Tabs, Tab, FormControl, ControlLabel, Table, Button, Checkbox} = require('react-bootstrap');
const DatePicker = require("react-bootstrap-date-picker");
const {asyncContainer, Typeahead} = require("react-bootstrap-typeahead");
const AsyncTypeahead = asyncContainer(Typeahead);
const Message = require('../../../MapStore2/web/client/components/I18N/Message');
const ToggleButton = require('../../../MapStore2/web/client/components/buttons/ToggleButton');
const _ = require('lodash');
// const isMobile = require('ismobilejs');
require('react-selectize/themes/index.css');
require('./DockedNaturalFeatures.css');
const Utils = require("../../utils/nfdUtils");
const Api = require('../../api/naturalfeaturesdata');

const DockedNaturalFeatures = React.createClass({
    propTypes: {
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
        initWidth: React.PropTypes.oneOfType([ React.PropTypes.number, React.PropTypes.string ]),
        dockSize: React.PropTypes.number,
        minDockSize: React.PropTypes.number,
        maxDockSize: React.PropTypes.number,
        setDockSize: React.PropTypes.func,
        previousVersion: React.PropTypes.func,
        nextVersion: React.PropTypes.func,
        mode: React.PropTypes.string,
        isAdmin: React.PropTypes.bool,
        isWriter: React.PropTypes.bool,
        isPublisher: React.PropTypes.bool,
        addPointGlyph: React.PropTypes.string,
        addPointEnabled: React.PropTypes.bool,
        addPolygonGlyph: React.PropTypes.string,
        addPolygonEnabled: React.PropTypes.bool,
        getMyLocationEnabled: React.PropTypes.bool,
        onChangeDrawingStatus: React.PropTypes.func,
        onEndDrawing: React.PropTypes.func,
        photos: React.PropTypes.array,
        getSpecies: React.PropTypes.func,
        cancel: React.PropTypes.func,
        selectedSpecie: React.PropTypes.number
    },
    getDefaultProps() {
        return {
            forms: [],
            photos: [],
            currentFeature: {},
            errors: {},
            isVisible: false,
            initWidth: 600,
            dockSize: 0.35,
            minDockSize: 0.1,
            maxDockSize: 1.0,
            addPointGlyph: "1-point-add",
            addPolygonGlyph: "1-polygon-add",
            setDockSize: () => {},
            onToggle: () => {},
            onSave: () => {},
            onUpdate: () => {},
            onDelete: () => {},
            getSpecies: () => {},
            previousVersion: () => {},
            nextVersion: () => {},
            onChangeDrawingStatus: () => {},
            onEndDrawing: () => {},
            cancel: () => {}
        };
    },
    componentWillMount: function() {
        // this.props.onChangeDrawingStatus("clean", null, "dockednaturalfeatures", [], {});
    },
    onClose: function() {
        this.props.onToggle();
        // this.props.onChangeDrawingStatus("clean", null, "dockednaturalfeatures", [], {});
    },
    onAddPointClick: function() {
        this.props.onChangeDrawingStatus("start", "MarkerReplace", "dockednaturalfeatures", [], {properties: this.props.currentFeature, icon: Utils.getIconUrl(this.props.featuretype)});
    },
    onAddPolygonClick: function() {
        this.props.onChangeDrawingStatus("start", "Polygon", "dockednaturalfeatures", [], {properties: this.props.currentFeature});
    },
    onGetMyLocationClick: function() {
        this.props.onChangeDrawingStatus("start", "Polygon", "dockednaturalfeatures", [], {});
    },
    getIcon(formname) {
        let icon = 'question-sign';
        if (formname === 'species') {
            icon = 'question-sign';
        } else if (formname === 'species.element_species') {
            icon = 'star';
        } else if (formname === 'details') {
            icon = 'th-list';
        } else if (formname === 'details.lifestages') {
            icon = 'refresh';
        } else if (formname === 'occurrencemanagement') {
            icon = 'cog';
        } else if (formname === 'observation') {
            icon = 'eye-open';
        } else if (formname === 'observation.reporter') {
            icon = 'reporter';
        } else if (formname === 'observation.recorder') {
            icon = 'recorder';
        } else if (formname === 'observation.verifier') {
            icon = 'verifier';
        } else if (formname === 'voucher') {
            icon = 'tag';
        } else if (formname === 'location') {
            icon = 'uniE062';
        } else if (formname === 'details.vegetation') {
            icon = 'uniE103';
        } else if (formname === 'details.substrate') {
            icon = 'uniE135';
        } else if (formname.includes('earthworm')) {
            icon = 'uniE232';
        } else if (formname.includes('disturbance')) {
            icon = 'uniE162';
        } else if (formname.includes('association')) {
            icon = 'uni4C';
        } else if (formname.includes('fruit')) {
            icon = 'uniF8FF';
        }
        
        return icon;
    },
    getOptions(values) {
        return values.items.map((item, index) => {
            return (
                <option style={{fontSize: "12px"}} value={item.key} key={index}>{item.value}</option>
            );
        });
    },
    renderTabContent(tab, tabindex) {
        let searchDiv;
        let tabName = tab.formlabel;
        let items = tab.formitems.map((item) => {
            if (item.type === 'string') {
                let value = "";
                let label = item.label;
                if (item.mandatory) {
                    label = '* ' + item.label;
                }
                let readOnly = false;
                if (item.readonly) {
                    readOnly = true;
                }
                if (!_.isEmpty(this.props.currentFeature) && this.props.currentFeature[item.key]) {
                    value = this.props.currentFeature[item.key];
                }
                return (
                    <tr style={{width: "100%"}} key={item.key + "-row"}>
                        <td style={{width: "40%"}}>
                            <ControlLabel>{label}</ControlLabel>
                        </td>
                        <td style={{width: "60%"}}>
                            <FormControl
                                style={{width: "100%", height: "24px", fontSize: "12px"}}
                                value={value}
                                readOnly={readOnly}
                                onChange={this.handleChange}
                                key={item.key}
                                name={item.key}
                                componentClass="input"
                                type="text"/>
                        </td>
                    </tr>
                );
            } else if (item.type === 'stringcombo') {
                let value = "";
                let label = item.label;
                if (item.mandatory) {
                    label = '* ' + item.label;
                }
                if (!_.isEmpty(this.props.currentFeature) && this.props.currentFeature[item.key]) {
                    value = this.props.currentFeature[item.key];
                }
                return (
                    <tr style={{width: "100%"}} key={item.key + "-row"}>
                        <td style={{width: "40%"}}>
                            <ControlLabel>{label}</ControlLabel>
                        </td>
                        <td style={{width: "60%"}}>
                            {item.readonly ?
                                (<select disabled style={{height: "24px", fontSize: "12px"}} name={item.key} className="form-control" bsSize="small" value={value || ""}>
                                    <option value="">---</option>
                                    {this.getOptions(item.values)}
                                </select>)
                                :
                                (<select style={{height: "24px", fontSize: "12px"}} name={item.key} className="form-control" value={value || ""} onChange={this.handleChange}>
                                    <option value="">---</option>
                                    {this.getOptions(item.values)}
                                </select>)
                            }
                        </td>
                    </tr>
                );
            } else if (item.type === 'integer') {
                let value = "";
                let label = item.label;
                if (item.mandatory) {
                    label = '* ' + item.label;
                }
                let readOnly = false;
                if (item.readonly) {
                    readOnly = true;
                }
                if (!_.isEmpty(this.props.currentFeature) && this.props.currentFeature[item.key]) {
                    value = this.props.currentFeature[item.key];
                }
                return (
                    <tr style={{width: "100%"}} key={item.key + "-row"}>
                        <td style={{width: "40%"}}>
                            <ControlLabel>{label}</ControlLabel>
                        </td>
                        <td style={{width: "60%"}}>
                            <FormControl
                                style={{width: "100%", height: "24px", fontSize: "12px"}}
                                value={value}
                                readOnly={readOnly}
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
                let value = "";
                let label = item.label;
                if (item.mandatory) {
                    label = '* ' + item.label;
                }
                let readOnly = false;
                if (item.readonly) {
                    readOnly = true;
                }
                if (!_.isEmpty(this.props.currentFeature) && this.props.currentFeature[item.key]) {
                    value = this.props.currentFeature[item.key];
                }
                return (
                    <tr style={{width: "100%"}} key={item.key + "-row"}>
                        <td style={{width: "40%"}}>
                            <ControlLabel>{label}</ControlLabel>
                        </td>
                        <td style={{width: "60%"}}>
                            <FormControl
                                style={{width: "100%", height: "24px", fontSize: "12px"}}
                                value={value}
                                readOnly={readOnly}
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
                let value = false;
                let label = item.label;
                if (item.mandatory) {
                    label = '* ' + item.label;
                }
                if (!_.isEmpty(this.props.currentFeature) && this.props.currentFeature[item.key]) {
                    value = this.props.currentFeature[item.key];
                }
                {
                    let self = this;
                    let handleBooleanChange = function(evt) {
                        self.handleChange({target: {name: evt.target.name, value: evt.target.checked}});
                    };
                    return (
                        <tr style={{width: "100%"}} key={item.key + "-row"}>
                            <td style={{width: "40%"}}>
                                <ControlLabel>{label}</ControlLabel>
                            </td>
                            <td style={{width: "60%"}}>
                                {item.readonly ?
                                    (<Checkbox name={item.key} checked={value} disabled/>)
                                    :
                                    (<Checkbox name={item.key} checked={value} onChange={handleBooleanChange}/>)
                                }
                            </td>
                        </tr>
                    );
                }
            } else if (item.type === 'date') {
                let value = null;
                let label = item.label;
                if (item.mandatory) {
                    label = '* ' + item.label;
                }
                if (!_.isEmpty(this.props.currentFeature) && this.props.currentFeature[item.key]) {
                    value = this.props.currentFeature[item.key];
                }
                {
                    let self = this;
                    let handleDateChange = function(isoDate, formattedDate) {
                        self.handleChange({target: {name: item.key, value: formattedDate}});
                    };
                    return (
                        <tr style={{width: "100%"}} key={item.key + "-row"}>
                            <td style={{width: "40%"}}>
                                <ControlLabel>{label}</ControlLabel>
                            </td>
                            <td style={{width: "60%"}}>
                                {item.readonly ?
                                    (<DatePicker dateFormat="YYYY-MM-DD" disabled style={{height: "24px"}} value={value} />)
                                    :
                                    (<DatePicker dateFormat="YYYY-MM-DD" style={{height: "24px"}} value={value} onChange={handleDateChange} />)

                                }
                            </td>
                        </tr>
                    );
                }
            }
        });

        searchDiv = tabindex <= 2 && (this.props.isWriter || this.props.isPublisher) && this.props.featuresubtype !== 'na';
        console.log(this.state);
        return (
            <div className="nf-tab-content">
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
            </div>
        );
    },
    renderTabs() {
        let tabs = [];

        this.props.forms.map((tab, index) => {
            let i = index + 1;
            let key = "tab-" + i;
            let tabIcon = this.getIcon(tab.formname);
            tabs.push(
                <Tab eventKey={i} key={key} title={<Glyphicon glyph={tabIcon} style={{cursor: "pointer", fontSize: "24px"}}/>}>
                    {this.renderTabContent(tab, i)}
                    {(tab.formname === 'location') ? this.renderDrawTools() : null}
                </Tab>
            );
        });
        /*if (isMobile.any) {
            let lastIndex = tabs.length + 1;
            tabs.push(
                <Tab eventKey={lastIndex} key="resources" title={<Glyphicon glyph="camera" style={{cursor: "pointer", fontSize: "24px"}}/>}>
                    <div>
                        <input type="file" accept="image/*" id="captured-images" multiple="multiple" onChange={this.handleImageChange}/>
                        <output id="result" />
                    </div>
                </Tab>
            );
        }*/
        if (this.props.mode === 'ADD') {
            tabs.push(
                <Tab eventKey={(tabs.length + 1)} key="resources" title={<Glyphicon glyph="camera" style={{cursor: "pointer", fontSize: "24px"}}/>}>
                    <div className="nf-tab-content">
                        <span className="btn btn-default btn-file">
                            Select or capture images <input type="file" accept="image/*" id="captured-images" multiple="multiple" onChange={this.handleImageChange}/>
                        </span>
                        <output id="result" />
                    </div>
                </Tab>
            );
        }
        /*
        tabs.push(
            <Tab eventKey={tabs.length + 1} key="location" title={<Glyphicon glyph="uniE062" style={{cursor: "pointer", fontSize: "24px"}}/>}>
                {this.renderDrawTools()}
            </Tab>
        );*/
        return tabs;
    },
    renderButtons() {
        const cancel = (<Button key="cancel" bsSize="small"
                    bsStyle="primary"
                    onClick={this.props.cancel}
                    disabled={false}
                    style={{marginRight: "2px"}}>
                    <Message msgId="cancel" />
                </Button>);
        if (this.props.isWriter || this.props.isPublisher) {
            return (this.props.mode === 'EDIT') ? [cancel,
                <Button key="delete" bsSize="small"
                    bsStyle="primary"
                    onClick={() => this.props.onDelete(this.props.featuretype, this.props.currentFeature.id)}
                    style={{marginRight: "2px"}}
                    disabled={false}>
                    <Message msgId="naturalfeatures.delete" />
                </Button>,
                <Button key="update" bsSize="small"
                    bsStyle="primary"
                    onClick={() => this.props.onUpdate(this.props.featuretype, this.props.featuresubtype, this.props.currentFeature)}
                    disabled={false}>
                    <Message msgId="naturalfeatures.update" />
                </Button>

            ] : [cancel,
                <Button key="save" bsSize="small"
                    bsStyle="primary"
                    onClick={() => this.props.onUpdate(this.props.featuretype, this.props.featuresubtype, this.props.currentFeature)}
                    disabled={false}>
                    <Message msgId="naturalfeatures.save" />
                </Button>

            ];
        }
        return [];
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
                  {/*<ToggleButton
                      text={<Message msgId="naturalfeatures.get_my_loc" />}
                      style={{}}
                      pressed={this.props.getMyLocationEnabled}
                      onClick={this.onGetMyLocationClick} />*/}
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
    // <Tabs defaultActiveKey={1} id="naturalfeature-tabs" onSelect={this.handleVisibility}>
    render() {
        let title = Utils.getPrettyFeatureType(this.props.featuretype) + ` (${Utils.getPrettyFeatureSubType(this.props.featuresubtype)})`;
        return (
            <Dock
                zIndex={1030 /*below dialogs, above left menu*/}
                position={"right" /* 'left', 'top', 'right', 'bottom' */}
                size={this.props.dockSize}
                dimMode={"none" /*'transparent', 'none', 'opaque'*/}
                isVisible={this.props.isVisible}
                onVisibleChange={this.handleVisibleChange}
                onSizeChange={(this.limitDockHeight)}
                fluid={true}
                dimStyle={{ background: 'rgba(0, 0, 100, 0.2)' }}
                dockStyle={{ left: '0px', right: '0px'}}
                dockHiddenStyle={null}>
                <div style={{width: "100%", minHeight: "35px", fontSize: "26px", padding: "15px"}}>
                    <Glyphicon glyph="1-close" className="no-border btn-default" onClick={this.onClose} style={{cursor: "pointer"}}/>
                    <span className="nfd-form-title">{title}</span>
                </div>
                <div>
                    <Tabs defaultActiveKey={1} id="naturalfeature-tabs" ref={(tabs) => { this.tabs = tabs; }}>
                        {this.renderTabs()}
                    </Tabs>
                    <div className="nf-errors">
                        {this.renderErrors()}
                    </div>
                </div>
                <div className="dock-panel-footer">
                    <div className="dock-panel-footer-buttons">
                        {(this.props.mode === 'EDIT') ? this.renderHistoric() : null}
                        {this.renderButtons()}
                    </div>
                </div>
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
    limitDockHeight(size) {
        if (size >= this.props.maxDockSize) {
            this.props.setDockSize(this.props.maxDockSize);
        } else if (size <= this.props.minDockSize) {
            this.props.setDockSize(this.props.minDockSize);
        } else {
            this.props.setDockSize(size);
        }
    },
    handleChange(e) {
        if (e.target.value === '') {
            this.props.currentFeature[e.target.name] = null;
        } else {
            this.props.currentFeature[e.target.name] = e.target.value;
        }
        if (this.props.mode === 'EDIT') {
            this.setState({selectedFeature: this.props.currentFeature});
        } else if (this.props.mode === 'ADD') {
            this.setState({selectedFeature: this.props.currentFeature});
        }
    },
    loadImage(e) {
        const picFile = e.target;
        const output = document.getElementById("result");
        const div = document.createElement("div");
        div.innerHTML = "<img class='thumbnail' src='" + picFile.result + "'" + "title='" + picFile.name + "'/>";
        output.insertBefore(div, null);
        this.props.photos.push(picFile.result);
    },
    handleImageChange(event) {
        // Check File API support
        if (window.File && window.FileList && window.FileReader) {
            const files = event.target.files;
            for (let i = 0; i < files.length; i++) {
                let file = files[i];
                // Only pics
                if (!file.type.match('image')) continue;
                let picReader = new FileReader();
                picReader.addEventListener("load", this.loadImage);
                // Read the image
                picReader.readAsDataURL(file);
            }
        } else {
            console.log("Your browser does not support File API");
        }
    }
});

module.exports = DockedNaturalFeatures;
