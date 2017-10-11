/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/
const React = require('react');
const PropTypes = require('prop-types');
const {asyncContainer, Typeahead} = require("react-bootstrap-typeahead");
const AsyncTypeahead = asyncContainer(Typeahead);

function isPresent(options = [], query) {
    return options.filter( o => o.name.toLowerCase().indexOf(query.toLowerCase()) === 0).length > 0;
}

class SpeciesSelector extends React.Component {
    static propTypes = {
      options: React.PropTypes.array,
      selectedSpecies: PropTypes.object,
      bsSize: PropTypes.string,
      maxResults: PropTypes.number,
      placeholder: PropTypes.string,
      onChange: PropTypes.func,
      onSearch: PropTypes.func
    }
    static defaultProps = {
        onSearch: () => {},
        onChange: () => {},
        bsSize: 'small',
        maxResults: 20,
        placeholder: "Search for a species..."
    }
    shouldComponentUpdate({options, selectedSpecies}) {
        return options !== this.props.options || selectedSpecies !== this.props.selectedSpecies;
    }
    componentDidUpdate(prevProps) {
        if (!this.props.selectedSpecies && prevProps.selectedSpecies && this.AsyncTypeahead) {
            this.AsyncTypeahead.getInstance().clear();
        }
    }
    componentWillUnmount() {
        this.AsyncTypeahead = null;
    }
    render() {
        const {options, selectedSpecies, maxResults, bsSize, placeholder} = this.props;
        return (
            <AsyncTypeahead
                ref={this.addRef}
                options={options}
                labelKey="name"
                bsSize={bsSize}
                maxResults={maxResults}
                onSearch={this._onSearch}
                placeholder={placeholder}
                renderMenuItemChildren={this._renderMenuItemChildren}
                selected={[selectedSpecies]}
                onChange={this._handleSpeciesChange}
                minLength={2}
            />);
    }
    addRef = (ref) => {
        this.AsyncTypeahead = ref;
    }
    _onSearch = (query) => {
        if (!isPresent(this.props.options, query)) {
            this.props.onSearch(query);
        }
    }
    _renderMenuItemChildren = (option) => {
        return (
            <div key={option.id}>
                <span>{option.name}</span>
            </div>
        );
    }
    _handleSpeciesChange = (species) => {
        if (species.length > 0) {
            this.props.onChange(species[0]);
        }else if (this.props.selectedSpecies) {
            this.props.onChange();
        }
    }
}

module.exports = SpeciesSelector;
