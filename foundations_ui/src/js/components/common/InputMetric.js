import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { ScrollSyncPane } from 'react-scroll-sync';
import TableSectionHeader from './TableSectionHeader';
import CommonActions from '../../actions/CommonActions';

class InputMetric extends Component {
  constructor(props) {
    super(props);
    this.changeHiddenParams = this.changeHiddenParams.bind(this);
    this.updateSearchText = this.updateSearchText.bind(this);
    this.state = {
      header: this.props.header,
      hiddenInputParams: [],
      allInputParams: this.props.allInputParams,
      jobs: [],
      isMetric: this.props.isMetric,
      searchText: '',
      toggleNumberFilter: this.props.toggleNumberFilter,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({
      allInputParams: nextProps.allInputParams,
      jobs: nextProps.jobs,
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

  render() {
    const {
      header, hiddenInputParams, allInputParams, jobs, isMetric, searchText, toggleNumberFilter,
    } = this.state;


    const inputParams = CommonActions.getInputMetricColumnHeaders(
      allInputParams, hiddenInputParams, toggleNumberFilter,
    );
    const rows = CommonActions.getInputMetricRows(jobs, isMetric, allInputParams, hiddenInputParams);

    return (
      <div className="job-static-columns-container">
        <TableSectionHeader
          header={header}
          changeHiddenParams={this.changeHiddenParams}
          columns={allInputParams}
          hiddenInputParams={hiddenInputParams}
          updateSearchText={this.updateSearchText}
          searchText={searchText}
          isMetric={isMetric}
          toggleNumberFilter={toggleNumberFilter}
        />
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
  header: PropTypes.string,
  hiddenInputParams: PropTypes.array,
  allInputParams: PropTypes.array,
  jobs: PropTypes.array,
  cellWidths: PropTypes.array,
  isMetric: PropTypes.bool,
  searchText: PropTypes.string,
  toggleNumberFilter: PropTypes.func,
};

InputMetric.defaultProps = {
  header: '',
  hiddenInputParams: [],
  allInputParams: [],
  jobs: [],
  cellWidths: [],
  isMetric: false,
  searchText: '',
  toggleNumberFilter: () => {},
};


export default InputMetric;
