import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobTable from './JobTable';
import Toolbar from '../common/Toolbar';
import JobHeader from './JobHeader';
import CommonActions from '../../actions/CommonActions';
import JobActions from '../../actions/JobListActions';
import hoverActions from '../../../scss/jquery/rowHovers';

const baseStatus = [
  { name: 'Completed', hidden: false },
  { name: 'Running', hidden: false },
  { name: 'Failed', hidden: false },
];

const baseBoolCheckboxes = [
  { name: 'True', hidden: false },
  { name: 'False', hidden: false },
];

class JobListPage extends Component {
  constructor(props) {
    super(props);
    this.bindAllJobs();
    this.state = {
      projectName: this.props.match.params.projectName,
      project: {},
      filters: [],
      statuses: [
        { name: 'Completed', hidden: false },
        { name: 'Running', hidden: false },
        { name: 'Failed', hidden: false },
      ],
      jobs: [],
      allUsers: [],
      hiddenUsers: [],
      allInputParams: [],
      numberFilters: [],
      containFilters: [],
      boolFilters: [],
      durationFilter: [],
      jobIdFilter: [],
      isMount: false,
      allMetrics: [],
      boolCheckboxes: [
        { name: 'True', hidden: false },
        { name: 'False', hidden: false },
      ],
      startTimeFilter: [],
    };
  }

  async componentDidMount() {
    this.setState({ isMount: true });
    await this.getJobs();
    hoverActions.hover();
  }

  componentWillUnmount() {
    this.setState({ isMount: false });
  }

  async getJobs() {
    const { projectName } = this.state;
    const apiJobs = await JobActions.getJobs(projectName);
    const allUsers = JobActions.getAllJobUsers(apiJobs.jobs);
    this.formatAndSaveParams(apiJobs, allUsers);
  }

  async getFilteredJobs() {
    const {
      projectName, hiddenUsers, statuses, numberFilters, containFilters, allUsers, boolFilters, durationFilter,
      jobIdFilter, startTimeFilter,
    } = this.state;

    const flatUsers = CommonActions.getFlatArray(allUsers);
    let visibleUsers = JobActions.getVisibleFromFilter(flatUsers, hiddenUsers);
    if (visibleUsers.length === allUsers.length) {
      visibleUsers = [];
    }
    const filterJobs = await JobActions.filterJobs(
      projectName, statuses, visibleUsers, numberFilters, containFilters, boolFilters, durationFilter, jobIdFilter,
      startTimeFilter,
    );
    return filterJobs;
  }

  async updateHiddenUser(hiddenFields) {
    const { allUsers } = this.state;
    await this.setState({ hiddenUsers: hiddenFields });

    const apiFilteredJobs = await this.getFilteredJobs();
    this.clearState();
    this.formatAndSaveParams(apiFilteredJobs, allUsers);
    this.saveFilters();
    this.forceUpdate();
  }

  async updateHiddenStatus(hiddenFields) {
    const { statuses, allUsers } = this.state;
    const formattedColumns = CommonActions.formatColumns(statuses, hiddenFields);
    await this.setState({ statuses: formattedColumns });

    const apiFilteredJobs = await this.getFilteredJobs();
    this.clearState();
    this.formatAndSaveParams(apiFilteredJobs, allUsers);
    this.saveFilters();
    this.forceUpdate();
  }

  async updateNumberFilter(min, max, isShowingNotAvailable, columnName) {
    const { numberFilters, allUsers } = this.state;
    const newNumberFilters = CommonActions.getNumberFilters(numberFilters, min, max, isShowingNotAvailable, columnName);
    await this.setState({ numberFilters: newNumberFilters });

    const apiFilteredJobs = await this.getFilteredJobs();
    this.clearState();
    this.formatAndSaveParams(apiFilteredJobs, allUsers);
    this.saveFilters();
    this.forceUpdate();
  }

  async updateContainsFilter(searchText, columnName) {
    const { containFilters, allUsers } = this.state;
    const newContainFilters = CommonActions.getContainFilters(containFilters, searchText, columnName);
    await this.setState({ containFilters: newContainFilters });

    const apiFilteredJobs = await this.getFilteredJobs();
    this.clearState();
    this.formatAndSaveParams(apiFilteredJobs, allUsers);
    this.saveFilters();
    this.forceUpdate();
  }

  async updateBoolFilter(hiddenFields, columnName) {
    const { boolFilters, boolCheckboxes, allUsers } = this.state;
    const formattedBoolFilter = CommonActions.formatColumns(boolCheckboxes, hiddenFields);

    const newBoolFilters = CommonActions.getBoolFilters(boolFilters, formattedBoolFilter, columnName);

    await this.setState({ boolFilters: newBoolFilters });

    const apiFilteredJobs = await this.getFilteredJobs();
    this.clearState();
    this.formatAndSaveParams(apiFilteredJobs, allUsers);
    this.saveFilters();
    this.forceUpdate();
  }

