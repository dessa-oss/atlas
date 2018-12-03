import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobColumnHeader from '../common/JobColumnHeader';
import TableSectionHeader from '../common/TableSectionHeader';
import InputMetric from '../common/InputMetric';
import UserFilter from '../common/filters/UserFilter';
import StatusFilter from '../common/filters/StatusFilter';
import JobActions from '../../actions/JobListActions';

const isStatus = true;
const isMetric = true;

class JobTableHeader extends Component {
  constructor(props) {
    super(props);
    this.toggleUserFilter = this.toggleUserFilter.bind(this);
    this.toggleStatusFilter = this.toggleStatusFilter.bind(this);
    this.state = {
      allInputParams: this.props.allInputParams,
      allMetrics: this.props.allMetrics,
      jobs: this.props.jobs,
      isShowingUserFilter: false,
      isShowingStatusFilter: false,
      updateHiddenStatus: this.props.updateHiddenStatus,
      statuses: this.props.statuses,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState(
      {
        allInputParams: nextProps.allInputParams,
        jobs: nextProps.jobs,
        allMetrics: nextProps.allMetrics,
        statuses: nextProps.statuses,
      },
    );
  }

  toggleUserFilter() {
    const { isShowingUserFilter } = this.state;
    this.setState({ isShowingUserFilter: !isShowingUserFilter });
  }

  toggleStatusFilter() {
    const { isShowingStatusFilter } = this.state;
    this.setState({ isShowingStatusFilter: !isShowingStatusFilter });
  }

  render() {
    const {
      allInputParams,
      jobs,
      allMetrics,
      isShowingUserFilter,
      isShowingStatusFilter,
      statuses,
      updateHiddenStatus,
    } = this.state;

    let userFilter = null;
    if (isShowingUserFilter) {
      const allUsers = JobActions.getAllJobUsers(jobs);
      userFilter = (
        <UserFilter
          columns={allUsers}
          toggleShowingFilter={this.toggleUserFilter}
          changeHiddenParams={updateHiddenStatus}
        />
      );
    }

    let statusFilter = null;
    let hiddenInputParams = [];
    if (isShowingStatusFilter) {
      hiddenInputParams = statuses.map(
        (status) => {
          if (status.hidden === true) {
            return status.name;
          }
        },
      );
      statusFilter = (
        <StatusFilter
          columns={statuses}
          toggleShowingFilter={this.toggleStatusFilter}
          changeHiddenParams={updateHiddenStatus}
          hiddenInputParams={hiddenInputParams}
        />
      );
    }

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
          <JobColumnHeader
            title="Status"
            isStatus={isStatus}
            className="status-offset"
            toggleFilter={this.toggleStatusFilter}
          />
          <JobColumnHeader title="Job ID" className="job-id-offset" />
          <JobColumnHeader title="Duration" className="duration-offset" />
          <JobColumnHeader title="User" className="user-offset" toggleFilter={this.toggleUserFilter} />
        </div>
        {userFilter}
        {statusFilter}
      </div>
    );
  }
}

JobTableHeader.propTypes = {
  allInputParams: PropTypes.array,
  jobs: PropTypes.array,
  allMetrics: PropTypes.array,
  isShowingUserFilter: PropTypes.bool,
  isShowingStatusFilter: PropTypes.bool,
  updateHiddenStatus: PropTypes.func,
  statuses: PropTypes.array,
};

JobTableHeader.defaultProps = {
  allInputParams: [],
  jobs: [],
  allMetrics: [],
  isShowingUserFilter: false,
  isShowingStatusFilter: false,
  updateHiddenStatus: () => {},
  statuses: [],
};

export default JobTableHeader;
