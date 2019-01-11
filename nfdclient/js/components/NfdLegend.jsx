/**
 * Copyright 2019, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
var React = require('react');


let NfdLegend = React.createClass({
    propTypes: {
        isMobile: React.PropTypes.bool
    },
    getDefaultProps() {
        return {
          isMobile: false
        };
    },
    getInitialState() {
        return { hideLegend: this.props.isMobile};
    },
    toggleLegend(e) {
        e.preventDefault();
        e.stopPropagation();
        if (this.props.isMobile) {
            let bkg = document.getElementsByClassName("background-plugin-position").item(0);
            if (bkg) {
                bkg.style.bottom = this.state.hideLegend ? "200px" : "40px";
            }
            this.setState((state) => ({hideLegend: !state.hideLegend}));
        }
    },
    render() {
        return this.state.hideLegend && (
                <div id="nfd-legend" className="nfd-legend mini" onClick={this.toggleLegend}>
                    <div className="row flex-center">
                        <div className="col-xs-2">
                            <span className="glyphicon glyphicon-list"></span>
                        </div>
                    </div>
                </div>) || (
                <div id="nfd-legend" className="nfd-legend" onClick={this.toggleLegend}>
                    <div className="row flex-center">
                        <div className="marker-plant col-xs-2"/>
                        <div className="col-xs-9">
                            <label>Plants</label>
                        </div>
                    </div>
                    <div className="row flex-center">
                        <div className="marker-fungus col-xs-2"/>
                        <div className="col-xs-9">
                            <label>Fungi</label>
                        </div>
                    </div>
                    <div className="row flex-center">
                        <div className="marker-animal col-xs-2"/>
                        <div className="col-xs-9">
                            <label>Animals</label>
                        </div>
                    </div>
                    <div className="row flex-center">
                        <div className="marker-slimemold col-xs-2"/>
                        <div className="col-xs-9">
                            <label>Slime mold</label>
                        </div>
                    </div>
                    <div className="row flex-center">
                        <div className="marker-naturalarea col-xs-2"/>
                        <div className="col-xs-9">
                            <label>Natural areas</label>
                        </div>
                    </div>
                </div>
            );
    }
});

module.exports = NfdLegend;
