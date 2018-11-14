import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobCell from './cells/JobCell';
import StartCell from './cells/StartTimeCell';
import StatusCell from './cells/StatusCell';
import JobIDCell from './cells/JobIDCell';
import DurationCell from './cells/DurationCell';
import UserCell from './cells/UserCell';
import JobActions from '../../actions/JobListActions';

class JobTableRow extends Component {
  constructor(props) {
    super(props);
    this.state = {
      job: this.props.job,
    };
  }

  render() {
    const { job } = this.state;

    return (
      <div className="job-table-row">
        <StartCell startTime={job.start_time} />
        <StatusCell status={job.status} />
        <JobIDCell jobID={job.job_id} />
        <DurationCell duration={JobActions.getDateDiff(job.start_time, job.completed_time)} />
        <UserCell user={job.user} />
      </div>
    );
  }
}

JobTableRow.propTypes = {
  job: PropTypes.object,
};

JobTableRow.defaultProps = {
  job: {},
};

export default JobTableRow;
