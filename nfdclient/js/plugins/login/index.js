/**
* Copyright 2016, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/
const React = require('react');
const {connect} = require('../../../MapStore2/web/client/utils/PluginsUtils');
const {userLoginSubmit, nfdLogout} = require('../../actions/naturalfeatures');
const {loginFail, logoutWithReload} = require('../../../MapStore2/web/client/actions/security');
const {setControlProperty} = require('../../../MapStore2/web/client/actions/controls');
const {Glyphicon, Tooltip, OverlayTrigger} = require('react-bootstrap');
const Message = require('../../../MapStore2/web/client/components/I18N/Message');


const UserMenu = connect((state) => ({
    user: state.security && state.security.user
}), {
    onShowLogin: setControlProperty.bind(null, "LoginForm", "enabled", true, true),
    onShowAccountInfo: setControlProperty.bind(null, "AccountInfo", "enabled", true, true),
    onShowChangePassword: setControlProperty.bind(null, "ResetPassword", "enabled", false),
    onLogout: logoutWithReload
})(require('../../../MapStore2/web/client/components/security/UserMenu'));

const UserDetails = connect((state) => ({
    user: state.security && state.security.user,
    show: state.controls.AccountInfo && state.controls.AccountInfo.enabled}
), {
    onClose: setControlProperty.bind(null, "AccountInfo", "enabled", false, false)
})(require('../../../MapStore2/web/client/components/security/modals/UserDetailsModal'));

const Login = connect((state) => ({
    show: state.controls.LoginForm && state.controls.LoginForm.enabled,
    user: state.security && state.security.user,
    loginError: state.security && state.security.loginError,
    includeCloseButton: false,
    options: {id: "login-dialog"}
}), {
    onLoginSuccess: setControlProperty.bind(null, 'LoginForm', 'enabled', false, false),
    onSubmit: userLoginSubmit,
    onError: loginFail
})(require('../../../MapStore2/web/client/components/security/modals/LoginModal'));

const LoginNav = connect((state) => ({
    showPasswordChange: false,
    user: state.security && state.security.user,
    nav: false,
    renderButtonText: false,
    renderButtonContent: () => {
        let tooltip = <Tooltip id="toolbar-tutorial-button">{<Message msgId={"clevmetro.tooltip.login"}/>}</Tooltip>;
        return (<OverlayTrigger placement="bottom" overlay={tooltip}>
            <Glyphicon glyph="user" />
        </OverlayTrigger>);
    },
    bsStyle: "primary",
    className: "square-button"
}), {
    onShowLogin: setControlProperty.bind(null, "LoginForm", "enabled", true, true),
    onShowAccountInfo: setControlProperty.bind(null, "AccountInfo", "enabled", true, true),
    onShowChangePassword: setControlProperty.bind(null, "ResetPassword", "enabled", false),
    onLogout: nfdLogout
})(require('../../../MapStore2/web/client/components/security/UserMenu'));

module.exports = {
    UserDetails,
    UserMenu,
    Login,
    LoginNav
};
