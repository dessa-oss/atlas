import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { ScrollSync } from 'react-scroll-sync';
import TableStaticColumns from './TableStaticColumns';
import InputMetric from '../common/InputMetric';
import UserFilter from '../common/filters/UserFilter';
import StatusFilter from '../common/filters/StatusFilter';
import DurationFilter from '../common/filters/DurationFilter';
import NumberFilter from '../common/filters/NumberFilter';
import CommonActions from '../../actions/CommonActions';

const isMetric = true;

class JobTableHeader extends Component {
  constructor(props) {
    super(props);
    this.toggleUserFilter = this.toggleUserFilter.bind(this);
    this.searchUserFilter = this.searchUserFilter.bind(this);
    this.toggleStatusFilter = this.toggleStatusFilter.bind(this);
    this.toggleDurationFilter = this.toggleDurationFilter.bind(this);
    this.toggleNumberFilter = this.toggleNumberFilter.bind(this);
    this.state = {
      allInputParams: this.props.allInputParams,
      allMetrics: this.props.allMetrics,
      jobs: this.props.jobs,
      isShowingUserFilter: false,
      updateHiddenUser: this.props.updateHiddenUser,
      isShowingStatusFilter: false,
      updateHiddenStatus: this.props.updateHiddenStatus,
      isShowingDurationFilter: false,
      isShowingNumberFilter: true,
      statuses: this.props.statuses,
      rowNumbers: this.props.rowNumbers,
      jobRows: this.props.jobRows,
      searchText: '',
      allUsers: this.props.allUsers,
      hiddenUsers: this.props.hiddenUsers,
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
        allUsers: nextProps.allUsers,
        hiddenUsers: nextProps.hiddenUsers,
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

  toggleDurationFilter() {
    const { isShowingDurationFilter } = this.state;
    this.setState({ isShowingDurationFilter: !isShowingDurationFilter });
  }

  toggleNumberFilter() {
    const { isShowingNumberFilter } = this.state;
    this.setState({ isShowingNumberFilter: !isShowingNumberFilter });
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
      updateHiddenUser,
      allUsers,
      hiddenUsers,
      isShowingDurationFilter,
      isShowingNumberFilter,
    } = this.state;

    let userFilter = null;
    if (isShowingUserFilter) {
      const nameArray = CommonActions.getFlatArray(allUsers);
      const filteredUsers = CommonActions.formatColumns(nameArray, hiddenUsers, searchText);
      userFilter = (
        <UserFilter
          columns={filteredUsers}
          toggleShowingFilter={this.toggleUserFilter}
          changeHiddenParams={updateHiddenUser}
          searchUserFilter={this.searchUserFilter}
          hiddenInputParams={hiddenUsers}
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

    let durationFilter = null;
    if (isShowingDurationFilter) {
      durationFilter = (
        <DurationFilter
          toggleShowingFilter={this.toggleDurationFilter}
        />
      );
    }

    let numberFilter = null;
    if (isShowingNumberFilter) {
      numberFilter = (
        <NumberFilter
          toggleShowingFilter={this.toggleDurationFilter}
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
            toggleDurationFilter={this.toggleDurationFilter}
          />
          <InputMetric
            header="input parameter"
            allInputParams={allInputParams}
            jobs={jobs}
            toggleNumberFilter={this.toggleNumberFilter}
          />
          <InputMetric
            header="metrics"
            allInputParams={allMetrics}
            jobs={jobs}
            isMetric={isMetric}
            toggleNumberFilter={this.toggleNumberFilter}
          />
          {userFilter}
          {statusFilter}
          {durationFilter}
          {numberFilter}
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
  updateHiddenUser: PropTypes.func,
  isShowingStatusFilter: PropTypes.bool,
  updateHiddenStatus: PropTypes.func,
  statuses: PropTypes.array,
  rowNumbers: PropTypes.array,
  jobRows: PropTypes.array,
  allUsers: PropTypes.array,
  hiddenUsers: PropTypes.array,
  isShowingDurationFilter: PropTypes.bool,
  isShowingNumberFilter: PropTypes.bool,
};

JobTableHeader.defaultProps = {
  allInputParams: [],
  jobs: [],
  allMetrics: [],
  isShowingUserFilter: false,
  updateHiddenUser: () => {},
  isShowingStatusFilter: false,
  updateHiddenStatus: () => {},
  statuses: [],
  rowNumbers: [],
  jobRows: [],
  allUsers: [],
  hiddenUsers: [],
  isShowingDurationFilter: false,
  isShowingNumberFilter: false,
};

export default JobTableHeader;
