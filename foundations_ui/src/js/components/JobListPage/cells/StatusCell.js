import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobActions from '../../../actions/JobListActions';

class StatusCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      status: this.props.status,
      isError: this.props.isError,
    };
  }

  render() {
    const { status, isError } = this.state;

    const statusClass = JobActions.getStatusCircle(status);

    const divClass = isError ? 'status-cell status-container error' : 'status-cell status-container';

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
};

StatusCell.defaultProps = {
  status: '',
  isError: false,
};

export default StatusCell;
