import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobListActions from '../../../actions/JobListActions';

class DurationCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      days: JobListActions.getDurationDays(this.props.duration),
      hours: JobListActions.getDurationHours(this.props.duration),
      minutes: JobListActions.getDurationMinutes(this.props.duration),
      seconds: JobListActions.getDurationSeconds(this.props.duration),
      isError: this.props.isError,
      rowNumber: this.props.rowNumber,
    };
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.rowNumber !== this.props.duration) {
      this.setState({
        days: JobListActions.getDurationDays(nextProps.duration),
        hours: JobListActions.getDurationHours(nextProps.duration),
        minutes: JobListActions.getDurationMinutes(nextProps.duration),
        seconds: JobListActions.getDurationSeconds(nextProps.duration),
        isError: nextProps.isError,
        rowNumber: nextProps.rowNumber,
      });
    }
  }

  render() {
    const {
      days, hours, minutes, seconds, isError, rowNumber,
    } = this.state;

    let daysUI = null;
    let hoursUI = null;
    let minutesUI = null;
    let secondsUI = null;

    daysUI = JobListActions.getDurationClass('days', days, hours, minutes, seconds, isError);
    hoursUI = JobListActions.getDurationClass('hours', days, hours, minutes, seconds, isError);
    minutesUI = JobListActions.getDurationClass('minutes', days, hours, minutes, seconds, isError);
    secondsUI = JobListActions.getDurationClass('seconds', days, hours, minutes, seconds, isError);

    const pClass = isError
      ? 'error'
      : '';

    return (
      <span className={pClass}>{daysUI}{hoursUI}{minutesUI}{secondsUI}</span>
    );
  }
}

DurationCell.propTypes = {
  duration: PropTypes.number,
  isError: PropTypes.bool,
  rowNumber: PropTypes.number,
  days: PropTypes.string,
  hours: PropTypes.string,
  minutes: PropTypes.string,
  seconds: PropTypes.string,
};

DurationCell.defaultProps = {
  duration: null,
  isError: false,
  rowNumber: 0,
  days: '',
  hours: '',
  minutes: '',
  seconds: '',
};

export default DurationCell;
