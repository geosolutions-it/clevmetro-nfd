/*
 * Copyright 2018, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');
const PropTypes = require('prop-types');
const assign = require('object-assign');
const {connect} = require('react-redux');
const {Button, Tooltip, OverlayTrigger} = require('react-bootstrap');
const Message = require('../../MapStore2/web/client/plugins/locale/Message');
const {toggleTutorial} = require('../../MapStore2/web/client/actions/tutorial');

const {TutorialPlugin, reducers, epics} = require('../../MapStore2/web/client/plugins/Tutorial');

class ToggleTutorial extends React.Component {
    static propTypes = {
       onToggle: PropTypes.func,
       active: PropTypes.bool
    };
    static defaultProps = {
        onToggle: () => {},
        active: false
    }


    render() {
        let tooltip = <Tooltip id="toolbar-tutorial-button">{<Message msgId={"tutorial.title"}/>}</Tooltip>;
        return (
        <OverlayTrigger placement="bottom" overlay={tooltip}>
            <Button
                active={this.props.active}
                onClick={this.props.onToggle}
                id="rightpanel-button"
                className="square-button"
                bsStyle="primary"
            >{TutorialPlugin.BurgerMenu.icon}</Button>
        </OverlayTrigger>);
    }
}

module.exports = {
     TutorialPlugin: assign(TutorialPlugin, {
         OmniBar: {
                     name: 'tutorial',
                     position: 6,
                     tool: connect((state)=>({active: state.tutorial.enabled}), {onToggle: toggleTutorial})(ToggleTutorial),
                     priority: 1,
                     tools: [TutorialPlugin]
        }
     }),
     reducers,
     epics
};
