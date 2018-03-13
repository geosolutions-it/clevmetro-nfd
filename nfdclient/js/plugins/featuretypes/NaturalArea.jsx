/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/

const React = require('react');
const {connect} = require('react-redux');

const {loadList, selectFeature, zooToFeature, setFilterProp, resetFtFilters,
toggleSearchPanel} = require('../../actions/featuresearch');
const {onToggleExport} = require('../../actions/exportfeatures');
const FilterUtils = require('../../utils/FilterUtils');
const SelectFilter = require('../../components/naturalfeatures/SelectFilter');
const {createSelector} = require('reselect');

const dataSelector = (state) => state.featuresearch && state.featuresearch.naturalarea || {};
const dataFilterSelector = (state) => state.featuresearch && state.featuresearch.naturalarea_filters || {};
const filtersSelector = (state) => state.featuresearch && state.featuresearch.filters;

const cmStatusSelector = createSelector([filtersSelector, dataFilterSelector],
    (filters = [], values = {}) => ({
        value: values.cm_status,
        options: (filters.filter((f) => f.name === 'cm_status')[0] || {}).options || []
    })
    );

const toggleExport = onToggleExport.bind(null, 'LIST', 'naturalarea', null, null);
const onPanelChange = toggleSearchPanel.bind(null, 'naturalarea');
const FeatureTypePanel = connect((state) => {
    const data = dataSelector(state);
    return {
        activePanel: data.activePanel || 'features'
    };

}, {
    onPanelChange,
    toggleExport
})(require('../../components/naturalfeatures/FeatureTypePanel'));

const FeaturesPanel = connect((state) => {
    const data = dataSelector(state);
    return {
        features: data.features || [],
        page: data.page || 0,
        total: data.total || 0,
        pageSize: state.featuresearch && state.featuresearch.pageSize || 30
    };
}, {
    loadFtType: loadList
})(require('../../components/naturalfeatures/FeaturesPanel'));

const FeatureCard = connect((state) => ({
    enableEdit: state.naturalfeatures && (state.naturalfeatures.mode !== 'ADD' && state.naturalfeatures.mode !== 'EDIT')
}), {
    onEdit: selectFeature,
    onZoom: zooToFeature
})(require('../../components/naturalfeatures/FeatureCard'));

const FilterElement = require('../../components/naturalfeatures/FilterElement');

const resetFilters = resetFtFilters.bind(null, 'naturalarea');
const upDateFeatureType = loadList.bind(null, 'naturalarea', 1);

const FilterPanel = connect((state) => {
    const filters = dataFilterSelector(state);
    const featuresInfo = dataSelector(state);
    return {
        disableSync: FilterUtils.equalFilters(filters, featuresInfo.filter)
    };
}, {
    onReset: resetFilters,
    onUpdate: upDateFeatureType
})(require('../../components/naturalfeatures/FilterPanel'));

const onStatusChange = setFilterProp.bind(null, 'naturalarea', 'cm_status');
const CmStatusFilter = connect(cmStatusSelector, {
    onChange: onStatusChange
})(SelectFilter);

class NaturalArea extends React.Component {
    static propTypes = {
      height: React.PropTypes.number
    }
    render() {
        return (
            <FeatureTypePanel featureType="naturalarea">
                <FeaturesPanel height={this.props.height}>
                    <FeatureCard/>
                </FeaturesPanel>
                <FilterPanel height={this.props.height}>
                    <FilterElement label="by Status">
                        <CmStatusFilter placeholder="Search for status..." labelKey="value"/>
                    </FilterElement>
                </FilterPanel>
            </FeatureTypePanel>
            );
    }
}

module.exports = NaturalArea;
