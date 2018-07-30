
/*
 * Copyright 2018, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');
const Message = require('../../../MapStore2/web/client/components/I18N/Message');
const Select = require('react-select');
const {Form, FormGroup, FormControl} = require('react-bootstrap');
const {DateTimePicker} = require('react-widgets');
const {isString} = require('lodash');
const moment = require('moment');

module.exports = ({
    name,
    type,
    loading,
    options,
    desc,
    code,
    onChange = () => {},
    reportOptions,
    disabled,
    placeholder = {
        multiselect: 'Select values',
        select: 'Select value',
        text: 'Insert value',
        number: 'Insert number',
        date: 'Select date'
    },
    optionsFilter
}) => (
    <div>
        {desc && <div style={{fontSize: 11}}><i><Message msgId={'clevmetro.' + desc}/></i></div>}
        {(type === 'multiselect' || type === 'select') && <Select
            options={options && options.filter(optionsFilter ? optionsFilter : () => true).map(option => ({
                value: isString(option) ? option : option.code,
                label: isString(option) ? option : option.name
            }))}
            name={name}
            disabled={disabled || loading || !options}
            multi={type === 'multiselect'}
            simpleValue
            value={reportOptions[code]}
            isLoading={loading}
            placeholder={placeholder[type]}
            onChange={(value) => { onChange({[code]: value}); }}
            simpleValue/>}
        {type === 'text' && <Form>
            <FormGroup controlId={(name || desc) + ':text'}>
                <FormControl
                    type="text"
                    disabled={disabled}
                    placeholder={placeholder[type]}
                    value={reportOptions[code]}
                    onChange={event => {
                        const value = event && event.target && event.target.value;
                        onChange({[code]: value});
                    }}/>
            </FormGroup>
        </Form>}

        {type === 'number' && <Form>
            <FormGroup controlId={(name || desc) + ':number'}>
                <FormControl
                    type="number"
                    disabled={disabled}
                    value={reportOptions[code]}
                    placeholder={placeholder[type]}
                    onChange={event => {
                        const value = event && event.target && event.target.value;
                        onChange({[code]: value});
                    }}/>
            </FormGroup>
        </Form>}

        {type === 'date' && <Form>
            {code[0] && <div><Message msgId={'clevmetro.' + code[0]} /></div> }
            {code[0] && <DateTimePicker
                disabled={disabled}
                value={reportOptions[code]}
                placeholder={placeholder[type]}
                time={false}
                onChange={date => onChange({[code[0]]: date && moment(date).format('YYYY-MM-DD') || date})}/>}
            {code[1] && <div><Message msgId={'clevmetro.' + code[1]} /></div> }
            {code[1] && <DateTimePicker
                value={reportOptions[code]}
                disabled={disabled}
                placeholder={placeholder[type]}
                time={false}
                onChange={date => onChange({[code[1]]: date && moment(date).format('YYYY-MM-DD') || date})}/>}
        </Form>}
    </div>
);
