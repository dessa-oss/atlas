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
      statuses: this.props.statuses,
      updateHiddenStatus: this.props.updateHiddenStatus,
    };
  }

  async componentDidMount() {
    this.setState({ isMount: true });
    await this.getJobs();
  }

  componentWillReceiveProps(nextProps) {
    this.setState(
      {
        statuses: nextProps.statuses,
      },
    );
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
      jobs, isLoaded, allInputParams, allMetrics, statuses, updateHiddenStatus,
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
          rowNumbers.push(<p key={key}>{rowNum}</p>);
          rowNum += 1;
        });
      }
    } else {
      jobRows = <p>Loading Jobs</p>;
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
          />
          <div className="table-row-number">
            {rowNumbers}
          </div>
          <div className="job-table-row-container">
            {jobRows}
          </div>
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
};

export default JobTable;
