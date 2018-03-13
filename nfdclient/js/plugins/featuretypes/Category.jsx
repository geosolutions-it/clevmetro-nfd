/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/

const React = require('react');
const {connect} = require('react-redux');
const {createSelector} = require('reselect');

const {loadList, selectFeature, zooToFeature, setFilterProp, resetFtFilters, toggleSearchPanel} = require('../../actions/featuresearch');
const {onToggleExport} = require('../../actions/exportfeatures');
const FilterUtils = require('../../utils/FilterUtils');
const SelectFilter = require('../../components/naturalfeatures/SelectFilter');
const FilterElement = require('../../components/naturalfeatures/FilterElement');

const category = (type) => {

    const dataSelector = (state) => state.featuresearch && state.featuresearch[type] || {};
    const dataFilterSelector = (state) => state.featuresearch && state.featuresearch[`${type}_filters`] || {};
    const filtersSelector = (state) => state.featuresearch && state.featuresearch.filters;

    const reservationSelector = createSelector([filtersSelector, dataFilterSelector],
        (filters = [], values = {}) => ({
            value: values.reservation,
            options: (filters.filter((f) => f.name === 'reservation')[0] || {}).options || []
         })
        );
    const watershedSelector = createSelector([filtersSelector, dataFilterSelector],
        (filters = [], values = {}) => ({
            value: values.watershed,
            options: (filters.filter((f) => f.name === 'watershed')[0] || {}).options || []
        })
        );
    const cmStatusSelector = createSelector([filtersSelector, dataFilterSelector],
        (filters = [], values = {}) => ({
            value: values.cm_status,
            options: (filters.filter((f) => f.name === 'cm_status')[0] || {}).options || []
        })
        );

    const toggleExport = onToggleExport.bind(null, 'LIST', type, null, null);
    const onPanelChange = toggleSearchPanel.bind(null, type);
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

    const resetFilters = resetFtFilters.bind(null, type);
    const upDateFeatureType = loadList.bind(null, type, 1);

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

    const onRankChange = setFilterProp.bind(null, type, 'taxon');
    const RankFilter = connect((state) => {
        const data = dataFilterSelector(state);
        return {
            value: data.taxon || ''
    }; }, {
        onChange: onRankChange
    })(require('../../components/naturalfeatures/UpperRankfilter'));


    const onResChange = setFilterProp.bind(null, type, 'reservation');
    const ReservetionFilter = connect(reservationSelector, {
        onChange: onResChange
    })(SelectFilter);

    const onWaterChange = setFilterProp.bind(null, type, 'watershed');
    const WatershedFilter = connect(watershedSelector, {
        onChange: onWaterChange
    })(SelectFilter);


    const onStatusChange = setFilterProp.bind(null, type, 'cm_status');
    const CmStatusFilter = connect(cmStatusSelector, {
        onChange: onStatusChange
    })(SelectFilter);


    class Category extends React.Component {
        static propTypes = {
            height: React.PropTypes.number
        }
        render() {
            return (
                <FeatureTypePanel featureType={type}>
                    <FeaturesPanel height={this.props.height}>
                        <FeatureCard/>
                    </FeaturesPanel>
                    <FilterPanel height={this.props.height}>
                        <FilterElement label="by Ranks">
                            <RankFilter/>
                        </FilterElement>
                        <FilterElement label="by Reservetion">
                            <ReservetionFilter placeholder="Search for reservation..." labelKey="value"/>
                        </FilterElement>
                        <FilterElement label="by Watershed">
                            <WatershedFilter placeholder="Search for watershed..." labelKey="value"/>
                        </FilterElement>
                        <FilterElement label="by Status">
                            <CmStatusFilter placeholder="Search for status..." labelKey="value"/>
                        </FilterElement>
                    </FilterPanel>
                </FeatureTypePanel>
                );
        }
    }
    return Category;
};

module.exports = category;
