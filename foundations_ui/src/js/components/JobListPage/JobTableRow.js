import React, { Component } from 'react';
import PropTypes from 'prop-types';
import StartCell from './cells/StartTimeCell';
import StatusCell from './cells/StatusCell';
import JobIDCell from './cells/JobIDCell';
// import TagsCell from './cells/TagsCell';
import DurationCell from './cells/DurationCell';
import UserCell from './cells/UserCell';
import CancelJobCell from './cells/CancelJobCell';
import JobListActions from '../../actions/JobListActions';
import CommonActions from '../../actions/CommonActions';

class JobTableRow extends Component {
  constructor(props) {
    super(props);
    this.state = {
      job: this.props.job,
      rowNumber: this.props.rowNumber,
    };
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.job !== this.props.job) {
      this.setState(
        {
          job: nextProps.job,
          rowNumber: nextProps.rowNumber,
        },
      );
    }
  }

  render() {
    const { job, rowNumber } = this.state;

    const isError = CommonActions.isError(job.status);

    return (
      <div
        role="presentation"
        className="job-table-row"
        onClick={() => this.props.handleClick(job, rowNumber)}
        onKeydown={() => this.props.handleClick(job, rowNumber)}
      >
        <CancelJobCell job={job} />
        <JobIDCell jobID={job.job_id} isError={isError} rowNumber={rowNumber} />
        <StartCell startTime={job.start_time} isError={isError} rowNumber={rowNumber} />
        <StatusCell status={job.status} isError={isError} rowNumber={rowNumber} />
        <DurationCell
          duration={JobListActions.parseDuration(job.duration)}
          isError={isError}
          rowNumber={rowNumber}
        />
        <UserCell user={job.user} isError={isError} rowNumber={rowNumber} />
        {/* <TagsCell tag={job.tags} isError={isError} rowNumber={rowNumber} /> */}
      </div>
    );
  }
}

JobTableRow.propTypes = {
  job: PropTypes.object,
  rowNumber: PropTypes.number,
  handleClick: PropTypes.func,
};

JobTableRow.defaultProps = {
  job: {},
  rowNumber: 0,
  handleClick: () => null,
};

export default JobTableRow;
