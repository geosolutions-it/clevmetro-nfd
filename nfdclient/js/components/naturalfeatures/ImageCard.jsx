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
      id: PropTypes.oneOfType([PropTypes.number, PropTypes.string]).isRequired
    };
    static defaultProps = {
      onRemove: () => {},
      glyphiconRemove: "remove-circle"
    }
    onRemove = () => {
        this.props.onRemove(this.props.id);
    }
    getThumbOrImageUrl = (image) => {
        // Changes thumb and image when thumb's path will be fixe on server
        return image && (image.image || image.thumbnail);
    }
    getThumbnailUrl = (image) => {
        const img = image.dataUrl ? image.dataUrl : this.getThumbOrImageUrl(image);
        return img ? decodeURIComponent(img) : null;
    }
    renderLoading() {
        return (<div className="img-loading-spinner"><Spinner spinnerName="circle" noFadeIn overrideSpinnerClassName="spinner"/></div>);
    }
    render() {
        const {loading} = this.props.image;
        const imgStyle = loading ? {} : {backgroundImage: `url(${this.getThumbnailUrl(this.props.image)})`};
        return (
            <div className="img-card">
                <div className="nfd-image" style={imgStyle}/>
                {loading ? this.renderLoading() : (
                <div className="image-remove" onClick={this.onRemove}>
                    <Glyphicon glyph={this.props.glyphiconRemove} />
                </div>)}
        </div>);
    }
}

module.exports = ImageCard;
