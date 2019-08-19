import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobTableHeader from './JobTableHeader';
import JobTableRow from './JobTableRow';
import JobSidebar from './job-sidebar/JobSidebar';
import rowSelect from '../../../scss/jquery/rowSelect';


class JobTable extends Component {
  constructor(props) {
    super(props);
    this.onDataUpdated = props.onDataUpdated.bind(this);
    this.state = {
      jobs: this.props.jobs,
      isLoaded: this.props.isLoaded,
      allInputParams: this.props.allInputParams,
      allMetrics: this.props.allMetrics,
      statuses: this.props.statuses,
      updateHiddenStatus: this.props.updateHiddenStatus,
      updateHiddenUser: this.props.updateHiddenUser,
      updateNumberFilter: this.props.updateNumberFilter,
      updateContainsFilter: this.props.updateContainsFilter,
      updateBoolFilter: this.props.updateBoolFilter,
      updateDurationFilter: this.props.updateDurationFilter,
      updateJobIdFilter: this.props.updateJobIdFilter,
      updateStartTimeFilter: this.props.updateStartTimeFilter,
      allUsers: this.props.allUsers,
      hiddenUsers: this.props.hiddenUsers,
      numberFilters: this.props.numberFilters,
      containFilters: this.props.containFilters,
      boolFilters: this.props.boolFilters,
      boolCheckboxes: this.props.boolCheckboxes,
      durationFilters: this.props.durationFilters,
      jobIdFilters: this.props.jobIdFilters,
      startTimeFilters: this.props.startTimeFilters,
      filters: this.props.filters,
      currentJob: { job_id: null },
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
        boolCheckboxes: nextProps.boolCheckboxes,
        numberFilters: nextProps.numberFilters,
        containFilters: nextProps.containFilters,
        boolFilters: nextProps.boolFilters,
        durationFilters: nextProps.durationFilters,
        jobIdFilters: nextProps.jobIdFilters,
        startTimeFilters: nextProps.startTimeFilters,
        filters: nextProps.filters,
      },
    );
  }

  handleRowSelection(rowNumber) {
    const { selectedRow } = this.state;
    if (selectedRow === rowNumber) {
      this.setState({ selectedRow: -1 });
      rowSelect.deselect(rowNumber);
    } else {
      rowSelect.select(rowNumber);
      this.setState({ selectedRow: rowNumber });
    }
  }

  closeSideBar() {
    this.setState({ currentJob: { job_id: null } });
    this.setState({ selectedRow: -1 });
    rowSelect.removePreviousActiveRows();
  }

  render() {
    const {
      jobs, isLoaded, allInputParams, allMetrics, statuses, updateHiddenStatus, updateHiddenUser, allUsers, hiddenUsers,
      updateNumberFilter, numberFilters, updateContainsFilter, containFilters, updateBoolFilter, boolFilters,
      boolCheckboxes, updateDurationFilter, durationFilters, updateJobIdFilter, jobIdFilters, updateStartTimeFilter,
      startTimeFilters, filters,
    } = this.state;

    const jobRows = [];
    const rowNum = 1;
    const rowNumbers = [];

    const handleClick = (job) => {
      if (this.state.currentJob.job_id === job.job_id) {
        this.setState({ currentJob: { job_id: null } });
      } else {
        this.setState({ currentJob: job });
      }
      this.handleRowSelection(job.job_id);
    };

    const selectedJob = () => {
      for (let i = 0; i < jobs.length; i += 1) {
        if (jobs[i].job_id === this.state.selectedRow) {
          return jobs[i];
        }
      }
    };

    return (
      <div className="job-table-content">
        <div className="job-table-container">
          <JobSidebar
            job={selectedJob() || { job_id: null }}
            onCloseClickHandler={() => this.closeSideBar()}
          />
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
            boolCheckboxes={boolCheckboxes}
            updateNumberFilter={updateNumberFilter}
            numberFilters={numberFilters}
            updateContainsFilter={updateContainsFilter}
            containFilters={containFilters}
            updateBoolFilter={updateBoolFilter}
            boolFilters={boolFilters}
            updateDurationFilter={updateDurationFilter}
            durationFilters={durationFilters}
            updateJobIdFilter={updateJobIdFilter}
            jobIdFilters={jobIdFilters}
            updateStartTimeFilter={updateStartTimeFilter}
            startTimeFilters={startTimeFilters}
            filters={filters}
            onMetricRowClick={handleClick}
            onDataUpdated={this.onDataUpdated}
          />
          {/* <div className="pagination-controls">
            <p><span className="font-bold">Viewing:</span> 1-100/600</p>
            <div className="arrow-right" />
            <p>Page 1</p>
            <div className="arrow-left" />
          </div> */}
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
  updateContainsFilter: PropTypes.func,
  containFilters: PropTypes.array,
  updateBoolFilter: PropTypes.func,
  boolFilters: PropTypes.array,
  boolCheckboxes: PropTypes.array,
  updateDurationFilter: PropTypes.func,
  durationFilters: PropTypes.array,
  updateJobIdFilter: PropTypes.func,
  jobIdFilters: PropTypes.array,
  updateStartTimeFilter: PropTypes.func,
  startTimeFilters: PropTypes.array,
  filters: PropTypes.array,
  selectedRow: PropTypes.string,
  onDataUpdated: PropTypes.func,
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
  updateContainsFilter: () => {},
  containFilters: [],
  updateBoolFilter: () => {},
  boolFilters: [],
  boolCheckboxes: [],
  updateDurationFilter: () => {},
  durationFilters: [],
  updateJobIdFilter: () => {},
  jobIdFilters: [],
  updateStartTimeFilter: () => {},
  startTimeFilters: [],
  filters: [],
  selectedRow: -1,
  onDataUpdated: () => window.location.reload(),
};

export default JobTable;
