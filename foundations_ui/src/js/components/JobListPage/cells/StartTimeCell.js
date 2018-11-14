import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobActions from '../../../actions/JobListActions';

class StartTimeCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      date: JobActions.getFormatedDate(this.props.startTime),
      time: JobActions.getFormatedTime(this.props.startTime),
    };
  }

  render() {
    const { date, time } = this.state;

    return (
      <p className="job-cell header-4 font-bold">{date} <span className="font-regular">{time}</span></p>
    );
  }
}

StartTimeCell.propTypes = {
  startTime: PropTypes.string,
};

StartTimeCell.defaultProps = {
  startTime: '',
};

export default StartTimeCell;
