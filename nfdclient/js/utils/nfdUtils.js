/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const baseUrl = '../../assets/img/';
module.exports = {
    getIconUrl: (ftType) => {
        switch (ftType) {
            case 'plant':
                return `${baseUrl}marker-icon-green-highlight.png`;
            case 'animal':
                return `${baseUrl}marker-icon-purple-highlight.png`;
            case 'fungus':
                return `${baseUrl}marker-icon-yellow-highlight.png`;
            case 'slimemold':
                return `${baseUrl}marker-icon-marine-highlight.png`;
            case 'naturalarea':
                return `${baseUrl}marker-icon-blue-highlight.png`;
            default:
                return `${baseUrl}marker-icon-green-highlight.png`;
        }
    }
};
