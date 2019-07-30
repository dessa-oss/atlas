import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { ScrollSync } from 'react-scroll-sync';
import InputMetric from '../common/InputMetric';
import UserFilter from '../common/filters/UserFilter';
import StatusFilter from '../common/filters/StatusFilter';
import DurationFilter from '../common/filters/DurationFilter';
import NumberFilter from '../common/filters/NumberFilter';
import ContainsFilter from '../common/filters/ContainsFilter';
import DateTimeFilter from '../common/filters/DateTimeFilter';
import CommonActions from '../../actions/CommonActions';
import JobListActions from '../../actions/JobListActions';
import CancelJobCell from './cells/CancelJobCell';
import StatusCell from './cells/StatusCell';
import StartTimeCell from './cells/StartTimeCell';
import DurationCell from './cells/DurationCell';
import JobIDCell from './cells/JobIDCell';

const isMetric = true;

class JobTableHeader extends Component {
  constructor(props) {
    super(props);
    this.onMetricRowClick = props.onMetricRowClick.bind(this);
    this.toggleUserFilter = this.toggleUserFilter.bind(this);
    this.searchUserFilter = this.searchUserFilter.bind(this);
    this.toggleStatusFilter = this.toggleStatusFilter.bind(this);
    this.toggleDurationFilter = this.toggleDurationFilter.bind(this);
    this.toggleInputMetricFilter = this.toggleInputMetricFilter.bind(this);
    this.getColumnType = this.getColumnType.bind(this);
    this.getColumnName = this.getColumnName.bind(this);
    this.getMetricClass = this.getMetricClass.bind(this);
    this.getRangeFilterValues = this.getRangeFilterValues.bind(this);
    this.toggleJobIdFilter = this.toggleJobIdFilter.bind(this);
    this.toggleStartTimeFilter = this.toggleStartTimeFilter.bind(this);
    this.hideOtherFilters = this.hideOtherFilters.bind(this);
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
      updateNumberFilter: this.props.updateNumberFilter,
      numberFilterColumn: '',
      isShowingBooleanFilter: false,
      updateBoolFilter: this.props.updateBoolFilter,
      isShowingJobIdFilter: false,
      isShowingStartTimeFilter: false,
      statuses: this.props.statuses,
      rowNumbers: this.props.rowNumbers,
      jobRows: this.props.jobRows,
      searchText: '',
      allUsers: this.props.allUsers,
      hiddenUsers: this.props.hiddenUsers,
      boolCheckboxes: this.props.boolCheckboxes,
      numberFilters: this.props.numberFilters,
      containFilters: this.props.containFilters,
      boolFilters: this.props.boolFilters,
      updateDurationFilter: this.props.updateDurationFilter,
      durationFilters: this.props.durationFilters,
      updateJobIdFilter: this.props.updateJobIdFilter,
      jobIdFilters: this.props.jobIdFilters,
      updateStartTimeFilter: this.props.updateStartTimeFilter,
      startTimeFilters: this.props.startTimeFilters,
      filters: this.props.filters,
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
        boolFilters: nextProps.boolFilters,
        durationFilters: nextProps.durationFilters,
        jobIdFilters: nextProps.jobIdFilters,
        startTimeFilters: nextProps.startTimeFilters,
        filters: nextProps.filters,
      },
    );
  }

  searchUserFilter(searchText) {
    this.setState({ searchText });
  }

  toggleStatusFilter() {
    const { isShowingStatusFilter } = this.state;
    this.setState({ isShowingStatusFilter: !isShowingStatusFilter });
    this.hideOtherFilters('Status');
  }

  toggleDurationFilter() {
    const { isShowingDurationFilter } = this.state;
    this.setState({ isShowingDurationFilter: !isShowingDurationFilter });
    this.hideOtherFilters('Duration');
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
    this.hideOtherFilters('User');
  }

  toggleJobIdFilter() {
    const { isShowingJobIdFilter } = this.state;
    this.setState({ isShowingJobIdFilter: !isShowingJobIdFilter });
    this.hideOtherFilters('Job');
  }

  toggleStartTimeFilter() {
    const { isShowingStartTimeFilter } = this.state;
    this.setState({ isShowingStartTimeFilter: !isShowingStartTimeFilter });
    this.hideOtherFilters('StartTime');
  }

  toggleInputMetricFilter(e) {
    const {
      numberFilterColumn,
    } = this.state;
    let columnName = this.getColumnName(e);
    let columnType = this.getColumnType(e);
    let metricClass = this.getMetricClass(e);

    if (columnType === 'number') {
      this.hideOtherFilters('Number');
      if (numberFilterColumn === columnName) {
        this.setState({
          isShowingNumberFilter: false,
        });
      } else {
        this.setState({
          isShowingNumberFilter: true,
        });
      }
    } else if (columnType === 'string') {
      this.hideOtherFilters('Contains');
      if (numberFilterColumn === columnName) {
        this.setState({
          isShowingContainsFilter: false,
        });
      } else {
        this.setState({
          isShowingContainsFilter: true,
        });
      }
    } else if (columnType === 'bool') {
      this.hideOtherFilters('Boolean');
      if (numberFilterColumn === columnName) {
        this.setState({
          isShowingBooleanFilter: false,
        });
      } else {
        this.setState({
          isShowingBooleanFilter: true,
        });
      }
    }

    if (e !== undefined) {
      this.setState({
        metricClass,
      });
      if (numberFilterColumn === columnName) {
        this.setState({
          numberFilterColumn: '',
        });
      } else {
        this.setState({
          numberFilterColumn: columnName,
        });
      }
    } else if (e === undefined) {
      // This means it's an apply/cancel button rather than a header arrow
      // so close everything
      this.setState({
        isShowingNumberFilter: false,
        isShowingContainsFilter: false,
        isShowingBooleanFilter: false,
        numberFilterColumn: '',
      });
    }
  }

  getRangeFilterValues() {
    const { numberFilters, numberFilterColumn } = this.state;
    const existingFilter = JobListActions.getExistingValuesForFilter(numberFilters, numberFilterColumn);
    let curMin = 0;
    let curMax = 0;
    if (existingFilter) {
      curMin = existingFilter.min;
      curMax = existingFilter.max;
    }
    return { min: curMin, max: curMax };
  }

  hideOtherFilters(filterToShow) {
    if (filterToShow !== 'Duration') {
      this.setState({
        isShowingDurationFilter: false,
      });
    }
    if (filterToShow !== 'Number') {
      this.setState({
        isShowingNumberFilter: false,
      });
    }
    if (filterToShow !== 'Contains') {
      this.setState({
        isShowingContainsFilter: false,
      });
    }
    if (filterToShow !== 'Boolean') {
      this.setState({
        isShowingBooleanFilter: false,
      });
    }
    if (filterToShow !== 'Job') {
      this.setState({
        isShowingJobIdFilter: false,
      });
    }
    if (filterToShow !== 'StartTime') {
      this.setState({
        isShowingStartTimeFilter: false,
      });
    }
    if (filterToShow !== 'User') {
      this.setState({
        isShowingUserFilter: false,
      });
    }
    if (filterToShow !== 'Status') {
      this.setState({
        isShowingStatusFilter: false,
      });
    }
  }

  getStaticJobsInputParams() {
    return [
      { name: '', type: 'string' },
      { name: 'Job ID', type: 'string' },
      { name: 'Launched At', type: 'string' },
      { name: 'Status', type: 'string', hoverable: false },
      { name: 'Duration', type: 'string' },
      { name: 'User', type: 'string' },
    ];
  }

  generateStaticJobs(jobs) {
    return jobs.map((el) => {
      const neededColums = [];

      neededColums.push({
        name: '',
        value: CancelJobCell({ job: el }),
        type: 'string',
        hoverable: false,
      });
      neededColums.push({
        name: 'Job ID',
        value: new JobIDCell({ jobID: el.job_id }).render(),
        type: 'string',
      });
      neededColums.push({
        name: 'Launched At',
        value: new StartTimeCell({ startTime: el.start_time }).render(),
        type: 'string',
      });
      neededColums.push({
        name: 'Status',
        value: new StatusCell(el).render(),
        type: 'string',
        hoverable: false,
      });
      neededColums.push({
        name: 'Duration',
        value: new DurationCell({
          duration: JobListActions.parseDuration(el.duration),
        }).render(),
        type: 'string',
        hoverable: false,
      });
      neededColums.push({
        name: 'User',
        value: el.user,
        type: 'string',
      });
      const job = Object.assign({}, el);
      job.output_metrics = neededColums;
      return job;
    });
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
      boolCheckboxes,
      isShowingDurationFilter,
      isShowingNumberFilter,
      isShowingContainsFilter,
      isShowingBooleanFilter,
      isShowingJobIdFilter,
      isShowingStartTimeFilter,
      numberFilterColumn,
      updateNumberFilter,
      metricClass,
      updateContainsFilter,
      containFilters,
      boolFilters,
      updateBoolFilter,
      updateDurationFilter,
      durationFilters,
      updateJobIdFilter,
      jobIdFilters,
      updateStartTimeFilter,
      startTimeFilters,
      filters,
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
    hiddenInputParams = statuses.map(
      (status) => {
        if (status.hidden === true && status.hidden !== undefined) {
          return status.name;
        }
      },
    );
    if (isShowingStatusFilter) {
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
      const existingFilter = JobListActions.getExistingValuesForFilter(durationFilters, 'Duration');
      let startValue = {
        days: '0', hours: '0', minutes: '0', seconds: '0',
      };
      let endValue = {
        days: '0', hours: '0', minutes: '0', seconds: '0',
      };
      if (existingFilter) {
        startValue = existingFilter.startTime;
        endValue = existingFilter.endTime;
      }
      durationFilter = (
        <DurationFilter
          toggleShowingFilter={this.toggleDurationFilter}
          changeHiddenParams={updateDurationFilter}
          startTime={startValue}
          endTime={endValue}
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
      const existingFilter = JobListActions.getExistingValuesForFilter(containFilters, numberFilterColumn);
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
    let changedBoolParams = [];
    let boolColumns = CommonActions.deepCopyArray(boolCheckboxes);
    if (isShowingBooleanFilter) {
      const existingFilter = JobListActions.getExistingValuesForFilter(boolFilters, numberFilterColumn);
      if (existingFilter) {
        boolColumns = existingFilter.boolCheckboxes;
        changedBoolParams = JobListActions.boolFilterGetHidden(existingFilter.boolCheckboxes);
      }
      // booleanFilter = (
      //   <BooleanFilter
      //     toggleShowingFilter={this.toggleInputMetricFilter}
      //     columnName={numberFilterColumn}
      //     changeHiddenParams={updateBoolFilter}
      //     metricClass={metricClass}
      //     columns={boolColumns}
      //     changedParams={changedBoolParams}
      //   />
      // );
    }

    let jobIDFilter = null;
    if (isShowingJobIdFilter) {
      const existingFilter = JobListActions.getExistingValuesForFilter(jobIdFilters, 'Job Id');
      let containString = '';
      if (existingFilter) {
        containString = existingFilter.searchText;
      }
      jobIDFilter = (
        <ContainsFilter
          toggleShowingFilter={this.toggleJobIdFilter}
          columnName={numberFilterColumn}
          changeHiddenParams={updateJobIdFilter}
          metricClass="job-id-filter"
          filterString={containString}
        />
      );
    }

    let startFilter = null;
    if (isShowingStartTimeFilter) {
      const existingFilter = JobListActions.getExistingValuesForFilter(startTimeFilters, 'Start Time');
      let startDate = null;
      let endDate = null;
      if (existingFilter) {
        startDate = new Date(existingFilter.startTime);
        endDate = new Date(existingFilter.endTime);
      }
      startFilter = (
        <DateTimeFilter
          toggleShowingFilter={this.toggleStartTimeFilter}
          changeHiddenParams={updateStartTimeFilter}
          startDate={startDate}
          endDate={endDate}
        />
      );
    }

    hiddenInputParams = hiddenInputParams.filter((hiddenParam) => {
      return hiddenParam !== undefined;
    });

    const jobsInputParams = this.getStaticJobsInputParams();

    const jobsMetaData = this.generateStaticJobs(jobs);

    return (
      <ScrollSync>
        <div className="job-list-container">
          <InputMetric
            header="Job Details"
            allInputParams={jobsInputParams}
            jobs={jobsMetaData}
            isMetric={isMetric}
            toggleNumberFilter={this.toggleInputMetricFilter}
            filters={filters}
            onMetricRowClick={this.onMetricRowClick}
          />
          <InputMetric
            header="Parameters"
            allInputParams={allInputParams}
            jobs={jobs}
            toggleNumberFilter={this.toggleInputMetricFilter}
            filters={filters}
          />
          <InputMetric
            header="Metrics"
            allInputParams={allMetrics}
            jobs={jobs}
            isMetric={isMetric}
            toggleNumberFilter={this.toggleInputMetricFilter}
            filters={filters}
          />
          {userFilter}
          {statusFilter}
          {durationFilter}
          {numberFilter}
          {containsFilter}
          {booleanFilter}
          {jobIDFilter}
          {startFilter}
        </div>
      </ScrollSync>
    );
  }
}

JobTableHeader.propTypes = {
  onMetricRowClick: PropTypes.func,
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
  boolCheckboxes: PropTypes.array,
  boolFilters: PropTypes.array,
  updateBoolFilter: PropTypes.func,
  updateDurationFilter: PropTypes.func,
  durationFilters: PropTypes.array,
  isShowingJobIdFilter: PropTypes.bool,
  updateJobIdFilter: PropTypes.func,
  jobIdFilters: PropTypes.array,
  isShowingStartTimeFilter: PropTypes.bool,
  updateStartTimeFilter: PropTypes.func,
  startTimeFilters: PropTypes.array,
  filters: PropTypes.array,
};

const defaultFunc = () => console.warn('JobTableHeader: Missing onMetricRowClick prop.');
JobTableHeader.defaultProps = {
  onMetricRowClick: defaultFunc,
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
  boolCheckboxes: [],
  boolFilters: [],
  updateBoolFilter: () => {},
  updateDurationFilter: () => {},
  durationFilters: [],
  isShowingJobIdFilter: false,
  updateJobIdFilter: () => {},
  jobIdFilters: [],
  isShowingStartTimeFilter: false,
  updateStartTimeFilter: () => {},
  startTimeFilters: [],
  filters: [],
};

export default JobTableHeader;
