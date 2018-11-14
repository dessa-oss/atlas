import React, { Component } from 'react';
import PropTypes from 'prop-types';

class JobIDCell extends Component {
  constructor(props) {
    super(props);
    this.state = {
      jobID: this.props.jobID,
    };
  }

  render() {
    const { jobID } = this.state;

    return (
      <p className="job-cell job-id-cell header-4 font-bold">{jobID}</p>
    );
  }
}

JobIDCell.propTypes = {
  jobID: PropTypes.string,
};

JobIDCell.defaultProps = {
  jobID: '',
};

export default JobIDCell;
