import React from 'react';
import JobColumnHeader from '../components/common/JobColumnHeader';
import InputMetricCell from '../components/common/InputMetricCell';
import InputMetricRow from '../components/common/InputMetricRow';

class CommonActions {
  // Helper Functions
  static getInputMetricColumnHeaders(allInputParams, resizeCells) {
    let inputParams = null;
    if (allInputParams.length > 0) {
      let colIndex = 0;
      inputParams = [];
      allInputParams.forEach((input) => {
        const key = input;
        inputParams.push(<JobColumnHeader key={key} title={input} className="inline-block" containerClass="input-metric-column-header" sizeCallback={resizeCells} colIndex={colIndex} />);
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
      arrowClass = 'arrow-down blue-header-arrow';
    }
    return arrowClass;
  }

  static getTableSectionHeaderText(header) {
    let textClass = 'blue-header-text font-regular no-margin';
    if (this.isHeaderNotEmpty(header)) {
      textClass = 'blue-header-text font-regular';
    }
    return textClass;
  }

  static isHeaderNotEmpty(header) {
    return header !== '';
  }

  static getInputMetricCells(job, cellWidths) {
    let cells = null;
    if (job.input_params && job.input_params.length > 0) {
      cells = [];
      let colIndex = 0;
      job.input_params.forEach((input) => {
        const cellWidth = cellWidths[colIndex];
        cells.push(<InputMetricCell key={input.name} cellWidth={cellWidth} />);
        colIndex += 1;
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
        rows.push(<InputMetricRow key={key} job={job} cellWidths={cellWidths} />);
      });
    }
    return rows;
  }
}

export default CommonActions;
