const React = require('react');
const PropTypes = require('prop-types');
const isMobile = require('ismobilejs');
const Select = require('react-select');
require('react-select/dist/react-select.css');


class SelectFilter extends React.Component {

    static propTypes = {
        labelKey: PropTypes.string,
        valueKey: React.PropTypes.string,
        disabled: React.PropTypes.bool,
        placeholder: React.PropTypes.string,
        options: React.PropTypes.array,
        onChange: PropTypes.func,
        value: React.PropTypes.any
    }
    static defaultProps = {
        onChange: () => {},
        labelKey: "label",
        valueKey: "key",
        disabled: false,
        options: [],
        placeholder: "Select ..."
    }
    constructor(props) {
        super(props);
        this.state = {full: false};
    }
    render() {
        return (
            <div className={this.state.full ? 'spec-selector-full' : ''} onClick={this.exitFull}>
                <Select
                    searchable={false}
                    multi={false}
                    onFocus={this.enterFull}
                    className="nf-select"
                    labelKey={this.props.labelKey}
                    valueKey={this.props.valueKey}
                    disabled={this.props.disabled}
                    value={this.props.value}
                    onChange={this.handelChange}
                    options={this.props.options}
                    placeholder={this.props.placeholder}
                       />
            </div>);
    }
    handelChange = (val) => {
        if (this.state.full) {
            this.setState(() => ({full: false}));
        }
        this.props.onChange(val);
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

module.exports = SelectFilter;
