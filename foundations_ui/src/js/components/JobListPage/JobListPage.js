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
      isMount: false,
      allMetrics: [],
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
    const { projectName, hiddenUsers, statuses } = this.state;
    const filterJobs = await JobActions.filterJobs(projectName, statuses, hiddenUsers);
    return filterJobs;
  }

  async updateHiddenUser(hiddenFields) {
    const { allUsers } = this.state;
    const usersNamesArray = CommonActions.getFlatArray(allUsers);
    await this.setState({ hiddenUsers: hiddenFields });

    const apiFilteredJobs = await this.getFilteredJobs();
    this.clearState();
    this.formatAndSaveParams(apiFilteredJobs, allUsers);
    this.saveFilters();
    this.forceUpdate();
  }

  async updateHiddenStatus(hiddenFields) {
    const { statuses, allUsers } = this.state;
    const statusNamesArray = statuses.map(status => status.name);
    const formattedColumns = CommonActions.formatColumns(statusNamesArray, hiddenFields);
    await this.setState({ statuses: formattedColumns });

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
    const { filters, statuses } = this.state;
    const newFilters = JobActions.getAllFilters(filters, statuses);

    this.setState({ filters: newFilters });
  }

  clearFilters() {
    this.setState({ filters: [], statuses: baseStatus });
    this.getJobs();
  }

  async removeFilter(removeFilter) {
    const { filters, statuses } = this.state;
    const newFilters = JobActions.removeFilter(filters, removeFilter);
    const newStatuses = JobActions.getUpdatedStatuses(statuses, newFilters);
    this.setState({ filters: newFilters, statuses: newStatuses });
    const apiFilteredJobs = await this.getFilteredJobs();

    this.clearState();
    this.formatAndSaveParams(apiFilteredJobs);
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
  }

  render() {
    const {
      projectName, project, filters, statuses, isLoaded, allInputParams, jobs, allMetrics, allUsers, hiddenUsers,
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
          jobs={jobs}
          isLoaded={isLoaded}
          allInputParams={allInputParams}
          allMetrics={allMetrics}
          allUsers={allUsers}
          hiddenUsers={hiddenUsers}
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
};

export default JobListPage;