  async updateDurationFilter(startTime, endTime) {
    const { allUsers } = this.state;

    const newDurationFilter = CommonActions.getDurationFilters(startTime, endTime, 'Duration');

    await this.setState({ durationFilter: newDurationFilter });

    const apiFilteredJobs = await this.getFilteredJobs();
    this.clearState();
    this.formatAndSaveParams(apiFilteredJobs, allUsers);
    this.saveFilters();
    this.forceUpdate();
  }

  async updateJobIdFilter(searchText) {
    const { jobIdFilter, allUsers } = this.state;
    const newJobIdFilters = CommonActions.getContainFilters(jobIdFilter, searchText, 'Job Id');
    await this.setState({ jobIdFilter: newJobIdFilters });

    const apiFilteredJobs = await this.getFilteredJobs();
    this.clearState();
    this.formatAndSaveParams(apiFilteredJobs, allUsers);
    this.saveFilters();
    this.forceUpdate();
  }

  async updateStartTimeFilter(startTime, endTime) {
    const { allUsers } = this.state;
    const newStartTimeFilter = CommonActions.getDurationFilters(startTime, endTime, 'Start Time');
    await this.setState({ startTimeFilter: newStartTimeFilter });

    const apiFilteredJobs = await this.getFilteredJobs();
    this.clearState();
    this.formatAndSaveParams(apiFilteredJobs, allUsers);
    this.saveFilters();
    this.forceUpdate();
  }

  clearState() {
    this.setState({
      jobs: [], isLoaded: true, allInputParams: [], allMetrics: [],
    });
  }

  formatAndSaveParams(apiJobs, allUsers) {
    // use is mount for async as when it returns may have been unmounted
    const { isMount } = this.state;
    if (isMount) {
      if (apiJobs != null) {
        this.saveAPIJobs(apiJobs);
        this.setProjectData(apiJobs);
        this.setState({ allUsers });
      } else {
        this.clearState();
      }
    }
  }

  setProjectData(apiJobs) {
    const jobName = apiJobs.name;
    this.setState({ project: { name: jobName } });
  }

  saveAPIJobs(apiJobs) {
    const getAllInputParams = apiJobs.input_parameter_names;
    const getAllMetrics = apiJobs.output_metric_names;
    this.setState({
      jobs: apiJobs.jobs, isLoaded: true, allInputParams: getAllInputParams, allMetrics: getAllMetrics,
    });
  }

  saveFilters() {
    const {
      statuses, hiddenUsers, allUsers, numberFilters, containFilters, boolFilters, durationFilter, jobIdFilter,
      startTimeFilter,
    } = this.state;
    const flatUsers = CommonActions.getFlatArray(allUsers);
    const newFilters = JobActions.getAllFilters(
      statuses, flatUsers, hiddenUsers, numberFilters, containFilters, boolFilters, durationFilter, jobIdFilter,
      startTimeFilter,
    );
    this.setState({ filters: newFilters });
  }

  clearFilters() {
    const { filters } = this.state;
    if (filters.length > 0) {
      this.setState({
        filters: [],
        statuses: baseStatus,
        hiddenUsers: [],
        numberFilters: [],
        containFilters: [],
        boolCheckboxes: baseBoolCheckboxes,
        durationFilter: [],
        jobIdFilter: [],
        startTimeFilter: [],
      });
      this.getJobs();
    }
  }

  async removeFilter(removeFilter) {
    const {
      filters, statuses, allUsers, hiddenUsers, numberFilters, containFilters, boolFilters, durationFilter, jobIdFilter,
      startTimeFilter,
    } = this.state;
    const newFilters = JobActions.removeFilter(filters, removeFilter);
    const newStatuses = JobActions.getUpdatedStatuses(statuses, newFilters);
    const flatUsers = CommonActions.getFlatArray(allUsers);
    const newHiddenUsers = JobActions.updateHiddenParams(flatUsers, removeFilter.value, hiddenUsers);
    const newNumberFilters = JobActions.removeFilterByName(numberFilters, removeFilter);
    const newContainFilters = JobActions.removeFilterByName(containFilters, removeFilter);
    const newBoolFilters = JobActions.removeFilterByName(boolFilters, removeFilter);
    const newDurationFilter = JobActions.removeFilterByName(durationFilter, removeFilter);
    const newJobIdFilter = JobActions.removeFilterByName(jobIdFilter, removeFilter);
    const newStartTimeFilter = JobActions.removeFilterByName(startTimeFilter, removeFilter);
    await this.setState({
      filters: newFilters,
      statuses: newStatuses,
      hiddenUsers: newHiddenUsers,
      numberFilters: newNumberFilters,
      containFilters: newContainFilters,
      boolFilters: newBoolFilters,
      durationFilter: newDurationFilter,
      jobIdFilter: newJobIdFilter,
      startTimeFilter: newStartTimeFilter,
    });
    const apiFilteredJobs = await this.getFilteredJobs();

    this.clearState();
    await this.formatAndSaveParams(apiFilteredJobs, allUsers);
    this.forceUpdate();
  }

