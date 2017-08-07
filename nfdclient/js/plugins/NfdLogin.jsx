/*
 * Copyright 2016, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');
const assign = require('object-assign');
const {UserDetails, UserMenu, Login, LoginNav } = require('./login/index');

require('../../MapStore2/web/client/plugins/login/login.css');
/**
  * Login Plugin. Allow to login/logout or show user info and reset password tools
  * @class Login
  * @memberof plugins
  * @static
  *
  * @prop {string} cfg.id identifier of the Plugin, by default `"mapstore-login-menu"`
  * @prop {object} cfg.menuStyle inline style for the menu, by defualt:
  * ```
  * menuStyle: {
  *      zIndex: 30
  * }
  *```
  */
const LoginTool = React.createClass({
    propTypes: {
        id: React.PropTypes.string,
        menuStyle: React.PropTypes.object
    },
    getDefaultProps() {
        return {
            id: "mapstore-login-menu",
            menuStyle: {
                zIndex: 30
            }
        };
    },
    render() {
        return (<div id={this.props.id}>
            <div style={this.props.menuStyle}>
                <UserMenu />
            </div>
            <UserDetails />
            <Login />
        </div>);
    }
});
module.exports = {
    NfdLoginPlugin: assign(LoginTool, {
        OmniBar: {
            name: "login",
            position: 3,
            tool: LoginNav,
            tools: [UserDetails, Login],
            priority: 1
        }
    }),
    reducers: {security: require('../reducers/security')}
};
