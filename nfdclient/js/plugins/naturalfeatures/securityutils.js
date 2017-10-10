/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const isWriter = (state, featureType) => {
    const ft = featureType || state.naturalfeatures.featuretype;
    if (state.security.user) {
        return state.security.user[`${ft}_writer`];
    }
    return false;
};

const isPublisher = (state, featureType) => {
    const ft = featureType || state.naturalfeatures.featuretype;
    if (state.security.user) {
        return state.security.user[`${ft}_publisher`];
    }
    return false;
};

module.exports = {
    isWriter,
    isPublisher
};
