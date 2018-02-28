/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/

const {isEqual, isEmpty} = require('lodash');

const getTaxon = (taxon) => {
    return `${taxon !== undefined ? `&taxon=${taxon}` : ''}`;
};

const getReservation = (reservation) => {
    return `${reservation !== undefined ? `&reservation=${reservation.key}` : ''}`;
};

const getCmStatus = (status) => {
    return `${status !== undefined ? `&cm_status=${status.key}` : ''}`;
};

const getWatershed = (watershed) => {
    return `${watershed !== undefined ? `&watershed=${watershed.key}` : ''}`;
};

module.exports = {
    equalFilters(a = {}, b = {}) {
        return isEqual(a, b);
    },
    isFilterEmpty(f = {}) {
        return isEmpty(f);
    },
    getFilter({taxon, reservation, watershed, cm_status}) {
        return getTaxon(taxon) + getReservation(reservation) + getWatershed(watershed) + getCmStatus(cm_status);
    }
};
