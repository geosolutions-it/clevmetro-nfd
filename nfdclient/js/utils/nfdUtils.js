/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const baseUrl = '../../assets/img/';
const baseStyle = {
        iconSize: [30, 30],
        iconAnchor: [15, 15]
};
module.exports = {
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
        if (formname === 'species') {
            icon = 'question-sign';
        } else if (formname === 'species.element_species') {
            icon = 'star';
        } else if (formname === 'details') {
            icon = 'th-list';
        } else if (formname === 'details.lifestages') {
            icon = 'refresh';
        } else if (formname === 'occurrencemanagement') {
            icon = 'cog';
        } else if (formname === 'observation') {
            icon = 'eye-open';
        } else if (formname === 'observation.reporter') {
            icon = 'reporter';
        } else if (formname === 'observation.recorder') {
            icon = 'recorder';
        } else if (formname === 'observation.verifier') {
            icon = 'verifier';
        } else if (formname === 'voucher') {
            icon = 'tag';
        } else if (formname === 'location') {
            icon = 'uniE062';
        } else if (formname === 'details.vegetation') {
            icon = 'uniE103';
        } else if (formname === 'details.substrate') {
            icon = 'uniE135';
        } else if (formname.includes('earthworm')) {
            icon = 'uniE232';
        } else if (formname.includes('disturbance')) {
            icon = 'uniE162';
        } else if (formname.includes('association')) {
            icon = 'uni4C';
        } else if (formname.includes('fruit')) {
            icon = 'uniF8FF';
        }
        return icon;
    }
};
