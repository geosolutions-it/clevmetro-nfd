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
const Message = require('../../../MapStore2/web/client/components/I18N/Message');
const ToggleButton = require('../../../MapStore2/web/client/components/buttons/ToggleButton');
const _ = require('lodash');
// const isMobile = require('ismobilejs');
require('react-selectize/themes/index.css');
require('./DockedNaturalFeatures.css');

const DockedNaturalFeatures = React.createClass({
    propTypes: {
        forms: React.PropTypes.array,
        featuretype: React.PropTypes.string,
        featuresubtype: React.PropTypes.string,
        currentFeature: React.PropTypes.object,
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
        addPointGlyph: React.PropTypes.string,
        addPointEnabled: React.PropTypes.bool,
        addPolygonGlyph: React.PropTypes.string,
        addPolygonEnabled: React.PropTypes.bool,
        getMyLocationEnabled: React.PropTypes.bool,
        onChangeDrawingStatus: React.PropTypes.func,
        onEndDrawing: React.PropTypes.func,
        photos: React.PropTypes.array
    },
    getDefaultProps() {
        return {
            forms: [],
            photos: [],
            currentFeature: {},
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
            previousVersion: () => {},
            nextVersion: () => {},
            onChangeDrawingStatus: () => {},
            onEndDrawing: () => {}
        };
    },
    componentWillMount: function() {
        this.props.onChangeDrawingStatus("clean", null, "dockednaturalfeatures", [], {});
    },
    onClose: function() {
        this.props.onToggle();
        this.props.onChangeDrawingStatus("clean", null, "dockednaturalfeatures", [], {});
    },
    onAddPointClick: function() {
        this.props.onChangeDrawingStatus("start", "Marker", "dockednaturalfeatures", [], {icon: '../../assets/img/marker-icon-green.png'});
    },
    onAddPolygonClick: function() {
        this.props.onChangeDrawingStatus("start", "Polygon", "dockednaturalfeatures", [], {});
    },
    onGetMyLocationClick: function() {
        this.props.onChangeDrawingStatus("start", "Polygon", "dockednaturalfeatures", [], {});
    },
    getIcon(formname) {
        let icon = 'question-sign';
        if (formname === 'species') {
            icon = 'question-sign';
        } else if (formname === 'species.element_species') {
            icon = 'question-sign';
        } else if (formname.includes("details")) {
            icon = 'th-list';
        } else if (formname.includes("lifestages")) {
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
        } else if (formname === 'photograh') {
            icon = 'question-sign';
        } else if (formname === 'location') {
            icon = 'question-sign';
        }
        return icon;
    },
    getOptions(values) {
        return values.items.map((item, index) => {
            return (
                <option value={item.key} key={index}>{item.value}</option>
            );
        });
    },
    renderTabContent(tab) {
        let tabName = tab.formlabel;
        let items = tab.formitems.map((item) => {
            if (item.type === 'string') {
                let value = "";
                if (!_.isEmpty(this.props.currentFeature) && this.props.currentFeature[item.key]) {
                    value = this.props.currentFeature[item.key];
                }
                return (
                    <tr style={{width: "100%"}} key={item.key + "-row"}>
                        <td style={{width: "40%"}}>
                            <ControlLabel>{item.label}</ControlLabel>
                        </td>
                        <td style={{width: "60%"}}>
                            {this.props.isAdmin ?
                                (<FormControl
                                    style={{width: "100%", height: "24px", fontSize: "12px"}}
                                    value={value}
                                    onChange={this.handleChange}
                                    key={item.key}
                                    name={item.key}
                                    componentClass="input"
                                    type="text"/>)
                                :
                                (<FormControl
                                    style={{width: "100%", height: "24px", fontSize: "12px"}}
                                    readOnly
                                    value={value}
                                    key={item.key}
                                    name={item.key}
                                    componentClass="input"
                                    type="text"/>)
                            }
                        </td>
                    </tr>
                );
            } else if (item.type === 'stringcombo') {
                let value = "";
                if (!_.isEmpty(this.props.currentFeature) && this.props.currentFeature[item.key]) {
                    value = this.props.currentFeature[item.key];
                }
                return (
                    <tr style={{width: "100%"}} key={item.key + "-row"}>
                        <td style={{width: "40%"}}>
                            <ControlLabel>{item.label}</ControlLabel>
                        </td>
                        <td style={{width: "60%"}}>
                            {this.props.isAdmin ?
                                (<select style={{height: "24px"}} className="form-control" value={value || ""}>
                                    <option value="">---</option>
                                    {this.getOptions(item.values)}
                                </select>)
                                :
                                (<select disabled style={{height: "24px"}} className="form-control" bsSize="small" value={value || ""}>
                                    {this.getOptions(item.values)}
                                </select>)
                            }
                        </td>
                    </tr>
                );
            } else if (item.type === 'integer') {
                let value = "";
                if (!_.isEmpty(this.props.currentFeature) && this.props.currentFeature[item.key]) {
                    value = this.props.currentFeature[item.key];
                }
                return (
                    <tr style={{width: "100%"}} key={item.key + "-row"}>
                        <td style={{width: "40%"}}>
                            <ControlLabel>{item.label}</ControlLabel>
                        </td>
                        <td style={{width: "60%"}}>
                            {this.props.isAdmin ?
                                (<FormControl
                                    style={{width: "100%", height: "24px", fontSize: "12px"}}
                                    value={value}
                                    onChange={this.handleChange}
                                    key={item.key}
                                    name={item.key}
                                    componentClass="input"
                                    min="0"
                                    step="1"
                                    type="number"/>)
                                :
                                (<FormControl
                                    style={{width: "100%", height: "24px", fontSize: "12px"}}
                                    readOnly
                                    value={value}
                                    key={item.key}
                                    name={item.key}
                                    componentClass="input"
                                    min="0"
                                    step="1"
                                    type="number"/>)
                            }
                        </td>
                    </tr>
                );
            } else if (item.type === 'double') {
                let value = "";
                if (!_.isEmpty(this.props.currentFeature) && this.props.currentFeature[item.key]) {
                    value = this.props.currentFeature[item.key];
                }
                return (
                    <tr style={{width: "100%"}} key={item.key + "-row"}>
                        <td style={{width: "40%"}}>
                            <ControlLabel>{item.label}</ControlLabel>
                        </td>
                        <td style={{width: "60%"}}>
                            {this.props.isAdmin ?
                                (<FormControl
                                    style={{width: "100%", height: "24px", fontSize: "12px"}}
                                    value={value}
                                    onChange={this.handleChange}
                                    key={item.key}
                                    name={item.key}
                                    componentClass="input"
                                    min="0"
                                    step="any"
                                    type="number"/>)
                                :
                                (<FormControl
                                    style={{width: "100%", height: "24px", fontSize: "12px"}}
                                    readOnly
                                    value={value}
                                    key={item.key}
                                    name={item.key}
                                    componentClass="input"
                                    min="0"
                                    step="any"
                                    type="number"/>)
                            }
                        </td>
                    </tr>
                );
            } else if (item.type === 'boolean') {
                let value = false;
                if (!_.isEmpty(this.props.currentFeature) && this.props.currentFeature[item.key]) {
                    value = this.props.currentFeature[item.key];
                }
                return (
                    <tr style={{width: "100%"}} key={item.key + "-row"}>
                        <td style={{width: "40%"}}>
                            <ControlLabel>{item.label}</ControlLabel>
                        </td>
                        <td style={{width: "60%"}}>
                            {this.props.isAdmin ?
                                (<Checkbox checked={value} onChange={this.handleChange}/>)
                                :
                                (<Checkbox checked={value} disabled/>)
                            }
                        </td>
                    </tr>
                );
            } else if (item.type === 'date') {
                let value = null;
                if (!_.isEmpty(this.props.currentFeature) && this.props.currentFeature[item.key]) {
                    value = this.props.currentFeature[item.key];
                }
                return (
                    <tr style={{width: "100%"}} key={item.key + "-row"}>
                        <td style={{width: "40%"}}>
                            <ControlLabel>{item.label}</ControlLabel>
                        </td>
                        <td style={{width: "60%"}}>
                            {this.props.isAdmin ?
                                (<DatePicker style={{height: "24px"}} value={value} onChange={this.handleChange} />)
                                :
                                (<DatePicker disabled style={{height: "24px"}} value={value} />)
                            }
                        </td>
                    </tr>
                );
            }
        });
        return (
            <div className="nf-tab-content">
                <Table style={{width: "100%"}} responsive striped condensed bordered>
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
                    {this.renderTabContent(tab)}
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
        if (this.props.mode === 'add') {
            let lastIndex = tabs.length + 1;
            tabs.push(
                <Tab eventKey={lastIndex} key="resources" title={<Glyphicon glyph="camera" style={{cursor: "pointer", fontSize: "24px"}}/>}>
                    <div className="nf-tab-content">
                        <span className="btn btn-default btn-file">
                            Select or capture images <input type="file" accept="image/*" id="captured-images" multiple="multiple" onChange={this.handleImageChange}/>
                        </span>
                        <output id="result" />
                    </div>
                </Tab>
            );
        }
        return tabs;
    },
    renderButtons() {
        return (this.props.mode === 'viewedit') ? [
            <Button key="delete" bsSize="small"
                bsStyle="primary"
                onClick={() => this.props.onDelete(this.props.featuretype, this.props.currentFeature.id)}
                style={{marginRight: "10px"}}
                disabled={false}>
                <Message msgId="naturalfeatures.delete" />
            </Button>,
            <Button key="update" bsSize="small"
                bsStyle="primary"
                onClick={() => this.props.onUpdate(this.props.featuretype, this.props.featuresubtype, this.props.currentFeature)}
                disabled={false}>
                <Message msgId="naturalfeatures.update" />
            </Button>

        ] : [
            <Button key="save" bsSize="small"
                bsStyle="primary"
                onClick={() => this.props.onSave(this.props.currentFeature)}
                disabled={false}>
                <Message msgId="naturalfeatures.save" />
            </Button>

        ];
    },
    renderHistoric() {
        return (
            <div className="nf-historic">
                <Button key="previous" bsSize="small"
                    bsStyle="primary"
                    onClick={() => this.props.previousVersion()}
                    disabled={true}>
                    <Glyphicon glyph={"menu-left"}/>
                </Button>
                <span className="nf-historic-date">17-5-2017</span>
                <Button key="next" bsSize="small"
                    bsStyle="primary"
                    onClick={() => this.props.nextVersion(this.props.currentFeature)}
                    disabled={false}>
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
                  <ToggleButton
                      text={<Message msgId="naturalfeatures.get_my_loc" />}
                      style={{}}
                      pressed={this.props.getMyLocationEnabled}
                      onClick={this.onGetMyLocationClick} />
              </div>
          </div>
        );
    },
    // {(this.props.mode === 'add') ? this.renderDrawTools() : null}
    render() {
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
                </div>
                <div>
                    <Tabs defaultActiveKey={1} id="naturalfeature-tabs" onSelect={this.handleVisibility}>
                        {this.renderTabs()}
                    </Tabs>
                </div>
                <div className="dock-panel-footer">
                    <div className="dock-panel-footer-buttons">
                        {(this.props.mode === 'viewedit') ? this.renderHistoric() : null}
                        {this.renderButtons()}
                    </div>
                </div>
            </Dock>
        );
    },
    handleVisibility(index, label) {
        if (this.props.mode === 'add') {
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
        this.props.currentFeature[e.target.name] = e.target.value;
        if (this.props.mode === 'viewedit') {
            this.setState({selectedFeature: this.props.currentFeature});
        } else if (this.props.mode === 'add') {
            this.setState({newFeature: this.props.currentFeature});
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
