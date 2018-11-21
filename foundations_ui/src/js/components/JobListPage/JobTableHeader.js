import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobColumnHeader from '../common/JobColumnHeader';
import TableSectionHeader from '../common/TableSectionHeader';
import InputMetric from '../common/InputMetric';

const isStatus = true;
const isMetric = true;

class JobTableHeader extends Component {
  constructor(props) {
    super(props);
    this.state = {
      allInputParams: this.props.allInputParams,
      allMetrics: this.props.allMetrics,
      jobs: this.props.jobs,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ allInputParams: nextProps.allInputParams, jobs: nextProps.jobs, allMetrics: nextProps.allMetrics });
  }

  render() {
    const {
      allInputParams,
      jobs,
      allMetrics,
    } = this.state;

    return (
      <div className="job-list-container">
        <TableSectionHeader />
        <InputMetric
          header="input parameter"
          allInputParams={allInputParams}
          jobs={jobs}
        />
        <InputMetric
          header="metrics"
          allInputParams={allMetrics}
          jobs={jobs}
          isMetric={isMetric}
        />
        <div className="job-column-header-container">
          <JobColumnHeader title="Start Time" className="start-time-offset" />
          <JobColumnHeader title="Status" isStatus={isStatus} className="status-offset" />
          <JobColumnHeader title="Job ID" className="job-id-offset" />
          <JobColumnHeader title="Duration" className="duration-offset" />
          <JobColumnHeader title="User" className="user-offset" />
        </div>
      </div>
    );
  }
}

JobTableHeader.propTypes = {
  allInputParams: PropTypes.array,
  jobs: PropTypes.array,
  allMetrics: PropTypes.array,
};

JobTableHeader.defaultProps = {
  allInputParams: [],
  jobs: [],
  allMetrics: [],
};

export default JobTableHeader;
