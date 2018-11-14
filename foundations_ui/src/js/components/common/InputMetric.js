import React, { Component } from 'react';
import PropTypes from 'prop-types';
import TableSectionHeader from './TableSectionHeader';
import JobColumnHeader from './JobColumnHeader';
import InputMetricCell from './InputMetricCell';

class InputMetric extends Component {
  constructor(props) {
    super(props);
    this.resizeCells = this.resizeCells.bind(this);
    this.state = {
      header: this.props.header,
      hiddenInputParams: this.props.hiddenInputParams,
      allInputParams: this.props.allInputParams,
      jobs: {
        input_params: [
          {
            name: 'a_value',
            value: {
              type: 'hyperparameter',
              name: 'value_for_a_value',
            },
            stage_uuid: '00000000-0000-0000-0000-000000000003',
          },
          {
            name: 'b_value',
            value: {
              type: 'constant',
              value: 65,
            },
            stage_uuid: '00000000-0000-0000-0000-000000000004',
          },
          {
            name: 'd_value',
            value: {
              type: 'hyperparameter',
              name: 'value_for_e_value',
            },
            stage_uuid: '00000000-0000-0000-0000-000000000003',
          },
          {
            name: 'e_value',
            value: {
              type: 'constant',
              value: 165,
            },
            stage_uuid: '00000000-0000-0000-0000-000000000004',
          },
          {
            name: 'expiry_time',
            value: {
              type: 'constant',
              value: 3600,
            },
            stage_uuid: '00000000-0000-0000-0000-000000000005',
          },
        ],
      },
      cellWidths: new Array(5),
    };
  }

  resizeCells(colIndex, newWidth) {
    const { cellWidths } = this.state;
    if (cellWidths[colIndex] !== newWidth) {
      cellWidths[colIndex] = newWidth;
      this.forceUpdate();
    }
  }

  render() {
    const {
      header, hiddenInputParams, allInputParams, jobs, cellWidths,
    } = this.state;

    let inputParams = null;
    if (allInputParams.length > 0) {
      let colIndex = 0;
      inputParams = [];
      allInputParams.forEach((input) => {
        const key = input;
        inputParams.push(<JobColumnHeader key={key} title={input} className="inline-block" containerClass="input-metric-column-header" sizeCallback={this.resizeCells} colIndex={colIndex} />);
        colIndex += 1;
      });
    }

    let cells = null;
    if (jobs.input_params && jobs.input_params.length > 0) {
      cells = [];
      let colIndex = 0;
      jobs.input_params.forEach((input) => {
        const cellWidth = cellWidths[colIndex];
        cells.push(<InputMetricCell key={input.name} cellWidth={cellWidth} />);
        colIndex += 1;
      });
    }

    return (
      <div className="input-metric-container">
        <TableSectionHeader header={header} />
        <div className="input-metric-column-header-container">
          {inputParams}
          <div className="input-metric-rows-container">
            {cells}
          </div>
        </div>
      </div>
    );
  }
}

InputMetric.propTypes = {
  header: PropTypes.string,
  hiddenInputParams: PropTypes.array,
  allInputParams: PropTypes.array,
  jobs: PropTypes.object,
  cellWidths: PropTypes.array,
};

InputMetric.defaultProps = {
  header: '',
  hiddenInputParams: [],
  allInputParams: [],
  jobs: {},
  cellWidths: [],
};


export default InputMetric;
