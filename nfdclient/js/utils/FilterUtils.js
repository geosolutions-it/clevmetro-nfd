/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/

/**
 * To add new filter filed, add the filter name in filds array, implemnt the
 * validation function in validator object, add a funciton that build filter
 * string in getFilter
 */
const {isFinite, isBoolean} = require('lodash');
const moment = require('moment');
const fields = ["selectedSpecies", "released", "includevalue"];

const validator = {
    includevalue: function(filters) {
        const {includevalue, operator} = filters;
        const {startDate, endDate} = includevalue || {};
        const start = moment(startDate);
        const end = moment(endDate);
        if (operator === '><' && ((!startDate || !endDate) || (startDate && endDate && end.diff(start) < 0))) {
            return false;
        }else if (!startDate) {
            return false;
        }
        return true;
    },
    selectedSpecies: function({selectedSpecies = {}}) {
        return isFinite(selectedSpecies.id);
    },
    released: function({released}) {
        return isBoolean(released) && released;
    }
};
const getIncludeFilter = (val = {}, operator) => {
    const {startDate, endDate} = val;
    const s = moment(startDate);
    const e = moment(endDate);
    if (operator === '><' && startDate && endDate) {
        return `&min_inclusion_date=${s.format("YYYY-MM-DD")}&max_inclusion_date=${e.format("YYYY-MM-DD")}`;
    }
    if (operator === '>' && startDate) {
        return `&min_inclusion_date=${s.format("YYYY-MM-DD")}`;
    }
    if (operator === '<' && startDate) {
        return `&max_inclusion_date=${s.format("YYYY-MM-DD")}`;
    }
    return '';
};
const getReleasFilter = (released) => {
    return `${released !== undefined ? `&released=${released}` : ''}`;
};
const getSpeciesFilter = (selectedSpecies) => {
    return `${selectedSpecies !== undefined ? `&species=${selectedSpecies.id}` : ''}`;
};
module.exports = {
    isFilterValid(filters) {
        return fields.reduce((valid, f) => valid ? valid : validator[f](filters), false);
    },
    getFilter({released, selectedSpecies, operator, includevalue}) {
        return getIncludeFilter(includevalue, operator) + getReleasFilter(released) + getSpeciesFilter(selectedSpecies);
    }
};
