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
      onSearch: PropTypes.func,
      paginate: PropTypes.bool,
      clearBtn: PropTypes.bool
    };
    static defaultProps = {
        onSearch: () => {},
        onChange: () => {},
        paginate: true,
        clearBtn: false,
        bsSize: 'small',
        maxResults: 5,
        placeholder: "Search for a species..."
    }
    constructor(props) {
        super(props);
        this.state = {full: false};
    }
    shouldComponentUpdate({options, selectedSpecies}, {full}) {
        return this.state.full !== full || options !== this.props.options || selectedSpecies !== this.props.selectedSpecies;
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
        const {options, selectedSpecies, maxResults, bsSize, placeholder, paginate, clearBtn} = this.props;
        return (
            <div className={this.state.full ? 'spec-selector-full' : ''} onClick={this.exitFull}>
                <AsyncTypeahead
                    clearButton={clearBtn}
                    onFocus={this.enterFull}
                    paginate={paginate}
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
                />
            </div>);
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
