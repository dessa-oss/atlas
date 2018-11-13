import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobTableHeader from './JobTableHeader';
import JobTableRow from './JobTableRow';
import JobActions from '../../actions/JobListActions';

class JobTable extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isMount: false,
      jobs: [],
      isLoaded: false,
      projectName: this.props.projectName,
      hiddenInputParams: [],
      allInputParams: ['input1', 'input2', 'input3', 'input4', 'longlonglonglonglonginput5'],
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
    // use is mount for async as when it returns may have been unmounted
    const { isMount } = this.state;
    if (isMount) {
      if (apiJobs != null) {
        this.setState({ jobs: apiJobs.jobs, isLoaded: true });
      } else {
        this.setState({ jobs: [], isLoaded: true });
      }
    }
  }

  render() {
    const {
      jobs, isLoaded, hiddenInputParams, allInputParams,
    } = this.state;

    let jobRows = [];
    if (isLoaded) {
      if (jobs.length === 0) {
        jobRows = <p>No Jobs available</p>;
      } else {
        jobRows = [];
        jobs.forEach((job) => {
          const key = job.job_id;
          jobRows.push(<JobTableRow key={key} job={job} />);
        });
      }
    } else {
      jobRows = <p>Loading projects</p>;
    }

    return (
      <div className="job-table-container">
        <JobTableHeader hiddenInputParams={hiddenInputParams} allInputParams={allInputParams} />
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
  hiddenInputParams: PropTypes.array,
  allInputParams: PropTypes.array,
};

JobTable.defaultProps = {
  isMount: false,
  jobs: [],
  isLoaded: false,
  projectName: '',
  hiddenInputParams: [],
  allInputParams: [],
};

export default JobTable;
