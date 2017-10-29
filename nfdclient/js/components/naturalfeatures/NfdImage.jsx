/**
 * Copyright 2016, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');
const PropTypes = require('prop-types');
const Dropzone = require('react-dropzone').default;
const Message = require('../../../MapStore2/web/client/components/I18N/Message');

const ImageCard = require('./ImageCard');
  /**
   * A Dropzone area for a img.
   */
const MB = 1048576;
const KB = 1024;
class NfdImage extends React.Component {
    static propTypes= {
        height: PropTypes.number,
        images: PropTypes.array,
        disabled: PropTypes.bool,
        glyphiconRemove: PropTypes.string,
        // CALLBACKS
        onError: PropTypes.func,
        addImage: PropTypes.func,
        removeImage: PropTypes.func,
        isMobile: PropTypes.bool,
        // I18N
        message: PropTypes.oneOfType([PropTypes.string, PropTypes.element]),
        fileSize: PropTypes.number
    };
    static contextTypes= {
        messages: PropTypes.object
    };
    static defaultProps = {
        height: 400,
        isMobile: false,
        images: [],
        fileSize: 5242880, // in Byte
        glyphiconRemove: "remove-circle",
        disabled: false,
        onError: () => {},
        addImage: () => {},
        removeImage: () => {},
        // I18N
        message: <Message msgId="map.message"/>
    }
    onRemoveImage = (idx) => {
        this.props.removeImage(idx);
    }
    onDropAccepted = ([image]) => {
        if (image) {
            this.getDataUri(image, (data) => {
                this.props.addImage({dataUrl: data, name: image.name, type: image.type});
            });
        }
    }
    onDropRejected = ([file]) => {
        const errors = [];
        // destroy preview
        if (!this.isImage(file)) {
            errors.push("FORMAT");
        }
        if (file.size > this.props.fileSize / KB) {
            errors.push("SIZE");
        }
        this.props.onError(errors);
    }
    getDataUri(image, callback) {
        if (image) {
            let fileReader = new FileReader();
            fileReader.onload = (event) => (callback(event.target.result));
            return fileReader.readAsDataURL(image);
        }
        return callback(null);
    }
    render() {
        const isUploading = this.props.images.filter((i) => i.loading).length > 0;
        const suggestion = `Max file size ${this.props.fileSize / MB} MB`;
        return (
            <div className={`nfd-images ${this.props.isMobile ? 'nfd-images-mobile' : ''} ${this.props.disabled ? 'disabled' : ''}`} style={{height: this.props.height}}>
                <Dropzone disabled={this.props.disabled || isUploading} multiple={false} className="dropzone alert alert-info" rejectClassName="alert-danger" onDropAccepted={this.onDropAccepted} onDropRejected={this.onDropRejected}accept="image/jpeg, image/png, image/jpg" disablePreview={true}>
                    <div className="dropzone-content-image">{this.props.message}<br/>{suggestion}</div>
                </Dropzone>
                <div className="nfd-thumbnails-container" style={{height: this.props.height - 100 }}>
                    {this.props.images.map( (img, idx) => (<ImageCard disabled={this.props.disabled || isUploading} key={idx} image={img} onRemove={this.onRemoveImage} id={idx}/>))}
                </div>
            </div>);
    }
    isImage = (image) => {
        return image.type === "image/png" || image.type === "image/jpeg" || image.type === "image/jpg";
    }
}

module.exports = NfdImage;
