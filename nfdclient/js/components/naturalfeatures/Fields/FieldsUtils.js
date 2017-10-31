/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/

module.exports = {
    getLabel(item) {
        return `${item.mandatory ? '* ' : ''}${item.label}`;
    },
    getValue(feature = {}, key, defaultValue = '') {
        return feature && feature[key] || defaultValue;
    }
};
