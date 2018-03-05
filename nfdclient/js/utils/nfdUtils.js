/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const baseUrl = '../../assets/img/';
const baseStyle = {
        iconSize: [24, 24],
        iconAnchor: [12, 12]
};
module.exports = {
    getSubCatByCat: (cat) => {
        switch (cat) {
            case 'plant':
                return 'co';
            case 'fungus':
                return 'fu';
            case 'slimemold':
                return 'sl';
            case 'animal':
                return 'ln';
            case 'naturalarea':
                return 'na';
            default:
                return false;
        }
    },

    getIcon: (ftType) => {
        switch (ftType) {
            case 'plant':
                return {html: {...baseStyle, className: "marker-plant-h"}};
            case 'animal':
                return {html: {...baseStyle, className: "marker-animal-h"}};
            case 'fungus':
                return {html: {...baseStyle, className: "marker-fungus-h"}};
            case 'slimemold':
                return {html: {...baseStyle, className: "marker-slimemold-h"}};
            case 'naturalarea':
                return {html: {...baseStyle, className: "marker-naturalarea-h"}};
            default:
                return `${baseUrl}marker-icon-green-highlight.png`;
        }
    },
    getPrettyFeatureType(ft) {
        switch (ft) {
            case 'plant':
                return 'Plant';
            case 'animal':
                return 'Animal';
            case 'fungus':
                return 'Fungus';
            case 'slimemold':
                return 'Slime/Mold';
            case 'naturalarea':
                return 'Natural area';
            default:
                return '';
        }
    },
    getPrettyFeatureSubType(fst) {
        switch (fst) {
            case 'co':
                return 'Conifer';
            case 'fe':
                return 'Fern';
            case 'fl':
                return 'Flowering plant';
            case 'pl':
                return 'Plant generic';
            case 'mo':
                return 'Moss';
            case 'ln':
                return 'Land animal';
            case 'lk':
                return 'Pond Lake animal';
            case 'st':
                return 'Stream animal';
            case 'we':
                return 'Wetland animal';
            default:
                return '';
        }
    },
    isWriter(user = {}, ft) {
        return !!user[`${ft}_writer`];
    },
    isPublisher(user = {}, ft) {
        return !!user[`${ft}_publisher`];
    },
    isLoading(loding = {}) {
        return Object.keys(loding).reduce((l, k) => l ? l : loding[k], false);
    },
    getFormIcon(formname) {
        let icon = 'question-sign';
        if (formname.toLowerCase() === 'species') {
            icon = 'pen';
        } else if (formname.toLowerCase() === 'taxon_status') {
            icon = 'star';
        } else if (formname.toLowerCase() === 'details') {
            icon = 'th-list';
        } else if (formname.toLowerCase() === 'details.lifestages') {
            icon = 'refresh';
        } else if (formname.toLowerCase() === 'management') {
            icon = 'cog';
        } else if (formname.toLowerCase() === 'observation') {
            icon = 'eye-open';
        } else if (formname.toLowerCase() === 'observation.reporter') {
            icon = 'reporter';
        } else if (formname.toLowerCase() === 'observation.recorder') {
            icon = 'recorder';
        } else if (formname.toLowerCase() === 'observation.verifier') {
            icon = 'verifier';
        } else if (formname.toLowerCase() === 'voucher') {
            icon = 'tag';
        } else if (formname.toLowerCase() === 'location') {
            icon = 'uniE062';
        } else if (formname.toLowerCase() === 'details.vegetation') {
            icon = 'uniE103';
        } else if (formname.toLowerCase() === 'details.substrate') {
            icon = 'uniE135';
        } else if (formname.toLowerCase().includes('earthworm')) {
            icon = 'uniE232';
        } else if (formname.toLowerCase().includes('disturbance')) {
            icon = 'uniE162';
        } else if (formname.toLowerCase().includes('association')) {
            icon = 'uni4C';
        } else if (formname.toLowerCase().includes('fruit')) {
            icon = 'uniF8FF';
        }
        return icon;
    }
};
