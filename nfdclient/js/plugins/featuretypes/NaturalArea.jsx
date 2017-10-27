/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/

const React = require('react');
const {connect} = require('react-redux');

const {loadList, selectFeature, zooToFeature, setFilterProp, resetFtFilters} = require('../../actions/featuresearch');
const {onToggleExport} = require('../../actions/exportfeatures');
const FilterUtils = require('../../utils/FilterUtils');

const dataSelector = (state) => state.featuresearch && state.featuresearch.naturalarea || {};
const dataFilterSelector = (state) => state.featuresearch && state.featuresearch.naturalarea_filters || {};

const toggleExport = onToggleExport.bind(null, 'LIST', 'naturalarea', null);
const FeatureTypePanel = connect(() => ({}), {
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

const onReleasedChange = setFilterProp.bind(null, 'naturalarea', 'released');

const ReleasedFilter = connect((state) => {
    const data = dataFilterSelector(state);
    return {
        value: !!data.released
    };
}, {
    onChange: onReleasedChange
})(require('../../components/naturalfeatures/CheckFilter'));

const onNotReleasedChange = setFilterProp.bind(null, 'naturalarea', 'notreleased');

const NotReleasedFilter = connect((state) => {
    const data = dataFilterSelector(state);
    return {
        value: !!data.notreleased
    };
}, {
    onChange: onNotReleasedChange
})(require('../../components/naturalfeatures/CheckFilter'));

const updateFieldValue = setFilterProp.bind(null, 'naturalarea');

const DateFiled = connect((state) => {
    const data = dataFilterSelector(state);
    return {
        operator: data.operator || state.featuresearch && state.featuresearch.defaultOperator,
        fieldValue: data.includevalue
    };
}, {
    updateFieldValue
})(require('../../components/naturalfeatures/DateFilter'));

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
                    <FilterElement label="by Inclusion date">
                        <DateFiled/>
                    </FilterElement>
                    <FilterElement label="by Properties">
                        <ReleasedFilter label="Released"/>
                        <NotReleasedFilter label="Not released"/>
                    </FilterElement>
                </FilterPanel>
            </FeatureTypePanel>
            );
    }
}

module.exports = NaturalArea;
