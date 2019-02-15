import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobListActions from '../../../actions/JobListActions';

class StatusCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      status: this.props.status,
      isError: this.props.isError,
      rowNumber: this.props.rowNumber,
    };
  }

  render() {
    const { status, isError, rowNumber } = this.state;

    const statusClass = JobListActions.getStatusCircle(status);

    const divClass = isError ? `status-cell job-cell error row-${rowNumber}` : `status-cell job-cell row-${rowNumber}`;

    return (
      <div className={divClass}>
        <span className={statusClass} />
      </div>
    );
  }
}

StatusCell.propTypes = {
  status: PropTypes.string,
  isError: PropTypes.bool,
  rowNumber: PropTypes.number,
};

StatusCell.defaultProps = {
  status: '',
  isError: false,
  rowNumber: 0,
};

export default StatusCell;
