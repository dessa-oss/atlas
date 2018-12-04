import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobActions from '../../../actions/JobListActions';

class StartTimeCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      date: JobActions.getFormatedDate(this.props.startTime),
      time: JobActions.getFormatedTime(this.props.startTime),
      isError: this.props.isError,
    };
  }

  render() {
    const { date, time, isError } = this.state;

    const errorClass = isError ? 'error' : '';
    const pClass = 'job-cell font-bold start-cell '.concat(errorClass);
    const spanClass = ''.concat(errorClass);

    return (
      <p className={pClass}>{date} <span className={spanClass}>{time}</span></p>
    );
  }
}

StartTimeCell.propTypes = {
  startTime: PropTypes.string,
  isError: PropTypes.bool,
};

StartTimeCell.defaultProps = {
  startTime: '',
  isError: false,
};

export default StartTimeCell;
