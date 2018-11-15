import React, { Component } from 'react';
import PropTypes from 'prop-types';
import TableSectionHeader from './TableSectionHeader';
import JobColumnHeader from './JobColumnHeader';
import InputMetricCell from './InputMetricCell';
import InputMetricRow from './InputMetricRow';

class InputMetric extends Component {
  constructor(props) {
    super(props);
    this.resizeCells = this.resizeCells.bind(this);
    this.state = {
      header: this.props.header,
      hiddenInputParams: this.props.hiddenInputParams,
      allInputParams: this.props.allInputParams,
      jobs: [],
      cellWidths: new Array(5),
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ allInputParams: nextProps.allInputParams, jobs: nextProps.jobs });
  }

  resizeCells(colIndex, newWidth) {
    const { cellWidths } = this.state;
    if (cellWidths[colIndex] !== newWidth) {
      cellWidths[colIndex] = newWidth;
      this.forceUpdate();
    }
  }

  render() {
    const {
      header, hiddenInputParams, allInputParams, jobs, cellWidths,
    } = this.state;

    let inputParams = null;
    if (allInputParams.length > 0) {
      let colIndex = 0;
      inputParams = [];
      allInputParams.forEach((input) => {
        const key = input;
        inputParams.push(
          <JobColumnHeader
            key={key}
            title={input}
            className="inline-block"
            containerClass="input-metric-column-header"
            sizeCallback={this.resizeCells}
            colIndex={colIndex}
          />,
        );
        colIndex += 1;
      });
    }

    let rows = null;
    if (jobs.length > 0) {
      rows = [];
      jobs.forEach((job) => {
        const key = job.job_id.concat('-input-metric-row');
        rows.push(<InputMetricRow key={key} job={job} cellWidths={cellWidths} />);
      });
    }

    return (
      <div className="input-metric-container">
        <TableSectionHeader header={header} />
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
};

InputMetric.defaultProps = {
  header: '',
  hiddenInputParams: [],
  allInputParams: [],
  jobs: [],
  cellWidths: [],
};


export default InputMetric;
