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

    let showingDays = false;
    let showingHours = false;
    let showingMinutes = false;

    if (days !== 0) {
      showingDays = true;
      daysUI = <span className="duration-day-number header-4 font-bold">{days}<span className="font-regular">d </span></span>;
    }

    if (hours !== 0) {
      showingHours = true;
      hoursUI = <span className="duration-hour-number header-4 font-bold">{hours}<span className="font-regular">h </span></span>;
    } else if (showingDays) {
      hoursUI = <span className="duration-hour-number header-4 font-bold">0<span className="font-regular">h </span></span>;
    }

    if (minutes !== 0) {
      showingMinutes = true;
      minutesUI = <span className="duration-minute-number header-4 font-bold">{minutes}<span className="font-regular">m </span></span>;
    } else if (showingDays || showingHours) {
      minutesUI = <span className="duration-minute-number header-4 font-bold">0<span className="font-regular">m </span></span>;
    }

    if (seconds !== 0) {
      secondsUI = <span className="duration-second-number header-4 font-bold">{seconds}<span className="font-regular">s</span></span>;
    } else if (showingDays || showingHours || showingMinutes) {
      secondsUI = <span className="duration-second-number header-4 font-bold">0<span className="font-regular">s </span></span>;
    }

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
