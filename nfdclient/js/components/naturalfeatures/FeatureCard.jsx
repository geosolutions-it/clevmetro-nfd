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
const moment = require('moment');

const FeatureCard = (props) => {
    const {feature, enableEdit, onEdit, onZoom} = props;
    const p = feature.properties;
    const edit = ()=> {
        if (enableEdit && p.id && onEdit) {
            onEdit(p.id, p);
        }
    };
    const zoom = ()=> {
        if (p.id && onZoom) {
            onZoom(feature);
        }
    };
    const date = moment(p.inclusion_date).format('YYYY-MM-DD hh:mm');
    // TODO a different card for natural features
    return (
      <span className="list-group-item nfd-list-item">
        <span className="feature-title">{p["taxon.name"]}</span>
        <span className="feature-desc" >{`${date} ${p.released ? 'released' : ''}`}</span>
        <span className="list-item-btn" style={{width: 60}} >
            <Glyphicon glyph="zoom-in" onClick={zoom}/>
            <Glyphicon className={enableEdit ? "" : "disabled"} glyph="pencil" onClick={edit}/>
        </span>
      </span>
    );
};

FeatureCard.propTypes = {
    onEdit: PropTypes.func,
    onZoom: PropTypes.func,
    enableEdit: PropTypes.bool,
    feature: PropTypes.object.isRequired
};

module.exports = FeatureCard;
