import React from 'react';
import PropTypes from 'prop-types';
import JobTable from '../JobListPage/JobTable';
import JobHeader from '../JobListPage/JobHeader';
import CommonActions from '../../actions/CommonActions';
import JobListActions from '../../actions/JobListActions';
import hoverActions from '../../../scss/jquery/rowHovers';
import ModalJobDetails from '../JobListPage/job-sidebar/ModalJobDetails';

const baseStatus = [
  { name: 'Completed', hidden: false },
  { name: 'Running', hidden: false },
  { name: 'Failed', hidden: false },
];

const baseBoolCheckboxes = [
  { name: 'True', hidden: false },
  { name: 'False', hidden: false },
];

class JobDetails extends React.Component {
  constructor(props) {
    super(props);
    this.bindAllJobs();
    this.state = {
      projectName: 'demo',
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
      queryStatus: 200,
      modalJobDetailsVisible: false,
      selectedJob: {},
    };
  }

  async componentDidMount() {
    await this.setState({ isMount: true });
    this.getJobs();
  }

  async getJobs() {
    const { projectName } = this.state;
    const fetchedJobs = await JobListActions.getJobs(projectName);
    const apiJobs = fetchedJobs;
    this.setState({ queryStatus: apiJobs === null ? 400 : 200 });
    const allUsers = JobListActions.getAllJobUsers(apiJobs.jobs);
    this.formatAndSaveParams(apiJobs, allUsers);
    this.updateEventsOnJobs();
    this.forceUpdate();
  }

  updateEventsOnJobs() {
    hoverActions.hover();
  }

  async getFilteredJobs() {
    const {
      projectName, hiddenUsers, statuses, numberFilters, containFilters, allUsers, boolFilters, durationFilter,
      jobIdFilter, startTimeFilter,
    } = this.state;

    const flatUsers = CommonActions.getFlatArray(allUsers);
    let visibleUsers = JobListActions.getVisibleFromFilter(flatUsers, hiddenUsers);
    if (visibleUsers.length === allUsers.length) {
      visibleUsers = [];
    }
    const fetchedFilteredJobs = await JobListActions.filterJobs(
      projectName, statuses, visibleUsers, numberFilters, containFilters, boolFilters, durationFilter, jobIdFilter,
      startTimeFilter,
    );
    this.setState({ queryStatus: fetchedFilteredJobs.status });
    if (this.checkStatusOk()) {
      return fetchedFilteredJobs.result;
    }
    return null;
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
    const newFilters = JobListActions.getAllFilters(
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
    const newFilters = JobListActions.removeFilter(filters, removeFilter);
    const newStatuses = JobListActions.getUpdatedStatuses(statuses, newFilters);
    const flatUsers = CommonActions.getFlatArray(allUsers);
    const newHiddenUsers = JobListActions.updateHiddenParams(flatUsers, removeFilter.value, hiddenUsers);
    const newNumberFilters = JobListActions.removeFilterByName(numberFilters, removeFilter);
    const newContainFilters = JobListActions.removeFilterByName(containFilters, removeFilter);
    const newBoolFilters = JobListActions.removeFilterByName(boolFilters, removeFilter);
    const newDurationFilter = JobListActions.removeFilterByName(durationFilter, removeFilter);
    const newJobIdFilter = JobListActions.removeFilterByName(jobIdFilter, removeFilter);
    const newStartTimeFilter = JobListActions.removeFilterByName(startTimeFilter, removeFilter);
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

  onToggleModalJobDetails(job) {
    console.log('ON TOGGLE: ', job);
    const { modalJobDetailsVisible } = this.state;
    const value = !modalJobDetailsVisible;

    this.setState({
      modalJobDetailsVisible: value,
      selectedJob: job,
    });
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
    this.onToggleModalJobDetails = this.onToggleModalJobDetails.bind(this);
  }

  render() {
    const {
      projectName, project, filters, statuses, isLoaded, allInputParams, jobs, allMetrics, allUsers, hiddenUsers,
      numberFilters, containFilters, boolCheckboxes, boolFilters, durationFilter, jobIdFilter, startTimeFilter,
      queryStatus, selectedJob, modalJobDetailsVisible,
    } = this.state;

    const jobList = (
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
        onClickJob={(job) => {
          this.onToggleModalJobDetails(job);
        }}
      />
    );

    return (
      <div>
        <div className="job-list-container">
          {jobList}
        </div>
        <ModalJobDetails job={selectedJob} visible={modalJobDetailsVisible} onToggle={this.onToggleModalJobDetails} />
      </div>

    );
  }
}

JobDetails.propTypes = {
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
  queryStatus: PropTypes.number,
  history: PropTypes.object,
};

JobDetails.defaultProps = {
  projectName: 'demo',
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
  queryStatus: 200,
  history: {},
};

export default JobDetails;
