import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { ScrollSyncPane } from 'react-scroll-sync';
import TableSectionHeader from './TableSectionHeader';
import CommonActions from '../../actions/CommonActions';

class InputMetric extends Component {
  constructor(props) {
    super(props);
    this.onMetricRowClick = props.onMetricRowClick;
    this.changeHiddenParams = this.changeHiddenParams.bind(this);
    this.updateSearchText = this.updateSearchText.bind(this);
    this.hasNoRows = this.hasNoRows.bind(this);
    this.state = {
      header: this.props.header,
      hiddenInputParams: [],
      allInputParams: this.props.allInputParams,
      jobs: [],
      isMetric: this.props.isMetric,
      searchText: '',
      toggleNumberFilter: this.props.toggleNumberFilter,
      filteredArray: this.props.filters,
      isMetaData: this.props.isMetaData,
      sortedColumn: this.props.sortedColumn,
      sortTable: this.props.sortTable,
      selectAllJobs: this.props.selectAllJobs,
      selectedJobs: this.props.selectedJobs,
      allJobsSelected: this.props.allJobsSelected,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({
      allInputParams: nextProps.allInputParams,
      jobs: nextProps.jobs,
      filteredArray: nextProps.filters,
      sortedColumn: nextProps.sortedColumn,
      allJobsSelected: nextProps.allJobsSelected,
    });
  }

  changeHiddenParams(hiddenParams) {
    this.setState({ hiddenInputParams: hiddenParams });
    this.forceUpdate();
  }

  updateSearchText(text) {
    this.setState({ searchText: text });
    this.forceUpdate();
  }

  hasNoRows(rows, flatParams) {
    const { hiddenInputParams } = this.state;
    return rows === null || rows.length === 0 || flatParams.length === hiddenInputParams.length;
  }

  render() {
    const {
      header, hiddenInputParams, allInputParams, isMetaData,
      jobs, isMetric, searchText, toggleNumberFilter, filteredArray, sortedColumn, sortTable, selectAllJobs,
      selectedJobs, allJobsSelected,
    } = this.state;
    const { onClickOpenModalJobDetails } = this.props;
    const flatParams = CommonActions.getFlatArray(allInputParams);

    const inputParams = CommonActions.getInputMetricColumnHeaders(
      allInputParams, hiddenInputParams, toggleNumberFilter, isMetric, filteredArray, sortedColumn, sortTable,
      selectAllJobs, allJobsSelected,
    );

    let rows = CommonActions.getInputMetricRows(jobs, isMetric, flatParams, hiddenInputParams,
      this.onMetricRowClick, onClickOpenModalJobDetails, selectedJobs);

    if (this.hasNoRows(rows, flatParams)) {
      rows = [];
      if (isMetaData) {
        rows.push(<p key="no-rows-message" className="empty-columns-message">No jobs found</p>);
      } else {
        rows.push(<p key="no-rows-message" className="empty-columns-message">There are no columns selected.</p>);
      }
    }

    return (
      <div className="job-static-columns-container">
        <h2>{header}</h2>
        <div className="input-metric-header-row-container">
          <div className="input-metric-column-container column-header">
            {inputParams}
          </div>
          <ScrollSyncPane group="vertical">
            <div className="input-metric-column-container">
              {rows}
            </div>
          </ScrollSyncPane>
        </div>
      </div>
    );
  }
}

InputMetric.propTypes = {
  onMetricRowClick: PropTypes.func,
  header: PropTypes.string,
  hiddenInputParams: PropTypes.array,
  allInputParams: PropTypes.array,
  jobs: PropTypes.array,
  cellWidths: PropTypes.array,
  isMetric: PropTypes.bool,
  searchText: PropTypes.string,
  toggleNumberFilter: PropTypes.func,
  filters: PropTypes.array,
  isMetaData: PropTypes.bool,
  onClickOpenModalJobDetails: PropTypes.func,
  sortedColumn: PropTypes.object,
  sortTable: PropTypes.func,
  selectAllJobs: PropTypes.func,
  selectedJobs: PropTypes.array,
  allJobsSelected: PropTypes.bool,
};
const defaultFunc = () => console.warn('JobTableHeader: Missing onMetricRowClick prop.');
InputMetric.defaultProps = {
  onMetricRowClick: defaultFunc,
  header: '',
  hiddenInputParams: [],
  allInputParams: [],
  jobs: [],
  cellWidths: [],
  isMetric: false,
  searchText: '',
  toggleNumberFilter: () => {},
  filters: [],
  isMetaData: false,
  onClickOpenModalJobDetails: () => null,
  sortedColumn: { column: '', isAscending: true },
  sortTable: () => {},
  selectAllJobs: () => {},
  selectedJobs: [],
  allJobsSelected: false,
};


export default InputMetric;
