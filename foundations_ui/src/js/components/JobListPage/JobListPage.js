import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobTable from './JobTable';
import Toolbar from '../common/Toolbar';
import JobHeader from './JobHeader';
import CommonActions from '../../actions/CommonActions';
import JobActions from '../../actions/JobListActions';

const baseStatus = [
  { name: 'Completed', hidden: false },
  { name: 'Processing', hidden: false },
  { name: 'Error', hidden: false },
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
      projectName: this.props.projectName,
      project: this.props.project,
      filters: [],
      statuses: [
        { name: 'Completed', hidden: false },
        { name: 'Processing', hidden: false },
        { name: 'Error', hidden: false },
      ],
      jobs: [],
      allUsers: [],
      hiddenUsers: [],
      allInputParams: [],
      numberFilters: [],
      containFilters: [],
      boolFilters: [],
      durationFilter: [],
      isMount: false,
      allMetrics: [],
      boolCheckboxes: [
        { name: 'True', hidden: false },
        { name: 'False', hidden: false },
      ],
    };
  }

  async componentDidMount() {
    this.setState({ isMount: true });
    await this.getJobs();
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
    } = this.state;

    const flatUsers = CommonActions.getFlatArray(allUsers);
    let visibleUsers = JobActions.getVisibleFromFilter(flatUsers, hiddenUsers);
    if (visibleUsers.length === allUsers.length) {
      visibleUsers = [];
    }
    const filterJobs = await JobActions.filterJobs(
      projectName, statuses, visibleUsers, numberFilters, containFilters, boolFilters, durationFilter,
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

    const newDurationFilter = CommonActions.getDurationFilters(startTime, endTime);

    await this.setState({ durationFilter: newDurationFilter });

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
        this.setState({ allUsers });
      } else {
        this.clearState();
      }
    }
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
      statuses, hiddenUsers, allUsers, numberFilters, containFilters, boolFilters, durationFilter,
    } = this.state;
    const flatUsers = CommonActions.getFlatArray(allUsers);
    const newFilters = JobActions.getAllFilters(
      statuses, flatUsers, hiddenUsers, numberFilters, containFilters, boolFilters, durationFilter,
    );
    this.setState({ filters: newFilters });
  }

  clearFilters() {
    this.setState({
      filters: [],
      statuses: baseStatus,
      hiddenUsers: [],
      numberFilters: [],
      containFilters: [],
      boolCheckboxes: baseBoolCheckboxes,
      durationFilter: [],
    });
    this.getJobs();
  }

  async removeFilter(removeFilter) {
    const {
      filters, statuses, allUsers, hiddenUsers, numberFilters, containFilters, boolFilters,
    } = this.state;
    const newFilters = JobActions.removeFilter(filters, removeFilter);
    const newStatuses = JobActions.getUpdatedStatuses(statuses, newFilters);
    const flatUsers = CommonActions.getFlatArray(allUsers);
    const newHiddenUsers = JobActions.updateHiddenParams(flatUsers, removeFilter.value, hiddenUsers);
    const newNumberFilters = JobActions.removeFilterByName(numberFilters, removeFilter);
    const newContainFilters = JobActions.removeFilterByName(containFilters, removeFilter);
    const newBoolFilters = JobActions.removeFilterByName(boolFilters, removeFilter);
    await this.setState({
      filters: newFilters,
      statuses: newStatuses,
      hiddenUsers: newHiddenUsers,
      numberFilters: newNumberFilters,
      containFilters: newContainFilters,
      boolFilters: newBoolFilters,
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
    this.clearState = this.clearState.bind(this);
    this.saveFilters = this.saveFilters.bind(this);
    this.clearFilters = this.clearFilters.bind(this);
    this.removeFilter = this.removeFilter.bind(this);
    this.getFilteredJobs = this.getFilteredJobs.bind(this);
    this.updateNumberFilter = this.updateNumberFilter.bind(this);
    this.updateContainsFilter = this.updateContainsFilter.bind(this);
    this.updateBoolFilter = this.updateBoolFilter.bind(this);
    this.updateDurationFilter = this.updateDurationFilter.bind(this);
  }

  render() {
    const {
      projectName, project, filters, statuses, isLoaded, allInputParams, jobs, allMetrics, allUsers, hiddenUsers,
      numberFilters, containFilters, boolCheckboxes, boolFilters,
    } = this.state;
    return (
      <div className="job-list-container">
        <Toolbar />
        <JobHeader
          project={project}
          filters={filters}
          clearFilters={this.clearFilters}
          removeFilter={this.removeFilter}
        />
        <JobTable
          projectName={projectName}
          statuses={statuses}
          updateHiddenStatus={this.updateHiddenStatus}
          updateHiddenUser={this.updateHiddenUser}
          updateNumberFilter={this.updateNumberFilter}
          updateContainsFilter={this.updateContainsFilter}
          updateBoolFilter={this.updateBoolFilter}
          updateDurationFilter={this.updateDurationFilter}
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
        />
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
};

export default JobListPage;
