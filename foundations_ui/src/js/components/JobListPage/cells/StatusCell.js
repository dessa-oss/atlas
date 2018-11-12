import React, { Component } from 'react';
import PropTypes from 'prop-types';

class StatusCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      status: this.props.status,
    };
  }

  render() {
    const { status } = this.state;

    let statusCircle = 'status-green';

    if (status === 'running') {
      statusCircle = 'status-yellow';
    } else if (status === 'failed') {
      statusCircle = 'status-red';
    }

    const statusClass = 'status '.concat(statusCircle);

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
