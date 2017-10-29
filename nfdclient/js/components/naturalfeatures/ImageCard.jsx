/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/
const React = require('react');
const PropTypes = require('prop-types');
const {Glyphicon} = require('react-bootstrap');
const Spinner = require('react-spinkit');

class ImageCard extends React.Component {
    static propTypes = {
      onRemove: PropTypes.func,
      image: PropTypes.object,
      glyphiconRemove: PropTypes.string,
      disabled: PropTypes.bool,
      id: PropTypes.oneOfType([PropTypes.number, PropTypes.string]).isRequired
    };
    static defaultProps = {
      onRemove: () => {},
      disabled: false,
      glyphiconRemove: "remove-circle"
    }
    state = {
        showImage: false
    }
    onRemove = () => {
        if (!this.props.disabled) {
            this.props.onRemove(this.props.id);
        }
    }
    getThumbOrImageUrl = (image, thumb = true) => {
        // Changes thumb and image when thumb's path will be fixe on server
        return image && (thumb && image.thumbnail || image.image);
    }
    getThumbnailUrl = (image, thumb = true) => {
        const img = image.dataUrl ? image.dataUrl : this.getThumbOrImageUrl(image, thumb);
        return img ? decodeURIComponent(img) : null;
    }
    renderLoading() {
        return (<div className="img-loading-spinner"><Spinner spinnerName="circle" noFadeIn overrideSpinnerClassName="spinner"/></div>);
    }
    render() {
        const {loading} = this.props.image;
        const imgStyle = loading ? {} : {backgroundImage: `url(${this.getThumbnailUrl(this.props.image)})`};
        return this.state.showImage ? (<div onClick={() => {this.setState({showImage: false}); }} className="fade in modal" style={{ background: "rgba(255,255,255,1)", display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
                <img src={this.getThumbnailUrl(this.props.image, false)} style={{maxWidth: '95%', maxHeight: '95%'}}/>
            </div>) : (
            <div className="img-card">
                <div className="nfd-image" style={imgStyle} onClick={() => this.setState({showImage: true})}/>
                {loading ? this.renderLoading() : (
                <div className={`image-remove ${this.props.disabled ? 'disabled' : ''}`} onClick={this.onRemove}>
                    <Glyphicon glyph={this.props.glyphiconRemove} />
                </div>)}
        </div>);
    }
}

module.exports = ImageCard;
