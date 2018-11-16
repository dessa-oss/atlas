import React from 'react';
import JobColumnHeader from '../components/common/JobColumnHeader';
import InputMetricCell from '../components/common/InputMetricCell';
import InputMetricRow from '../components/common/InputMetricRow';
import JobActions from './JobListActions';

class CommonActions {
  // Helper Functions
  static getInputMetricColumnHeaders(allInputParams, resizeCells) {
    let inputParams = null;
    if (allInputParams.length > 0) {
      let colIndex = 0;
      inputParams = [];
      allInputParams.forEach((input) => {
        const key = input;
        inputParams.push(<JobColumnHeader
          key={key}
          title={input}
          className="inline-block"
          containerClass="input-metric-column-header"
          sizeCallback={resizeCells}
          colIndex={colIndex}
        />);
        colIndex += 1;
      });
    }
    return inputParams;
  }

  static getTableSectionHeaderDiv(header) {
    let divClass = 'table-section-header';
    if (this.isHeaderNotEmpty(header)) {
      divClass = 'table-section-header blue-header';
    }
    return divClass;
  }

  static getTableSectionHeaderArrow(header) {
    let arrowClass = '';
    if (this.isHeaderNotEmpty(header)) {
      arrowClass = 'arrow-down blue-header-arrow border-top-white border-left-clear border-right-clear';
    }
    return arrowClass;
  }

  static getTableSectionHeaderText(header) {
    let textClass = 'blue-header-text font-regular white-text no-margin';
    if (this.isHeaderNotEmpty(header)) {
      textClass = 'blue-header-text font-regular white-text';
    }
    return textClass;
  }

  static isHeaderNotEmpty(header) {
    return header !== '';
  }

  static getInputMetricCells(job, cellWidths, isError) {
    let cells = null;
    if (job.input_params && job.input_params.length > 0) {
      cells = [];
      let colIndex = 0;
      job.input_params.forEach((input) => {
        if (input.value.type === 'constant') {
          const cellWidth = cellWidths[colIndex];
          const inputValue = JobActions.getInputParamValue(input);
          cells.push(<InputMetricCell key={input.name} cellWidth={cellWidth} value={inputValue} isError={isError} />);
          colIndex += 1;
        }
      });
    }
    return cells;
  }

  static getInputMetricRows(jobs, cellWidths) {
    let rows = null;
    if (jobs.length > 0) {
      rows = [];
      jobs.forEach((job) => {
        const key = job.job_id.concat('-input-metric-row');
        const isError = job.status.toLowerCase() === 'error';
        rows.push(<InputMetricRow key={key} job={job} cellWidths={cellWidths} isError={isError} />);
      });
    }
    return rows;
  }
}

export default CommonActions;
