import React from 'react';
import JobColumnHeader from '../components/common/JobColumnHeader';
import InputMetricCell from '../components/common/InputMetricCell';
import InputMetricRow from '../components/common/InputMetricRow';
import Checkbox from '../components/common/Checkbox';
import JobActions from './JobListActions';

const notFound = -1;
const oneElement = 1;

class CommonActions {
  // Helper Functions
  static getInputMetricColumnHeaders(allInputParams, resizeCells, hiddenInputParams) {
    if (allInputParams.length > 0) {
      return this.getInputParamHeaders(allInputParams, resizeCells, hiddenInputParams);
    }
    return null;
  }

  static getInputParamHeaders(allInputParams, resizeCells, hiddenInputParams) {
    const inputParams = [];
    let colIndex = 0;
    allInputParams.forEach((input) => {
      if (this.arrayDoesNotInclude(hiddenInputParams, input)) {
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
      }
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

  static getInputMetricCells(job, cellWidths, isError, isMetric, columns, hiddenInputParams) {
    if (isMetric && job.output_metrics) {
      return this.getMetricCellsFromOutputMetrics(job, cellWidths, isError, columns, isMetric, hiddenInputParams);
    }

    if (!isMetric && job.input_params && job.input_params.length > 0) {
      return this.getInputCellsFromInputParams(job, cellWidths, isError, columns, isMetric, hiddenInputParams);
    }
    return null;
  }

  static getInputCellsFromInputParams(job, cellWidths, isError, columns, isMetric, hiddenInputParams) {
    let cells = [];
    cells = [];
    let colIndex = 0;
    columns.forEach((col) => {
      if (this.arrayDoesNotInclude(hiddenInputParams, col)) {
        const input = this.getInputMetricInput(job.input_params, col, isMetric);
        const key = this.getInputMetricKey(input, col, isMetric);
        if (this.isConstant(input)) {
          const cellWidth = cellWidths[colIndex];
          const inputValue = JobActions.getInputMetricValue(input, isMetric, columns);
          cells.push(<InputMetricCell
            key={key}
            cellWidth={cellWidth}
            value={inputValue}
            isError={isError}
          />);
        }
      } else {
        cells.push(null);
      }
      colIndex += 1;
    });
    return cells;
  }

  static getMetricCellsFromOutputMetrics(job, cellWidths, isError, columns, isMetric, hiddenInputParams) {
    const cells = [];
    let colIndex = 0;
    columns.forEach((col) => {
      if (this.arrayDoesNotInclude(hiddenInputParams, col)) {
        const input = this.getInputMetricInput(job.output_metrics.data_set_name, col, isMetric);
        const cellWidth = cellWidths[colIndex];
        const inputValue = JobActions.getInputMetricValue(input, isMetric, columns);
        const key = this.getInputMetricKey(input, col, isMetric);
        cells.push(<InputMetricCell
          key={key}
          cellWidth={cellWidth}
          value={inputValue}
          isError={isError}
        />);
      } else {
        cells.push(null);
      }
      colIndex += 1;
    });
    return cells;
  }

  static getInputMetricRows(jobs, cellWidths, isMetric, allInputMetricColumn, hiddenInputParams) {
    let rows = null;
    if (jobs.length > 0) {
      rows = [];
      jobs.forEach((job) => {
        const key = this.getRowKey(job);
        const isError = this.isError(job.status);
        rows.push(<InputMetricRow
          key={key}
          job={job}
          cellWidths={cellWidths}
          isError={isError}
          isMetric={isMetric}
          allInputMetricColumn={allInputMetricColumn}
          hiddenInputParams={hiddenInputParams}
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

  static formatColumns(columns, hiddenInputParams, searchText) {
    const formatedColumns = [];
    if (columns !== null) {
      columns.forEach((col) => {
        if (col.toLowerCase().includes(searchText.toLowerCase())) {
          let isHidden = false;
          if (hiddenInputParams.includes(col)) {
            isHidden = true;
          }
          formatedColumns.push({ name: col, hidden: isHidden });
        }
      });
    }
    return formatedColumns;
  }

  static getChangedCheckboxes(changedParams, colName) {
    const index = changedParams.indexOf(colName);
    const copyArray = this.deepCopyArray(changedParams);
    if (index !== notFound) {
      copyArray.splice(index, oneElement);
    } else {
      copyArray.push(colName);
    }
    return copyArray;
  }

  static getRowKey(job) {
    return job.job_id.concat('-input-metric-row');
  }

  // private functions, not cannot declare a private and static
  // function in JS https://stackoverflow.com/a/3218950
  static arrayDoesNotInclude(array, value) {
    return !array.includes(value);
  }

  static getInputMetricInput(jobArray, col, isMetric) {
    let input = null;
    if (!isMetric) {
      input = {
        value: {
          type: 'constant',
        },
      };
    }
    if (jobArray) {
      jobArray.forEach((param) => {
        if (!isMetric && param.name === col) {
          input = param;
        }
        if (isMetric && param === col) {
          input = param;
        }
      });
    }
    return input;
  }

  static getInputMetricKey(input, colIndex, isMetric) {
    if (isMetric) {
      let key = 'metric-'.concat(colIndex);
      if (input && input.name) {
        key = input.name;
      }
      return key;
    }
    let key = 'input-param-'.concat(colIndex);
    if (input && input.name) {
      key = input.name;
    }
    return key;
  }

  static isConstant(input) {
    return input.value.type === 'constant';
  }

  static getCheckboxes(columns, changeLocalParams, showAllFilters, unsetClearFilters) {
    let checkboxes = null;
    if (columns.length > 0) {
      checkboxes = [];
      columns.forEach((col) => {
        const key = col.name.concat('-checkbox');
        checkboxes.push(<Checkbox
          key={key}
          name={col.name}
          hidden={col.hidden}
          changeHiddenParams={changeLocalParams}
          showAllFilters={showAllFilters}
          unsetClearFilters={unsetClearFilters}
        />);
      });
    }
    return checkboxes;
  }

  static deepCopyArray(originalArry) {
    return JSON.parse(JSON.stringify(originalArry));
  }
}

export default CommonActions;
