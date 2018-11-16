import React, { Component } from 'react';
import PropTypes from 'prop-types';
import CommonActions from '../../actions/CommonActions';

class InputMetricRow extends Component {
  constructor(props) {
    super(props);
    this.state = {
      cellWidths: this.props.cellWidths,
      isError: this.props.isError,
      job: this.props.job,
      isMetric: this.props.isMetric,
      allInputMetricColumn: this.props.allInputMetricColumn,
    };
  }

  render() {
    const {
      job, cellWidths, isError, isMetric, allInputMetricColumn,
    } = this.state;

    const cells = CommonActions.getInputMetricCells(job, cellWidths, isError, isMetric, allInputMetricColumn);

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
  isMetric: PropTypes.bool,
  allInputMetricColumn: PropTypes.array,
};

InputMetricRow.defaultProps = {
  job: {},
  cellWidths: [],
  isError: false,
  isMetric: false,
  allInputMetricColumn: [],
};

export default InputMetricRow;
