import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobTableHeader from './JobTableHeader';
import JobTableRow from './JobTableRow';
import JobActions from '../../actions/JobListActions';

class JobTable extends Component {
  constructor(props) {
    super(props);
    this.formatAndSaveParams = this.formatAndSaveParams.bind(this);
    this.saveAPIJobs = this.saveAPIJobs.bind(this);
    this.clearState = this.clearState.bind(this);
    this.state = {
      isMount: false,
      jobs: [],
      isLoaded: false,
      projectName: this.props.projectName,
      allInputParams: [],
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

  async getInputParams() {
    this.setState({ allInputParams: ['input1', 'input2', 'input3', 'input4', 'input5'] });
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

  saveAPIJobs(apiJobs) {
    const getAllInputParams = JobActions.getAllInputParams(apiJobs.jobs);
    const getAllMetrics = JobActions.getAllMetrics(apiJobs.jobs);
    this.setState({
      jobs: apiJobs.jobs, isLoaded: true, allInputParams: getAllInputParams, allMetrics: getAllMetrics,
    });
  }

  clearState() {
    this.setState({
      jobs: [], isLoaded: true, allInputParams: [], allMetrics: [],
    });
  }

  render() {
    const {
      jobs, isLoaded, hiddenInputParams, allInputParams, allMetrics,
    } = this.state;

    let jobRows = [];
    let rowNum = 1;
    const rowNumbers = [];
    if (isLoaded) {
      if (jobs.length === 0) {
        jobRows = <p>No Jobs available</p>;
      } else {
        jobRows = [];
        jobs.forEach((job) => {
          const key = job.job_id;
          jobRows.push(<JobTableRow key={key} job={job} />);
          rowNumbers.push(<p>{rowNum}</p>);
          rowNum += 1;
        });
      }
    } else {
      jobRows = <p>Loading projects</p>;
    }

    return (
      <div className="job-table-container">
        <JobTableHeader
          allInputParams={allInputParams}
          allMetrics={allMetrics}
          jobs={jobs}
        />
        <div className="table-row-number">
          {rowNumbers}
        </div>
        <div className="job-table-row-container">
          {jobRows}
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
};

JobTable.defaultProps = {
  isMount: false,
  jobs: [],
  isLoaded: false,
  projectName: '',
  allInputParams: [],
  allMetrics: [],
};

export default JobTable;
