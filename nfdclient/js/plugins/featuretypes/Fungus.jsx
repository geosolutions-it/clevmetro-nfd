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
const {onToggleExport} = require('../../actions/exportfeatures');
const FilterUtils = require('../../utils/FilterUtils');

const dataSelector = (state) => state.featuresearch && state.featuresearch.fungus || {};
const dataFilterSelector = (state) => state.featuresearch && state.featuresearch.fungus_filters || {};

const toggleExport = onToggleExport.bind(null, 'LIST', 'fungus', null);
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

const resetFilters = resetFtFilters.bind(null, 'fungus');
const upDateFeatureType = loadList.bind(null, 'fungus', 1);

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

const onSearch = searchSpecies.bind(null, 'fungus');
const onSpeciesChange = setFilterProp.bind(null, 'fungus', 'selectedSpecies');

const SpeciesSelector = connect((state) => {
    const data = dataFilterSelector(state);
    return {
        options: data.species,
        selectedSpecies: data.selectedSpecies
}; }, {
    onSearch,
    onChange: onSpeciesChange
})(require('../../components/naturalfeatures/SpeciesSelector'));

const onReleasedChange = setFilterProp.bind(null, 'fungus', 'released');

const ReleasedFilter = connect((state) => {
    const data = dataFilterSelector(state);
    return {
        value: !!data.released
    };
}, {
    onChange: onReleasedChange
})(require('../../components/naturalfeatures/CheckFilter'));

const onNotReleasedChange = setFilterProp.bind(null, 'fungus', 'notreleased');

const NotReleasedFilter = connect((state) => {
    const data = dataFilterSelector(state);
    return {
        value: !!data.notreleased
    };
}, {
    onChange: onNotReleasedChange
})(require('../../components/naturalfeatures/CheckFilter'));

const updateFieldValue = setFilterProp.bind(null, 'fungus');

const DateFiled = connect((state) => {
    const data = dataFilterSelector(state);
    return {
        operator: data.operator || state.featuresearch && state.featuresearch.defaultOperator,
        fieldValue: data.includevalue
    };
}, {
    updateFieldValue
})(require('../../components/naturalfeatures/DateFilter'));

class Fungus extends React.Component {
    static propTypes = {
      height: React.PropTypes.number
    }
    render() {
        return (
            <FeatureTypePanel featureType="fungus">
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

module.exports = Fungus;
