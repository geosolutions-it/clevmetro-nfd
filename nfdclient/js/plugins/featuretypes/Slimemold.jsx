/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/

const React = require('react');
const {connect} = require('react-redux');

const {loadList, selectFeature, zooToFeature, searchSpecies, setFilterProp, resetFtFilters} = require('../../actions/featuresearch');

const FilterUtils = require('../../utils/FilterUtils');
const {onToggleExport} = require('../../actions/exportfeatures');
const dataSelector = (state) => state.featuresearch && state.featuresearch.slimemold || {};
const dataFilterSelector = (state) => state.featuresearch && state.featuresearch.slimemold_filters || {};

const toggleExport = onToggleExport.bind(null, 'LIST', 'slimemold', null);
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

const resetFilters = resetFtFilters.bind(null, 'slimemold');
const upDateFeatureType = loadList.bind(null, 'slimemold', 1);

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

const onSearch = searchSpecies.bind(null, 'slimemold');
const onSpeciesChange = setFilterProp.bind(null, 'slimemold', 'selectedSpecies');

const SpeciesSelector = connect((state) => {
    const data = dataFilterSelector(state);
    return {
        options: data.species,
        selectedSpecies: data.selectedSpecies
}; }, {
    onSearch,
    onChange: onSpeciesChange
})(require('../../components/naturalfeatures/SpeciesSelector'));

const onReleasedChange = setFilterProp.bind(null, 'slimemold', 'released');

const ReleasedFilter = connect((state) => {
    const data = dataFilterSelector(state);
    return {
        value: !!data.released
    };
}, {
    onChange: onReleasedChange
})(require('../../components/naturalfeatures/CheckFilter'));

const onNotReleasedChange = setFilterProp.bind(null, 'slimemold', 'notreleased');

const NotReleasedFilter = connect((state) => {
    const data = dataFilterSelector(state);
    return {
        value: !!data.notreleased
    };
}, {
    onChange: onNotReleasedChange
})(require('../../components/naturalfeatures/CheckFilter'));

const updateFieldValue = setFilterProp.bind(null, 'slimemold');

const DateFiled = connect((state) => {
    const data = dataFilterSelector(state);
    return {
        operator: data.operator || state.featuresearch && state.featuresearch.defaultOperator,
        fieldValue: data.includevalue
    };
}, {
    updateFieldValue
})(require('../../components/naturalfeatures/DateFilter'));

class SlimeMold extends React.Component {
    static propTypes = {
      height: React.PropTypes.number
    }
    render() {
        return (
            <FeatureTypePanel featureType="slimemold">
                <FeaturesPanel height={this.props.height}>
                    <FeatureCard/>
                </FeaturesPanel>
                <FilterPanel height={this.props.height}>
                    <FilterElement label="by Species">
                        <SpeciesSelector/>
                    </FilterElement>
                    <FilterElement label="by Inclusion date">
                        <DateFiled/>
                    </FilterElement>
                    <FilterElement label="by Properties">
                        <ReleasedFilter label="released"/>
                        <NotReleasedFilter label="Not released"/>
                    </FilterElement>
                </FilterPanel>
            </FeatureTypePanel>
            );
    }
}

module.exports = SlimeMold;
