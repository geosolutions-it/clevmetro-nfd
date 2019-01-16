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
const isMobile = require('ismobilejs');
const Api = require('../../api/naturalfeaturesdata');
const noFilter = () => true;
class SpeciesSelector extends React.Component {
    static propTypes = {
      options: React.PropTypes.array,
      selectedSpecies: PropTypes.object,
      bsSize: PropTypes.string,
      maxResults: PropTypes.number,
      placeholder: PropTypes.string,
      onChange: PropTypes.func,
      onSearch: PropTypes.func,
      paginate: PropTypes.bool,
      clearBtn: PropTypes.bool,
      labelKey: React.PropTypes.string,
      keyName: React.PropTypes.string,
      isLoading: PropTypes.bool,
      featuretype: PropTypes.string
    };
    static defaultProps = {
        onSearch: () => {},
        onChange: () => {},
        paginate: true,
        clearBtn: false,
        bsSize: 'small',
        maxResults: 5,
        labelKey: "name",
        placeholder: "Search for a species...",
        keyName: "id",
        isLoading: false
    }
    constructor(props) {
        super(props);
        this.state = {full: false, isLoading: false};
    }
    shouldComponentUpdate({ selectedSpecies}, {full, isLoading, options}) {
        return isLoading !== this.state.isLoading || this.state.full !== full || options !== this.state.options || selectedSpecies !== this.props.selectedSpecies;
    }
    componentDidUpdate(prevProps) {
        // Clean selector if selectedSpecies is null
        if (!this.props.selectedSpecies && prevProps.selectedSpecies && this.AsyncTypeahead) {
            this.AsyncTypeahead.getInstance().clear();
            this.AsyncTypeahead.getInstance().blur();
        }

    }
    componentWillUnmount() {
        this.AsyncTypeahead = null;
    }
    render() {

        const {selectedSpecies, maxResults, bsSize, placeholder, paginate, clearBtn} = this.props;
        const {options, isLoading, full} = this.state;
        return (
            <div className={full ? 'spec-selector-full' : ''} onClick={this.exitFull}>
                <AsyncTypeahead
                    filterBy={noFilter}
                    delay={400}
                    clearButton={clearBtn}
                    onFocus={this.enterFull}
                    paginate={paginate}
                    ref={this.addRef}
                    options={options}
                    labelKey="name"
                    bsSize={bsSize}
                    emptyLabel={isLoading ? "Searching..." : undefined}
                    maxResults={maxResults}
                    onSearch={this._onSearch}
                    placeholder={placeholder}
                    renderMenuItemChildren={this._renderMenuItemChildren}
                    selected={[selectedSpecies]}
                    onChange={this._handleSpeciesChange}
                    minLength={2}
                    isLoading={isLoading}
                    useCache={false}
                    searchText="Searching..."
                />
            </div>);
    }
    addRef = (ref) => {
        this.AsyncTypeahead = ref;
    }
    _onSearch = (query) => {
        if (query) {
            this.setState(()=>({isLoading: true, options: undefined}));
            Api.searchSpecies(query, this.props.featuretype)
                .then(json => this.setState(() => ({options: json, isLoading: false})))
                .catch((e) => {
                    if (e.message !== "cancelled") {
                        this.setState(() => ({isLoading: false}));
                    }
                });
        }
    }
    _renderMenuItemChildren = (option) => {
        return (
            <div key={option[this.props.keyName]}>
                <span>{option[this.props.labelKey]}</span>
            </div>
        );
    }
    _handleSpeciesChange = (species) => {
        if (species.length > 0) {
            this.props.onChange(species[0]);
            this.setState(() => ({full: false}));
        }else if (this.props.selectedSpecies) {
            this.props.onChange();
            this.setState(() => ({full: false}));
        }
    }
    enterFull = () => {
        if (isMobile.any) {
            this.setState(() => ({full: true}));
        }
    }
    exitFull = (e) => {
        if (this.state.full && e.target.className && e.target.className === 'spec-selector-full') {
            this.setState(() => ({full: false}));
        }
    }
}

module.exports = SpeciesSelector;
