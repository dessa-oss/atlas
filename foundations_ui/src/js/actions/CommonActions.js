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
  static getInputMetricColumnHeaders(allInputParams, hiddenInputParams, toggleNumberFilter, isMetric) {
    if (allInputParams.length > 0) {
      return this.getInputParamHeaders(allInputParams, hiddenInputParams, toggleNumberFilter, isMetric);
    }
    return null;
  }

  static getInputParamHeaders(allInputParams, hiddenInputParams, toggleNumberFilter, isMetric) {
    const inputParams = [];
    allInputParams.forEach((input) => {
      if (this.arrayDoesNotInclude(hiddenInputParams, input.name)) {
        const key = input.name;
        const colType = input.type;
        inputParams.push(<JobColumnHeader
          key={key}
          title={key}
          className="inline-block full-width"
          containerClass="job-column-header"
          toggleFilter={toggleNumberFilter}
          colType={colType}
          isMetric={isMetric}
        />);
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

  static getInputMetricCells(job, isError, isMetric, columns, hiddenInputParams) {
    if (isMetric && job.output_metrics) {
      return this.getMetricCellsFromOutputMetrics(job, isError, columns, isMetric, hiddenInputParams);
    }

    if (!isMetric && job.input_params && job.input_params.length > 0) {
      return this.getInputCellsFromInputParams(job, isError, columns, isMetric, hiddenInputParams);
    }
    return null;
  }

  static getInputCellsFromInputParams(job, isError, columns, isMetric, hiddenInputParams) {
    let cells = [];
    cells = [];
    columns.forEach((col) => {
      if (this.arrayDoesNotInclude(hiddenInputParams, col)) {
        const input = this.getInputMetricInput(job.input_params, col, isMetric);
        const key = this.getInputMetricKey(input, col, isMetric);
        const inputValue = JobActions.getInputMetricValue(input, isMetric, columns);
        const cellType = this.getInputMetricCellType(input);
        cells.push(<InputMetricCell
          key={key}
          value={inputValue}
          isError={isError}
          cellType={cellType}
        />);
      }
    });
    return cells;
  }

  static getMetricCellsFromOutputMetrics(job, isError, columns, isMetric, hiddenInputParams) {
    const cells = [];
    columns.forEach((col) => {
      if (this.arrayDoesNotInclude(hiddenInputParams, col)) {
        const input = this.getInputMetricInput(job.output_metrics, col, isMetric);
        const inputValue = JobActions.getInputMetricValue(input, isMetric, columns);
        const key = this.getInputMetricKey(input, col, isMetric);
        const cellType = this.getInputMetricCellType(input);
        cells.push(<InputMetricCell
          key={key}
          value={inputValue}
          isError={isError}
          cellType={cellType}
        />);
      } else {
        cells.push(null);
      }
    });
    return cells;
  }

  static getInputMetricRows(jobs, isMetric, allInputMetricColumn, hiddenInputParams) {
    let rows = null;
    if (jobs.length > 0) {
      rows = [];
      jobs.forEach((job) => {
        const key = this.getRowKey(job);
        const isError = this.isError(job.status);
        rows.push(<InputMetricRow
          key={key}
          job={job}
          isError={isError}
          isMetric={isMetric}
          allInputMetricColumn={allInputMetricColumn}
          hiddenInputParams={hiddenInputParams}
        />);
      });
    }
    return rows;
  }

  static getInputMetricCellPClass(isError, cellType) {
    return isError ? `error type-${cellType}` : `type-${cellType}`;
  }

  static getInputMetricCellDivClass(isError) {
    return isError ? 'job-cell error' : 'job-cell';
  }

  static isError(status) {
    return status.toLowerCase() === 'error';
  }

  static formatColumns(columns, hiddenInputParams, searchText = '') {
    const formatedColumns = [];
    if (columns !== null) {
      columns.forEach((col) => {
        if (col.name.toLowerCase().includes(searchText.toLowerCase())) {
          let isHidden = false;
          if (hiddenInputParams.includes(col.name)) {
            isHidden = true;
          }
          formatedColumns.push({ name: col.name, hidden: isHidden });
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

  static addBorderToElementWidth(element, borderWidth) {
    return element.clientWidth + borderWidth;
  }

  static elementsWidthLargerThanParent(elementWidth, parentWidth) {
    return elementWidth > parentWidth;
  }

  static getInputMetricCellType(inputMetric) {
    if (inputMetric && inputMetric.type) {
      return inputMetric.type;
    }
    return 'not-available';
  }

  static getFlatArray(array) {
    return array.map((element) => {
      return element.name;
    });
  }

  static getNumberFilters(oldFilters, newMin, newMax, newShowingNotAvailable, newColumnName) {
    const newFilters = oldFilters.filter(
      (filter) => {
        if (filter.columnName !== newColumnName) {
          return true;
        }
      },
    );
    newFilters.push({
      columnName: newColumnName,
      min: newMin,
      max: newMax,
      showingNotAvailable: newShowingNotAvailable,
    });
    return newFilters;
  }

  // private functions, not cannot declare a private and static
  // function in JS https://stackoverflow.com/a/3218950
  static arrayDoesNotInclude(array, value) {
    return !array.includes(value);
  }

  static getInputMetricInput(jobArray, column, isMetric) {
    let input = null;
    if (!isMetric) {
      input = {};
    }
    if (jobArray) {
      jobArray.forEach((param) => {
        if (param.name === column) {
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
    return input.source === 'constant';
  }

  static getCheckboxes(columns, changeLocalParams, showAllFilters, unsetClearFilters, statusCheckbox = false) {
    let checkboxes = null;
    if (columns.length > 0) {
      checkboxes = [];
      columns.forEach((col) => {
        let statusCircle = null;
        if (statusCheckbox) {
          statusCircle = JobActions.getStatusCircle(col.name);
        }
        const key = col.name.concat('-checkbox');
        checkboxes.push(<Checkbox
          key={key}
          name={col.name}
          hidden={col.hidden}
          changeHiddenParams={changeLocalParams}
          showAllFilters={showAllFilters}
          unsetClearFilters={unsetClearFilters}
          statusCircle={statusCircle}
        />);
      });
    }
    return checkboxes;
  }

  static deepCopyArray(originalArray) {
    return JSON.parse(JSON.stringify(originalArray));
  }
}

export default CommonActions;
