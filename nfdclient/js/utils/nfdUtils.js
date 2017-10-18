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
                return 'Plant';
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
                return 'Natural area';
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
    }
};
