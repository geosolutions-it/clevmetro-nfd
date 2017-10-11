/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/

const React = require('react');
const PropTypes = require('prop-types');

class FilterElement extends React.Component {
        static propTypes = {
          children: PropTypes.node,
          label: PropTypes.string
        }
        static defaultProps = {
          label: ''
        }
        render() {
            const {label, children} = this.props;
            return (
                <div className="feature-filter">
                    <div className="container-fluid">
                        <div className="row">
                            <div className="col-xs-12">
                                <h5>{label}</h5>
                                {children ? children : null}
                            </div>
                        </div>
                    </div>
                </div>
                );
        }
}

module.exports = FilterElement;
