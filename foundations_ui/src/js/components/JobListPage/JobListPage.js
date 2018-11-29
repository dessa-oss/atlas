import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobTable from './JobTable';
import Toolbar from '../common/Toolbar';
import JobHeader from './JobHeader';
import CommonActions from '../../actions/CommonActions';
import JobActions from '../../actions/JobListActions';

class JobListPage extends Component {
  constructor(props) {
    super(props);
    this.updateHiddenStatus = this.updateHiddenStatus.bind(this);
    this.formatAndSaveParams = this.formatAndSaveParams.bind(this);
    this.saveAPIJobs = this.saveAPIJobs.bind(this);
    this.clearState = this.clearState.bind(this);
    this.saveFilters = this.saveFilters.bind(this);
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
    this.formatAndSaveParams(apiJobs);
  }

  formatAndSaveParams(apiJobs) {
    // use is mount for async as when it returns may have been unmounted
    const { isMount } = this.state;
    if (isMount) {
      if (apiJobs != null) {
        this.saveAPIJobs(apiJobs);
      } else {
        this.clearState();
      }
    }
  }

  clearState() {
    this.setState({
      jobs: [], isLoaded: true, allInputParams: [], allMetrics: [],
    });
  }

  async updateHiddenStatus(hiddenFields) {
    const { statuses, projectName } = this.state;
    const statusNamesArray = statuses.map(status => status.name);
    const formattedColumns = CommonActions.formatColumns(statusNamesArray, hiddenFields);
    const apiFilteredJobs = await JobActions.filterJobs(projectName, formattedColumns);
    this.clearState();
    this.formatAndSaveParams(apiFilteredJobs);
    this.setState({ statuses: formattedColumns });
    this.saveFilters();
    this.forceUpdate();
  }

  saveAPIJobs(apiJobs) {
    const getAllInputParams = JobActions.getAllInputParams(apiJobs.jobs);
    const getAllMetrics = JobActions.getAllMetrics(apiJobs.jobs);
    this.setState({
      jobs: apiJobs.jobs, isLoaded: true, allInputParams: getAllInputParams, allMetrics: getAllMetrics,
    });
  }

  saveFilters() {
    const { filters, statuses } = this.state;
    const newFilters = JobActions.getAllFilters(filters, statuses);
    this.setState({ filters: newFilters });
  }

  render() {
    const {
      projectName, project, filters, statuses, isLoaded, allInputParams, jobs, allMetrics,
    } = this.state;
    return (
      <div className="job-list-container">
        <Toolbar />
        <JobHeader project={project} filters={filters} />
        <JobTable
          projectName={projectName}
          statuses={statuses}
          updateHiddenStatus={this.updateHiddenStatus}
          jobs={jobs}
          isLoaded={isLoaded}
          allInputParams={allInputParams}
          allMetrics={allMetrics}
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
};

JobListPage.defaultProps = {
  projectName: '',
  project: {},
  filters: [],
  statuses: [],
  jobs: [],
  allInputParams: [],
  allMetrics: [],
};

export default JobListPage;
