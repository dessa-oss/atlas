import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobTableHeader from './JobTableHeader';
import JobTableRow from './JobTableRow';

class JobTable extends Component {
  constructor(props) {
    super(props);
    this.state = {
      jobs: this.props.jobs,
      isLoaded: this.props.isLoaded,
      allInputParams: this.props.allInputParams,
      allMetrics: this.props.allMetrics,
      statuses: this.props.statuses,
      updateHiddenStatus: this.props.updateHiddenStatus,
      updateHiddenUser: this.props.updateHiddenUser,
      updateNumberFilter: this.props.updateNumberFilter,
      allUsers: this.props.allUsers,
      hiddenUsers: this.props.hiddenUsers,
      numberFilters: this.props.numberFilters,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState(
      {
        statuses: nextProps.statuses,
        jobs: nextProps.jobs,
        isLoaded: nextProps.isLoaded,
        allInputParams: nextProps.allInputParams,
        allMetrics: nextProps.allMetrics,
        allUsers: nextProps.allUsers,
        hiddenUsers: nextProps.hiddenUsers,
        numberFilters: nextProps.numberFilters,
      },
    );
  }

  render() {
    const {
      jobs, isLoaded, allInputParams, allMetrics, statuses, updateHiddenStatus, updateHiddenUser, allUsers, hiddenUsers,
      updateNumberFilter, numberFilters,
    } = this.state;

    let jobRows = [];
    let rowNum = 1;
    const rowNumbers = [];
    if (isLoaded) {
      if (jobs.length === 0) {
        jobRows.push(<p key="no-jobs-available">No Jobs available</p>);
      } else {
        jobRows = [];
        jobs.forEach((job) => {
          const key = job.job_id;
          jobRows.push(<JobTableRow key={key} job={job} />);
          rowNumbers.push(<p key={key}>{rowNum}</p>);
          rowNum += 1;
        });
      }
    } else {
      jobRows.push(<p key="loading-jobs">Loading Jobs</p>);
    }

    return (
      <div className="job-table-content">
        <div className="job-table-container">
          <JobTableHeader
            allInputParams={allInputParams}
            allMetrics={allMetrics}
            jobs={jobs}
            statuses={statuses}
            updateHiddenStatus={updateHiddenStatus}
            rowNumbers={rowNumbers}
            jobRows={jobRows}
            updateHiddenUser={updateHiddenUser}
            allUsers={allUsers}
            hiddenUsers={hiddenUsers}
            updateNumberFilter={updateNumberFilter}
            numberFilters={numberFilters}
          />
          <div className="pagination-controls">
            <p><span className="font-bold">Viewing:</span> 1-100/600</p>
            <div className="arrow-right" />
            <p>Page 1</p>
            <div className="arrow-left" />
          </div>
        </div>
      </div>
    );
  }
}

JobTable.propTypes = {
  isMount: PropTypes.bool,
  jobs: PropTypes.array,
  isLoaded: PropTypes.bool,
  projectName: PropTypes.string,
  allInputParams: PropTypes.array,
  allMetrics: PropTypes.array,
  updateHiddenStatus: PropTypes.func,
  statuses: PropTypes.array,
  updateHiddenUser: PropTypes.func,
  allUsers: PropTypes.array,
  hiddenUsers: PropTypes.array,
  updateNumberFilter: PropTypes.func,
  numberFilters: PropTypes.array,
};

JobTable.defaultProps = {
  isMount: false,
  jobs: [],
  isLoaded: false,
  projectName: '',
  allInputParams: [],
  allMetrics: [],
  updateHiddenStatus: () => {},
  statuses: [],
  updateHiddenUser: () => {},
  allUsers: [],
  hiddenUsers: [],
  updateNumberFilter: () => {},
  numberFilters: [],
};

export default JobTable;
