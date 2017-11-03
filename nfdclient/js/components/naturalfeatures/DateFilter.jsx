/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/

const React = require('react');
const PropTypes = require('prop-types');

const DateFiled = require('../../ms2Override/DateTimeField');
const ComboField = require('../../../MapStore2/web/client/components/data/query/ComboField');

class DateFilter extends React.Component {
        static propTypes = {
          rowId: PropTypes.number,
          operator: PropTypes.string,
          fieldValue: PropTypes.object,
          operatorOptions: React.PropTypes.array,
          updateFieldValue: PropTypes.func
        }
        static defaultProps = {
          operatorOptions: [">", "<", "><"],
          rowId: 1,
          operator: '=',
          updateFieldValue: () => {}
        }
        render() {
            const {operatorOptions, rowId, operator, fieldValue} = this.props;
            return (
                <div className="container-fluid">
                    <div className="row">
                        <div className="col-xs-5" style={{paddingLeft: 0}} >
                        <label>Operator</label>
                        <ComboField
                            placeholder=""
                            fieldOptions= {operatorOptions}
                            fieldName="operator"
                            fieldRowId={rowId}
                            fieldValue={operator}
                            onUpdateField={this.update}/>
                        </div>
                    </div>
                    <div className="row">
                        <DateFiled
                        fieldName="includevalue"
                        fieldRowId={rowId}
                        fieldValue={fieldValue}
                        onUpdateField={this.update} operator={operator}/>
                    </div>
                </div>
            );
        }
        update = (rowId, filedName, value) => {
            this.props.updateFieldValue(filedName, value);
            if (filedName === 'operator' && this.props.fieldValue) {
                this.props.updateFieldValue('includevalue');
            }
        }
}

module.exports = DateFilter;
