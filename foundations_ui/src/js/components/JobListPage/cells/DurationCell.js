import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobActions from '../../../actions/JobListActions';

class DurationCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      days: JobActions.getDurationDays(this.props.duration),
      hours: JobActions.getDurationHours(this.props.duration),
      minutes: JobActions.getDurationMinutes(this.props.duration),
      seconds: JobActions.getDurationSeconds(this.props.duration),
      isError: this.props.isError,
    };
  }

  render() {
    const {
      days, hours, minutes, seconds, isError,
    } = this.state;

    let daysUI = null;
    let hoursUI = null;
    let minutesUI = null;
    let secondsUI = null;

    daysUI = JobActions.getDurationClass('days', days, hours, minutes, seconds, isError);
    hoursUI = JobActions.getDurationClass('hours', days, hours, minutes, seconds, isError);
    minutesUI = JobActions.getDurationClass('minutes', days, hours, minutes, seconds, isError);
    secondsUI = JobActions.getDurationClass('seconds', days, hours, minutes, seconds, isError);

    const pClass = isError ? 'job-cell duration-cell error' : 'job-cell duration-cell';

    return (
      <p className={pClass}>{daysUI}{hoursUI}{minutesUI}{secondsUI}</p>
    );
  }
}

DurationCell.propTypes = {
  duration: PropTypes.number,
  isError: PropTypes.bool,
};

DurationCell.defaultProps = {
  duration: null,
  isError: false,
};

export default DurationCell;
