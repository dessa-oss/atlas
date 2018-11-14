import React, { Component } from 'react';
import PropTypes from 'prop-types';
import InputMetricCell from './InputMetricCell';

class InputMetricRow extends Component {
  constructor(props) {
    super(props);
    this.state = {
      job: this.props.job,
      cellWidths: this.props.cellWidths,
    };
  }

  render() {
    const { job, cellWidths } = this.state;

    let cells = null;
    if (job.input_params && job.input_params.length > 0) {
      cells = [];
      let colIndex = 0;
      job.input_params.forEach((input) => {
        const cellWidth = cellWidths[colIndex];
        cells.push(<InputMetricCell key={input.name} cellWidth={cellWidth} />);
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
};

InputMetricRow.defaultProps = {
  job: {},
  cellWidths: [],
};

export default InputMetricRow;
