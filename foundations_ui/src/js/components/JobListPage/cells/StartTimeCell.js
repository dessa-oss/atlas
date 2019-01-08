import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobActions from '../../../actions/JobListActions';
import CommonActions from '../../../actions/CommonActions';

class StartTimeCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      date: JobActions.getFormatedDate(this.props.startTime),
      time: JobActions.getFormatedTime(this.props.startTime),
      isError: this.props.isError,
      rowNumber: this.props.rowNumber,
    };
  }

  render() {
    const {
      date, time, isError, rowNumber,
    } = this.state;

    const errorClass = CommonActions.errorStatus(isError);
    const pClass = `job-cell font-bold start-cell ${errorClass} row-${rowNumber}`;
    const spanClass = ''.concat(errorClass);

    return (
      <p className={pClass}>{date} <span className={spanClass}>{time}</span></p>
    );
  }
}

StartTimeCell.propTypes = {
  startTime: PropTypes.string,
  isError: PropTypes.bool,
  rowNumber: PropTypes.number,
};

StartTimeCell.defaultProps = {
  startTime: '',
  isError: false,
  rowNumber: 0,
};

export default StartTimeCell;
