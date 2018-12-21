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
      rowNumber: this.props.rowNumber,
    };
  }

  render() {
    const { job, rowNumber } = this.state;

    const isError = CommonActions.isError(job.status);

    return (
      <div className="job-table-row">
        <StartCell startTime={job.start_time} isError={isError} rowNumber={rowNumber} />
        <StatusCell status={job.status} isError={isError} rowNumber={rowNumber} />
        <JobIDCell jobID={job.job_id} isError={isError} rowNumber={rowNumber} />
        <DurationCell
          duration={JobActions.getDateDiff(job.start_time, job.completed_time)}
          isError={isError}
          rowNumber={rowNumber}
        />
        <UserCell user={job.user} isError={isError} rowNumber={rowNumber} />
      </div>
    );
  }
}

JobTableRow.propTypes = {
  job: PropTypes.object,
  rowNumber: PropTypes.number,
};

JobTableRow.defaultProps = {
  job: {},
  rowNumber: 0,
};

export default JobTableRow;
