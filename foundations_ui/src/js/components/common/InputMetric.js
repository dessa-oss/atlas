import React, { Component } from 'react';
import PropTypes from 'prop-types';
import TableSectionHeader from './TableSectionHeader';
import CommonActions from '../../actions/CommonActions';

class InputMetric extends Component {
  constructor(props) {
    super(props);
    this.resizeCells = this.resizeCells.bind(this);
    this.isCellWidthSame = this.isCellWidthSame.bind(this);
    this.changeHiddenParams = this.changeHiddenParams.bind(this);
    this.updateSearchText = this.updateSearchText.bind(this);
    this.state = {
      header: this.props.header,
      hiddenInputParams: [],
      allInputParams: this.props.allInputParams,
      jobs: [],
      cellWidths: new Array(this.props.allInputParams.length),
      isMetric: this.props.isMetric,
      searchText: '',
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({
      allInputParams: nextProps.allInputParams,
      jobs: nextProps.jobs,
      cellWidths: new Array(nextProps.allInputParams.length),
    });
  }

  resizeCells(colIndex, newWidth) {
    const { cellWidths } = this.state;
    if (this.isCellWidthSame(cellWidths[colIndex], newWidth)) {
      cellWidths[colIndex] = newWidth;
      this.forceUpdate();
    }
  }

  isCellWidthSame(oldWidth, newWidth) {
    return (oldWidth !== newWidth);
  }

  changeHiddenParams(hiddenParams) {
    this.setState({ hiddenInputParams: hiddenParams });
    this.forceUpdate();
  }

  updateSearchText(text) {
    this.setState({ searchText: text });
  }

  render() {
    const {
      header, hiddenInputParams, allInputParams, jobs, cellWidths, isMetric, searchText,
    } = this.state;


    const inputParams = CommonActions.getInputMetricColumnHeaders(allInputParams, this.resizeCells, hiddenInputParams);
    const rows = CommonActions.getInputMetricRows(jobs, cellWidths, isMetric, allInputParams, hiddenInputParams);

    return (
      <div className="input-metric-container">
        <TableSectionHeader
          header={header}
          changeHiddenParams={this.changeHiddenParams}
          columns={allInputParams}
          hiddenInputParams={hiddenInputParams}
        />
        <div className="input-metric-column-header-container">
          {inputParams}
          {rows}
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
};

InputMetric.defaultProps = {
  header: '',
  hiddenInputParams: [],
  allInputParams: [],
  jobs: [],
  cellWidths: [],
  isMetric: false,
  searchText: '',
};


export default InputMetric;