  bindAllJobs() {
    this.updateHiddenStatus = this.updateHiddenStatus.bind(this);
    this.formatAndSaveParams = this.formatAndSaveParams.bind(this);
    this.updateHiddenUser = this.updateHiddenUser.bind(this);
    this.saveAPIJobs = this.saveAPIJobs.bind(this);
    this.setProjectData = this.setProjectData.bind(this);
    this.clearState = this.clearState.bind(this);
    this.saveFilters = this.saveFilters.bind(this);
    this.clearFilters = this.clearFilters.bind(this);
    this.removeFilter = this.removeFilter.bind(this);
    this.getFilteredJobs = this.getFilteredJobs.bind(this);
    this.updateNumberFilter = this.updateNumberFilter.bind(this);
    this.updateContainsFilter = this.updateContainsFilter.bind(this);
    this.updateBoolFilter = this.updateBoolFilter.bind(this);
    this.updateDurationFilter = this.updateDurationFilter.bind(this);
    this.updateJobIdFilter = this.updateJobIdFilter.bind(this);
    this.updateStartTimeFilter = this.updateStartTimeFilter.bind(this);
  }

  render() {
    const {
      projectName, project, filters, statuses, isLoaded, allInputParams, jobs, allMetrics, allUsers, hiddenUsers,
      numberFilters, containFilters, boolCheckboxes, boolFilters, durationFilter, jobIdFilter, startTimeFilter,
    } = this.state;
    let jobList;
    jobList = (
      <JobTable
        projectName={projectName}
        statuses={statuses}
        updateHiddenStatus={this.updateHiddenStatus}
        updateHiddenUser={this.updateHiddenUser}
        updateNumberFilter={this.updateNumberFilter}
        updateContainsFilter={this.updateContainsFilter}
        updateBoolFilter={this.updateBoolFilter}
        updateDurationFilter={this.updateDurationFilter}
        updateJobIdFilter={this.updateJobIdFilter}
        updateStartTimeFilter={this.updateStartTimeFilter}
        jobs={jobs}
        isLoaded={isLoaded}
        allInputParams={allInputParams}
        allMetrics={allMetrics}
        allUsers={allUsers}
        hiddenUsers={hiddenUsers}
        boolCheckboxes={boolCheckboxes}
        numberFilters={numberFilters}
        containFilters={containFilters}
        boolFilters={boolFilters}
        durationFilters={durationFilter}
        jobIdFilters={jobIdFilter}
        startTimeFilters={startTimeFilter}
        filters={filters}
      />
    );
    return (
      <div className="job-list-container">
        <Toolbar />
        <JobHeader
          project={project}
          filters={filters}
          clearFilters={this.clearFilters}
          removeFilter={this.removeFilter}
        />
        {jobList}
      </div>
    );
  }
}

JobListPage.propTypes = {
  projectName: PropTypes.string,
  project: PropTypes.object,
  filters: PropTypes.array,
  statuses: PropTypes.array,
  jobs: PropTypes.array,
  allInputParams: PropTypes.array,
  allMetrics: PropTypes.array,
  allUsers: PropTypes.array,
  hiddenUsers: PropTypes.array,
  containFilters: PropTypes.array,
  boolCheckboxes: PropTypes.array,
  boolFilters: PropTypes.array,
  durationFilter: PropTypes.array,
  jobIdFilter: PropTypes.array,
  startTimeFilter: PropTypes.array,
  match: PropTypes.shape({
    params: PropTypes.shape({
      projectName: PropTypes.string,
    }),
  }),
};

JobListPage.defaultProps = {
  projectName: '',
  project: {},
  filters: [],
  statuses: [],
  jobs: [],
  allInputParams: [],
  allMetrics: [],
  allUsers: [],
  hiddenUsers: [],
  containFilters: [],
  boolCheckboxes: [],
  boolFilters: [],
  durationFilter: [],
  jobIdFilter: [],
  startTimeFilter: [],
  match: {
    params: {
      projectName: '',
    },
  },
};

export default JobListPage;
