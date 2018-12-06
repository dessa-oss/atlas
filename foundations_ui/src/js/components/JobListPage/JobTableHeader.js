import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { ScrollSync } from 'react-scroll-sync';
import TableStaticColumns from './TableStaticColumns';
import InputMetric from '../common/InputMetric';
import UserFilter from '../common/filters/UserFilter';
import StatusFilter from '../common/filters/StatusFilter';
import JobActions from '../../actions/JobListActions';
import CommonActions from '../../actions/CommonActions';

const isMetric = true;
const noneHidden = [];

class JobTableHeader extends Component {
  constructor(props) {
    super(props);
    this.toggleUserFilter = this.toggleUserFilter.bind(this);
    this.searchUserFilter = this.searchUserFilter.bind(this);
    this.toggleStatusFilter = this.toggleStatusFilter.bind(this);
    this.state = {
      allInputParams: this.props.allInputParams,
      allMetrics: this.props.allMetrics,
      jobs: this.props.jobs,
      isShowingUserFilter: false,
      isShowingStatusFilter: false,
      updateHiddenStatus: this.props.updateHiddenStatus,
      statuses: this.props.statuses,
      rowNumbers: this.props.rowNumbers,
      jobRows: this.props.jobRows,
      searchText: '',
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState(
      {
        allInputParams: nextProps.allInputParams,
        jobs: nextProps.jobs,
        allMetrics: nextProps.allMetrics,
        statuses: nextProps.statuses,
        jobRows: nextProps.jobRows,
        rowNumbers: nextProps.rowNumbers,
      },
    );
  }

  toggleUserFilter() {
    const { isShowingUserFilter } = this.state;
    this.setState({ isShowingUserFilter: !isShowingUserFilter });
  }

  searchUserFilter(searchText) {
    this.setState({ searchText });
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
      rowNumbers,
      jobRows,
      searchText,
    } = this.state;

    let userFilter = null;
    if (isShowingUserFilter) {
      const allUsers = JobActions.getAllJobUsers(jobs);
      const nameArray = CommonActions.getFlatArray(allUsers);
      const filteredUsers = CommonActions.formatColumns(nameArray, noneHidden, searchText);
      userFilter = (
        <UserFilter
          columns={filteredUsers}
          toggleShowingFilter={this.toggleUserFilter}
          changeHiddenParams={updateHiddenStatus}
          searchUserFilter={this.searchUserFilter}
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
      <ScrollSync>
        <div className="job-list-container">
          <TableStaticColumns
            jobRows={jobRows}
            rowNumbers={rowNumbers}
            toggleUserFilter={this.toggleUserFilter}
            toggleStatusFilter={this.toggleStatusFilter}
          />
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
          {userFilter}
          {statusFilter}
        </div>
      </ScrollSync>
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
  rowNumbers: PropTypes.array,
  jobRows: PropTypes.array,
};

JobTableHeader.defaultProps = {
  allInputParams: [],
  jobs: [],
  allMetrics: [],
  isShowingUserFilter: false,
  isShowingStatusFilter: false,
  updateHiddenStatus: () => {},
  statuses: [],
  rowNumbers: [],
  jobRows: [],
};

export default JobTableHeader;
