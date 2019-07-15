import React, { Component } from 'react';
import PropTypes from 'prop-types';
import CommonActions from '../../actions/CommonActions';

class InputMetricRow extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isError: this.props.isError,
      job: this.props.job,
      isMetric: this.props.isMetric,
      allInputMetricColumn: this.props.allInputMetricColumn,
      hiddenInputParams: this.props.hiddenInputParams,
      rowNumber: this.props.rowNumber,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({
      isError: nextProps.isError,
      job: nextProps.job,
      isMetric: nextProps.isMetric,
      allInputMetricColumn: nextProps.allInputMetricColumn,
      hiddenInputParams: nextProps.hiddenInputParams,
      rowNumber: nextProps.rowNumber,
    });
  }

  render() {
    const {
      job, isError, isMetric, allInputMetricColumn, hiddenInputParams, rowNumber,
    } = this.state;

    const cells = CommonActions.getInputMetricCells(job,
      isError,
      isMetric,
      allInputMetricColumn,
      hiddenInputParams,
      rowNumber);

    return (
      <div className="job-table-row">
        {cells}
      </div>
    );
  }
}

InputMetricRow.propTypes = {
  job: PropTypes.object,
  isError: PropTypes.bool,
  isMetric: PropTypes.bool,
  allInputMetricColumn: PropTypes.array,
  hiddenInputParams: PropTypes.array,
  rowNumber: PropTypes.number,
};

InputMetricRow.defaultProps = {
  job: {},
  isError: false,
  isMetric: false,
  allInputMetricColumn: [],
  hiddenInputParams: [],
  rowNumber: 0,
};

export default InputMetricRow;
