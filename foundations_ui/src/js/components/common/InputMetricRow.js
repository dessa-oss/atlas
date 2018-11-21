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
      hiddenInputParams: this.props.hiddenInputParams,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({
      hiddenInputParams: nextProps.hiddenInputParams,
    });
  }

  render() {
    const {
      job, cellWidths, isError, isMetric, allInputMetricColumn, hiddenInputParams,
    } = this.state;

    const cells = CommonActions.getInputMetricCells(job,
      cellWidths,
      isError,
      isMetric,
      allInputMetricColumn,
      hiddenInputParams);

    return (
      <div className="job-table-row">
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
  hiddenInputParams: PropTypes.array,
};

InputMetricRow.defaultProps = {
  job: {},
  cellWidths: [],
  isError: false,
  isMetric: false,
  allInputMetricColumn: [],
  hiddenInputParams: [],
};

export default InputMetricRow;
