import React, { Component } from 'react';
import PropTypes from 'prop-types';
import HoverCell from './HoverCell';
import JobListActions from '../../../actions/JobListActions';
import CommonActions from '../../../actions/CommonActions';


class StartTimeCell extends Component {
  constructor(props) {
    super(props);
    this.toggleExpand = this.toggleExpand.bind(this);
    this.state = {
      date: JobListActions.getFormatedDate(this.props.startTime),
      time: JobListActions.getFormatedTime(this.props.startTime),
      isError: this.props.isError,
      rowNumber: this.props.rowNumber,
      expand: false,
    };
  }

  toggleExpand(value) {
    this.setState({ expand: value });
  }

  render() {
    const {
      date, time, isError, rowNumber, expand,
    } = this.state;

    let hover;

    const errorClass = CommonActions.errorStatus(isError);
    const spanClass = ''.concat(errorClass);

    const pClass = isError
      ? `job-cell start-cell error row-${rowNumber}`
      : `job-cell start-cell row-${rowNumber}`;

    const dateTimeFormatted = (
      <p className="font-bold">
        <div className="launch-date">{date}</div>
        <span className={spanClass}>{time}</span>
      </p>
    );

    if (expand) {
      hover = <HoverCell textToRender={dateTimeFormatted} />;
    }

    return (
      <div
        className={pClass}
        onMouseEnter={() => this.toggleExpand(true)}
        onMouseLeave={() => this.toggleExpand(false)}
      >
        {dateTimeFormatted}
        <div>
          {hover}
        </div>
      </div>

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
