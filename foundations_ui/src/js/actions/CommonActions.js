import React from 'react';
import JobColumnHeader from '../components/common/JobColumnHeader';
import InputMetricCell from '../components/common/InputMetricCell';
import InputMetricRow from '../components/common/InputMetricRow';
import JobActions from './JobListActions';

class CommonActions {
  // Helper Functions
  static getInputMetricColumnHeaders(allInputParams, resizeCells) {
    if (allInputParams.length > 0) {
      return this.getInputParamHeaders(allInputParams, resizeCells);
    }
    return null;
  }

  static getInputParamHeaders(allInputParams, resizeCells) {
    const inputParams = [];
    let colIndex = 0;
    allInputParams.forEach((input) => {
      const key = input;
      inputParams.push(<JobColumnHeader
        key={key}
        title={input}
        className="inline-block"
        containerClass="job-column-header"
        sizeCallback={resizeCells}
        colIndex={colIndex}
      />);
      colIndex += 1;
    });
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
      arrowClass = 'blue-header-arrow border-input-metric-arrow';
    }
    return arrowClass;
  }

  static getTableSectionHeaderText(header) {
    let textClass = 'blue-header-text text-white no-margin';
    if (this.isHeaderNotEmpty(header)) {
      textClass = 'blue-header-text text-white';
    }
    return textClass;
  }

  static isHeaderNotEmpty(header) {
    return header !== '';
  }

  static getInputMetricCells(job, cellWidths, isError, isMetric, columns) {
    if (isMetric && job.output_metrics) {
      return this.getMetricCellsFromOutputMetrics(job, cellWidths, isError, columns, isMetric);
    }

    if (!isMetric && job.input_params && job.input_params.length > 0) {
      return this.getInputCellsFromInputParams(job, cellWidths, isError, columns, isMetric);
    }
    return null;
  }

  static getInputCellsFromInputParams(job, cellWidths, isError, columns, isMetric) {
    let cells = [];
    cells = [];
    let colIndex = 0;
    columns.forEach((col) => {
      let input = {
        value: {
          type: 'constant',
        },
      };
      job.input_params.forEach((param) => {
        if (param.name === col) {
          input = param;
        }
      });
      let key = 'input-param-'.concat(colIndex);
      if (input && input.name) {
        key = input.name;
      }
      if (input.value.type === 'constant') {
        const cellWidth = cellWidths[colIndex];
        const inputValue = JobActions.getInputMetricValue(input, isMetric, columns);
        cells.push(<InputMetricCell
          key={key}
          cellWidth={cellWidth}
          value={inputValue}
          isError={isError}
        />);
        colIndex += 1;
      }
    });
    return cells;
  }

  static getMetricCellsFromOutputMetrics(job, cellWidths, isError, columns, isMetric) {
    const cells = [];
    let colIndex = 0;
    columns.forEach((col) => {
      let input = null;
      if (job.output_metrics.data_set_name) {
        job.output_metrics.data_set_name.forEach((metric) => {
          if (metric === col) {
            input = metric;
          }
        });
      }
      const cellWidth = cellWidths[colIndex];
      const inputValue = JobActions.getInputMetricValue(input, isMetric, columns);
      let key = 'metric-'.concat(colIndex);
      if (input && input.name) {
        key = input.name;
      }
      cells.push(<InputMetricCell
        key={key}
        cellWidth={cellWidth}
        value={inputValue}
        isError={isError}
      />);
      colIndex += 1;
    });
    return cells;
  }

  static getInputMetricRows(jobs, cellWidths, isMetric, allInputMetricColumn) {
    let rows = null;
    if (jobs.length > 0) {
      rows = [];
      jobs.forEach((job) => {
        const key = job.job_id.concat('-input-metric-row');
        const isError = this.isError(job.status);
        rows.push(<InputMetricRow
          key={key}
          job={job}
          cellWidths={cellWidths}
          isError={isError}
          isMetric={isMetric}
          allInputMetricColumn={allInputMetricColumn}
        />);
      });
    }
    return rows;
  }

  static getInputMetricCellPClass(isError) {
    return isError ? 'font-bold error' : 'font-bold';
  }

  static getInputMetricCellDivClass(isError) {
    return isError ? 'job-cell error' : 'job-cell';
  }

  static isError(status) {
    return status.toLowerCase() === 'error';
  }
}

export default CommonActions;
