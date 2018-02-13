/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/

module.exports = {
    animal: require('./Category')('animal'),
    plant: require('./Category')('plant'),
    slimemold: require('./Category')('slimemold'),
    fungus: require('./Category')('fungus'),
    naturalarea: require('./NaturalArea')
};
