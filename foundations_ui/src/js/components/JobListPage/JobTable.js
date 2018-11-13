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
    };
  }

  async componentDidMount() {
    await this.setState({ isMount: true });
    this.getJobs();
  }

  componentWillUnmount() {
    this.setState({ isMount: false });
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
    const { jobs, isLoaded, hiddenInputParams } = this.state;

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
        <JobTableHeader hiddenInputParams={hiddenInputParams} />
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
};

JobTable.defaultProps = {
  isMount: false,
  jobs: [],
  isLoaded: false,
  projectName: '',
  hiddenInputParams: [],
};

export default JobTable;
