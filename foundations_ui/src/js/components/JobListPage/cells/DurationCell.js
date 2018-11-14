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
    };
  }

  render() {
    const {
      days, hours, minutes, seconds,
    } = this.state;

    let daysUI = null;
    let hoursUI = null;
    let minutesUI = null;
    let secondsUI = null;

    daysUI = JobActions.getDurationClass('days', days, hours, minutes, seconds);
    hoursUI = JobActions.getDurationClass('hours', days, hours, minutes, seconds);
    minutesUI = JobActions.getDurationClass('minutes', days, hours, minutes, seconds);
    secondsUI = JobActions.getDurationClass('seconds', days, hours, minutes, seconds);

    return (
      <p className="job-cell duration-cell">{daysUI}{hoursUI}{minutesUI}{secondsUI}</p>
    );
  }
}

DurationCell.propTypes = {
  duration: PropTypes.number,
};

DurationCell.defaultProps = {
  duration: null,
};

export default DurationCell;
