import React, { Component } from 'react';
import PropTypes from 'prop-types';
import InputMetricCell from './InputMetricCell';
import JobActions from '../../actions/JobListActions';

class InputMetricRow extends Component {
  constructor(props) {
    super(props);
    this.state = {
      inputParams: JobActions.getConstantInputParams(this.props.job.input_params),
      cellWidths: this.props.cellWidths,
      isError: this.props.isError,
    };
  }

  render() {
    const { inputParams, cellWidths, isError } = this.state;

    let cells = null;
    if (inputParams && inputParams.length > 0) {
      cells = [];
      let colIndex = 0;
      inputParams.forEach((input) => {
        const cellWidth = cellWidths[colIndex];
        const inputValue = JobActions.getInputParamValue(input);
        cells.push(<InputMetricCell key={input.name} cellWidth={cellWidth} value={inputValue} isError={isError} />);
        colIndex += 1;
      });
    }

    return (
      <div className="input-metric-rows-container">
        {cells}
      </div>
    );
  }
}

InputMetricRow.propTypes = {
  job: PropTypes.object,
  cellWidths: PropTypes.array,
  isError: PropTypes.bool,
};

InputMetricRow.defaultProps = {
  job: {},
  cellWidths: [],
  isError: false,
};

export default InputMetricRow;
