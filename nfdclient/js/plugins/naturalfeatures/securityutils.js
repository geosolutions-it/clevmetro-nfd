/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const isWriter = (state) => {
    if (state.security.user) {
        if (state.naturalfeatures.featuretype === 'animal') {
            return state.security.user.animal_writer;
        }
        if (state.naturalfeatures.featuretype === 'plant') {
            return state.security.user.plant_writer;
        }
        if (state.naturalfeatures.featuretype === 'slimemold') {
            return state.security.user.slimemold_writer;
        }
        if (state.naturalfeatures.featuretype === 'fungus') {
            return state.security.user.fungus_writer;
        }
        if (state.naturalfeatures.featuretype === 'naturalarea') {
            return state.security.user.naturalarea_writer;
        }
    }
    return false;
};

const isPublisher = (state) => {
    if (state.security.user) {
        if (state.naturalfeatures.featuretype === 'animal') {
            return state.security.user.animal_publisher;
        }
        if (state.naturalfeatures.featuretype === 'plant') {
            return state.security.user.plant_publisher;
        }
        if (state.naturalfeatures.featuretype === 'slimemold') {
            return state.security.user.slimemold_publisher;
        }
        if (state.naturalfeatures.featuretype === 'fungus') {
            return state.security.user.fungus_publisher;
        }
        if (state.naturalfeatures.featuretype === 'naturalarea') {
            return state.security.user.naturalarea_publisher;
        }
    }
    return false;
};

module.exports = {
    isWriter,
    isPublisher
};
