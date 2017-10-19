/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/

const React = require('react');
const PropTypes = require('prop-types');

const {ListGroup} = require('react-bootstrap');
const PaginationToolbar = require('../../ms2Override/PaginationToolbar');

const FeaturesPanel = ({featureType, features, height, pageSize, page, total, loadFtType, children}) => {
    const loadFeatures = (p) => {
        if ( loadFtType) {
            loadFtType(featureType, p + 1);
        }
    };
    return (
        <div>
            <div style={{overflow: 'auto', height: height - 10 - 59 - 59 - 2 - 20 - 84}} className="ft-list-container">
                <ListGroup>
                    {features.map((ft, idx) => React.cloneElement(children, {key: idx, feature: ft}))}
                </ListGroup>
            </div>
            <div className="row">
                <div className="text-center col-xs-12">
                    <PaginationToolbar items={features} pageSize={pageSize} page={page - 1} total={total} onSelect={loadFeatures}/>
                </div>
            </div>
        </div>);
};


FeaturesPanel.propTypes = {
  features: PropTypes.array,
  featureType: PropTypes.string.isRequired,
  height: PropTypes.number,
  pageSize: PropTypes.number,
  page: PropTypes.number,
  total: PropTypes.number,
  loadFtType: PropTypes.func.isRequired,
  children: PropTypes.node
};

FeaturesPanel.defaultProps = {
  pageSize: 10,
  page: 0,
  total: 0,
  features: [],
  onEdit: () => {},
  onZoom: () => {}
};

module.exports = FeaturesPanel;
