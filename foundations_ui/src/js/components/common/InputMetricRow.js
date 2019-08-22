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
      onMetricRowClick: this.props.onMetricRowClick,
      key: this.props.key,
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
      onMetricRowClick: nextProps.onMetricRowClick,
      key: nextProps.key,
    });
  }

  render() {
    const {
      job, isError, isMetric, allInputMetricColumn, hiddenInputParams, rowNumber, key, onMetricRowClick,
    } = this.state;
    const { onClickOpenModalJobDetails } = this.props;
    const cells = CommonActions.getInputMetricCells(job,
      isError,
      isMetric,
      allInputMetricColumn,
      hiddenInputParams,
      rowNumber,
      onClickOpenModalJobDetails);
    return (
      <div
        role="presentation"
        className="job-table-row"
        onClick={() => onMetricRowClick(job, key)}
        onKeyDown={() => onMetricRowClick(job, key)}
      >
        {cells}
      </div>
    );
  }
}

InputMetricRow.propTypes = {
  onMetricRowClick: PropTypes.func,
  key: PropTypes.string,
  job: PropTypes.object,
  isError: PropTypes.bool,
  isMetric: PropTypes.bool,
  allInputMetricColumn: PropTypes.array,
  hiddenInputParams: PropTypes.array,
  rowNumber: PropTypes.number,
  onClickOpenModalJobDetails: PropTypes.func,
};
const defaultFunc = () => console.warn('InputMetricRow: onClick func missing.');
InputMetricRow.defaultProps = {
  onMetricRowClick: defaultFunc,
  key: '',
  job: {},
  isError: false,
  isMetric: false,
  allInputMetricColumn: [],
  hiddenInputParams: [],
  rowNumber: 0,
  onClickOpenModalJobDetails: () => null,
};

export default InputMetricRow;
