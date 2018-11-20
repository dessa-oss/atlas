import React, { Component } from 'react';
import PropTypes from 'prop-types';
import TableSectionHeader from './TableSectionHeader';
import CommonActions from '../../actions/CommonActions';

const notFound = -1;
const oneElement = 1;

class InputMetric extends Component {
  constructor(props) {
    super(props);
    this.resizeCells = this.resizeCells.bind(this);
    this.isCellWidthSame = this.isCellWidthSame.bind(this);
    this.changeHiddenParams = this.changeHiddenParams.bind(this);
    this.state = {
      header: this.props.header,
      hiddenInputParams: [],
      allInputParams: this.props.allInputParams,
      jobs: [],
      cellWidths: new Array(this.props.allInputParams.length),
      isMetric: this.props.isMetric,
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

  changeHiddenParams(colName) {
    const { hiddenInputParams } = this.state;
    const index = hiddenInputParams.indexOf(colName);
    let newArray = [];
    if (index !== notFound) {
      hiddenInputParams.splice(index, oneElement);
    } else {
      hiddenInputParams.push(colName);
    }
    newArray = hiddenInputParams;
    this.setState({ hiddenInputParams: newArray });
  }

  render() {
    const {
      header, hiddenInputParams, allInputParams, jobs, cellWidths, isMetric,
    } = this.state;

    const inputParams = CommonActions.getInputMetricColumnHeaders(allInputParams, this.resizeCells);
    const rows = CommonActions.getInputMetricRows(jobs, cellWidths, isMetric, allInputParams);

    return (
      <div className="input-metric-container">
        <TableSectionHeader
          header={header}
          hiddenInputParams={hiddenInputParams}
          changeHiddenParams={this.changeHiddenParams}
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
};

InputMetric.defaultProps = {
  header: '',
  hiddenInputParams: [],
  allInputParams: [],
  jobs: [],
  cellWidths: [],
  isMetric: false,
};


export default InputMetric;
