import React, { Component } from 'react';
import PropTypes from 'prop-types';
import StartCell from './cells/StartTimeCell';
import StatusCell from './cells/StatusCell';
import JobIDCell from './cells/JobIDCell';
import DurationCell from './cells/DurationCell';
import UserCell from './cells/UserCell';
import JobActions from '../../actions/JobListActions';
import CommonActions from '../../actions/CommonActions';

class JobTableRow extends Component {
  constructor(props) {
    super(props);
    this.state = {
      job: this.props.job,
    };
  }

  render() {
    const { job } = this.state;

    const isError = CommonActions.isError(job.status);

    return (
      <div className="job-table-row">
        <StartCell startTime={job.start_time} isError={isError} />
        <StatusCell status={job.status} isError={isError} />
        <JobIDCell jobID={job.job_id} isError={isError} />
        <DurationCell
          duration={JobActions.getDateDiff(job.start_time, job.completed_time)}
          isError={isError}
        />
        <UserCell user={job.user} isError={isError} />
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
