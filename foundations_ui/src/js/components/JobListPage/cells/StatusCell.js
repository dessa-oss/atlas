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

  componentWillReceiveProps(nextProps) {
    if (nextProps.rowNumber !== this.props.status) {
      this.setState({
        status: nextProps.status,
        isError: nextProps.isError,
        rowNumber: nextProps.rowNumber,
      });
    }
  }

  render() {
    const { status, isError, rowNumber } = this.state;

    const statusClass = JobListActions.getStatusCircle(status);
    const divClass = isError ? `status-cell error row-${rowNumber}` : `status-cell  row-${rowNumber}`;

    return (
      <span className={divClass}>
        <span className={statusClass} />
      </span>
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
