import React, { Component } from 'react';
import PropTypes from 'prop-types';

class JobIDCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      jobID: this.props.jobID,
      isError: this.props.isError,
    };
  }

  render() {
    const { jobID, isError } = this.state;

    const aClass = isError
      ? 'job-cell job-id-cell error'
      : 'job-cell job-id-cell';

    const href = '/'.concat(jobID);
    return (
      <p className={aClass}>{jobID}</p>
    );
  }
}

JobIDCell.propTypes = {
  jobID: PropTypes.string,
  isError: PropTypes.bool,
};

JobIDCell.defaultProps = {
  jobID: '',
  isError: false,
};

export default JobIDCell;
