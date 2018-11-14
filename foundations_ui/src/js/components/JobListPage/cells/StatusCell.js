import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobActions from '../../../actions/JobListActions';

class StatusCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      status: this.props.status,
    };
  }

  render() {
    const { status } = this.state;

    const statusClass = JobActions.getStatusCircle(status);

    return (
      <div className="status-container">
        <span className={statusClass} />
      </div>
    );
  }
}

StatusCell.propTypes = {
  status: PropTypes.string,
};

StatusCell.defaultProps = {
  status: '',
};

export default StatusCell;
