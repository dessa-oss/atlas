import React, { Component } from 'react';
import PropTypes from 'prop-types';

class JobIDCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      jobID: this.props.jobID,
      isError: this.props.isError,
      rowNumber: this.props.rowNumber,
    };
  }

  render() {
    const { jobID, isError, rowNumber } = this.state;

    const aClass = isError
      ? `job-cell job-id-cell error row-${rowNumber}`
      : `job-cell job-id-cell row-${rowNumber}`;

    const href = '/'.concat(jobID);
    return (
      <p className={aClass}>{jobID}</p>
    );
  }
}

JobIDCell.propTypes = {
  jobID: PropTypes.string,
  isError: PropTypes.bool,
  rowNumber: PropTypes.number,
};

JobIDCell.defaultProps = {
  jobID: '',
  isError: false,
  rowNumber: 0,
};

export default JobIDCell;
