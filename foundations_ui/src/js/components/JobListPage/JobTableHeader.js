import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { ScrollSync } from 'react-scroll-sync';
import TableStaticColumns from './TableStaticColumns';
import InputMetric from '../common/InputMetric';
import UserFilter from '../common/filters/UserFilter';
import StatusFilter from '../common/filters/StatusFilter';
import DurationFilter from '../common/filters/DurationFilter';
import NumberFilter from '../common/filters/NumberFilter';
import ContainsFilter from '../common/filters/ContainsFilter';
import BooleanFilter from '../common/filters/BooleanFilter';
import CommonActions from '../../actions/CommonActions';
import JobActions from '../../actions/JobListActions';

const isMetric = true;

class JobTableHeader extends Component {
  constructor(props) {
    super(props);
    this.toggleUserFilter = this.toggleUserFilter.bind(this);
    this.searchUserFilter = this.searchUserFilter.bind(this);
    this.toggleStatusFilter = this.toggleStatusFilter.bind(this);
    this.toggleDurationFilter = this.toggleDurationFilter.bind(this);
    this.toggleInputMetricFilter = this.toggleInputMetricFilter.bind(this);
    this.getColumnType = this.getColumnType.bind(this);
    this.getColumnName = this.getColumnName.bind(this);
    this.getMetricClass = this.getMetricClass.bind(this);
    this.getRangeFilterValues = this.getRangeFilterValues.bind(this);
    this.state = {
      allInputParams: this.props.allInputParams,
      allMetrics: this.props.allMetrics,
      jobs: this.props.jobs,
      isShowingUserFilter: false,
      updateHiddenUser: this.props.updateHiddenUser,
      isShowingStatusFilter: false,
      updateHiddenStatus: this.props.updateHiddenStatus,
      isShowingDurationFilter: false,
      isShowingContainsFilter: false,
      updateContainsFilter: this.props.updateContainsFilter,
      metricClass: '',
      isShowingNumberFilter: false,
      numberFilterColumn: '',
      isShowingBooleanFilter: false,
      statuses: this.props.statuses,
      rowNumbers: this.props.rowNumbers,
      jobRows: this.props.jobRows,
      searchText: '',
      allUsers: this.props.allUsers,
      hiddenUsers: this.props.hiddenUsers,
      updateNumberFilter: this.props.updateNumberFilter,
      numberFilters: this.props.numberFilters,
      containFilters: this.props.containFilters,
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
        numberFilters: nextProps.numberFilters,
        containFilters: nextProps.containFilters,
      },
    );
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

  getColumnType(e) {
    let columnType = '';
    if (e) {
      if (e.target.className.includes('number')) {
        columnType = 'number';
      } else if (e.target.className.includes('string')) {
        columnType = 'string';
      } else if (e.target.className.includes('bool')) {
        columnType = 'bool';
      }
    }
    return columnType;
  }

  getColumnName(e) {
    let columnName = '';
    if (e) {
      if (e.target.id) {
        columnName = e.target.id;
      } else {
        columnName = e.target.childNodes[0].id;
      }
    }
    return columnName;
  }

  getMetricClass(e) {
    let metricClass = 'not-metric';
    if (e) {
      if (e.target.className.includes('is-metric')) {
        metricClass = 'is-metric';
      }
    }
    return metricClass;
  }

  toggleUserFilter() {
    const { isShowingUserFilter } = this.state;
    this.setState({ isShowingUserFilter: !isShowingUserFilter });
  }

  toggleInputMetricFilter(e) {
    const { isShowingNumberFilter, isShowingContainsFilter, isShowingBooleanFilter } = this.state;
    let columnName = this.getColumnName(e);
    let columnType = this.getColumnType(e);
    let metricClass = this.getMetricClass(e);

    if (columnType === 'number') {
      this.setState({
        isShowingNumberFilter: !isShowingNumberFilter,
        numberFilterColumn: columnName,
        metricClass,
      });
    } else if (columnType === 'string') {
      this.setState({
        isShowingContainsFilter: !isShowingContainsFilter,
        numberFilterColumn: columnName,
        metricClass,
      });
    } else if (columnType === 'bool') {
      this.setState({
        isShowingBooleanFilter: !isShowingBooleanFilter,
        numberFilterColumn: columnName,
        metricClass,
      });
    } else if (e === undefined) {
      // This means it's an apply/cancel button rather than a header arrow
      // so close everything
      this.setState({
        isShowingNumberFilter: false,
        isShowingContainsFilter: false,
      });
    }
  }

  getRangeFilterValues() {
    const { numberFilters, numberFilterColumn } = this.state;
    const existingFilter = JobActions.getExistingValuesForFilter(numberFilters, numberFilterColumn);
    let curMin = 0;
    let curMax = 0;
    if (existingFilter) {
      curMin = existingFilter.min;
      curMax = existingFilter.max;
    }
    return { min: curMin, max: curMax };
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
      isShowingContainsFilter,
      isShowingBooleanFilter,
      numberFilterColumn,
      updateNumberFilter,
      metricClass,
      updateContainsFilter,
      containFilters,
    } = this.state;

    let userFilter = null;
    if (isShowingUserFilter) {
      const filteredUsers = CommonActions.formatColumns(allUsers, hiddenUsers, searchText);
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
      const filterValues = this.getRangeFilterValues();
      numberFilter = (
        <NumberFilter
          toggleShowingFilter={this.toggleInputMetricFilter}
          columnName={numberFilterColumn}
          changeHiddenParams={updateNumberFilter}
          minValue={filterValues.min}
          maxValue={filterValues.max}
          metricClass={metricClass}
        />
      );
    }

    let containsFilter = null;
    if (isShowingContainsFilter) {
      const existingFilter = JobActions.getExistingValuesForFilter(containFilters, numberFilterColumn);
      let containString = '';
      if (existingFilter) {
        containString = existingFilter.searchText;
      }
      containsFilter = (
        <ContainsFilter
          toggleShowingFilter={this.toggleInputMetricFilter}
          columnName={numberFilterColumn}
          changeHiddenParams={updateContainsFilter}
          metricClass={metricClass}
          filterString={containString}
        />
      );
    }

    let booleanFilter = null;
    if (isShowingBooleanFilter) {
      booleanFilter = (
        <BooleanFilter
          toggleShowingFilter={this.toggleInputMetricFilter}
          columnName={numberFilterColumn}
          changeHiddenParams={updateContainsFilter}
          metricClass={metricClass}
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
            toggleNumberFilter={this.toggleInputMetricFilter}
          />
          <InputMetric
            header="metrics"
            allInputParams={allMetrics}
            jobs={jobs}
            isMetric={isMetric}
            toggleNumberFilter={this.toggleInputMetricFilter}
          />
          {userFilter}
          {statusFilter}
          {durationFilter}
          {numberFilter}
          {containsFilter}
          {booleanFilter}
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
  numberFilterColumn: PropTypes.string,
  updateNumberFilter: PropTypes.func,
  numberFilters: PropTypes.array,
  metricClass: PropTypes.string,
  isShowingContainsFilter: PropTypes.bool,
  updateContainsFilter: PropTypes.func,
  containFilters: PropTypes.array,
  isShowingBooleanFilter: PropTypes.bool,
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
  numberFilterColumn: '',
  updateNumberFilter: () => {},
  numberFilters: [],
  metricClass: 'not-metric',
  isShowingContainsFilter: false,
  updateContainsFilter: () => {},
  containFilters: [],
  isShowingBooleanFilter: false,
};

export default JobTableHeader;
