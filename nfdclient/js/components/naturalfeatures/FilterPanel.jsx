/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/

const React = require('react');
const PropTypes = require('prop-types');
const {Button, ButtonGroup} = require('react-bootstrap');

const FilterPanel = ({height, children, onReset, onUpdate, disableSync}) => {
    return (
        <div className="filter-panel">
            <div style={{overflow: 'auto', height: height - 10 - 59 - 59 - 2 - 30 - 40}} className="ft-filter">
                {children ? children : null}
            </div>
            <div className="row" style={{height: 40}}>
                <div className="text-center col-xs-12">
                    <ButtonGroup>
                        <Button onClick={onReset}>Clear</Button>
                        <Button disabled={disableSync} onClick={onUpdate}>Sync</Button>
                    </ButtonGroup>
                </div>
            </div>
        </div>);
};


FilterPanel.propTypes = {
  height: PropTypes.number,
  children: PropTypes.node,
  onReset: PropTypes.func,
  onUpdate: PropTypes.func,
  disableSync: PropTypes.bool
};

FilterPanel.defaultProps = {
    height: 100,
    onReset: () => {},
    onUpdate: () => {}
};

module.exports = FilterPanel;
