import React from 'react';
import JobColumnHeader from '../components/common/JobColumnHeader';
import InputMetricCell from '../components/common/InputMetricCell';
import InputMetricRow from '../components/common/InputMetricRow';
import Checkbox from '../components/common/Checkbox';
import JobListActions from './JobListActions';

const notFound = -1;
const oneElement = 1;

class CommonActions {
  // Helper Functions
  static getInputMetricColumnHeaders(
    allInputParams, hiddenInputParams, toggleNumberFilter, isMetric, filteredArray,
  ) {
    if (allInputParams.length > 0) {
      return this.getInputParamHeaders(
        allInputParams, hiddenInputParams, toggleNumberFilter, isMetric, filteredArray,
      );
    }
    return null;
  }

  static getInputParamHeaders(allInputParams, hiddenInputParams, toggleNumberFilter, isMetric, filteredArray) {
    const inputParams = [];
    allInputParams.forEach((input) => {
      if (this.arrayDoesNotInclude(hiddenInputParams, input.name)) {
        const key = input.name;
        const colType = input.type;
        const isFiltered = JobListActions.isColumnFiltered(filteredArray, key);
        inputParams.push(<JobColumnHeader
          key={key}
          title={key}
          className="inline-block full-width"
          containerClass="job-column-header"
          toggleFilter={toggleNumberFilter}
          colType={colType}
          isMetric={isMetric}
          isFiltered={isFiltered}
        />);
      }
    });
    return inputParams;
  }

  static formatAMPM(date) {
    const updatedTime = new Date(date.setHours(date.getHours() - 4));
    let hours = updatedTime.getHours();
    let minutes = date.getMinutes();
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours %= 12;
    hours = hours || 12;
    minutes = minutes < 10 ? `0${minutes}` : minutes;
    const strTime = `${hours}:${minutes} ${ampm}`;
    return strTime;
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

  static getInputMetricCells(job, isError, isMetric, columns, hiddenInputParams, rowNumber) {
    if (isMetric && job.output_metrics) {
      return this.getMetricCellsFromOutputMetrics(job, isError, columns, isMetric, hiddenInputParams, rowNumber);
    }

    if (!isMetric && job.input_params) {
      return this.getInputCellsFromInputParams(job, isError, columns, isMetric, hiddenInputParams, rowNumber);
    }
    return null;
  }

  static getInputCellsFromInputParams(job, isError, columns, isMetric, hiddenInputParams, rowNumber) {
    let cells = [];
    cells = [];
    columns.forEach((col) => {
      if (this.arrayDoesNotInclude(hiddenInputParams, col)) {
        const input = this.getInputMetricInput(job.input_params, col, isMetric);
        const key = this.getInputMetricKey(input, col, isMetric);
        let inputValue = JobListActions.getInputMetricValue(input, isMetric, columns);
        const cellType = this.getInputMetricCellType(input);
        const isHoverable = this.getInputMetricIsHoverable(input);

        if (cellType.match(/array*/)) {
          inputValue = this.transformArraysToString(inputValue);
        }
        cells.push(<InputMetricCell
          key={key}
          value={inputValue}
          isError={isError}
          cellType={cellType}
          rowNumber={rowNumber}
          hoverable={isHoverable}
        />);
      }
    });
    return cells;
  }

  static getMetricCellsFromOutputMetrics(job, isError, columns, isMetric, hiddenInputParams, rowNumber) {
    const cells = [];
    columns.forEach((col) => {
      if (this.arrayDoesNotInclude(hiddenInputParams, col)) {
        const input = this.getInputMetricInput(job.output_metrics, col, isMetric);
        let inputValue = JobListActions.getInputMetricValue(input, isMetric, columns);
        const key = this.getInputMetricKey(input, col, isMetric);
        const cellType = this.getInputMetricCellType(input);
        const isHoverable = this.getInputMetricIsHoverable(input);
        if (cellType.match(/array*/)) {
          inputValue = this.transformArraysToString(inputValue);
        }
        cells.push(<InputMetricCell
          key={key}
          value={inputValue}
          isError={isError}
          cellType={cellType}
          rowNumber={rowNumber}
          hoverable={isHoverable}
        />);
      } else {
        cells.push(null);
      }
    });
    return cells;
  }

  static transformArraysToString(arrayValue) {
    let newValue = '[';
    arrayValue.forEach((element) => {
      newValue = newValue.concat(String(element));
      newValue += ', ';
    });
    newValue = newValue.slice(0, newValue.length - 2);
    newValue += ']';
    return newValue;
  }

  static getInputMetricRows(jobs, isMetric, allInputMetricColumn, hiddenInputParams, onMetricRowClick) {
    let rows = null;
    let rowNumber = 0;
    if (jobs.length > 0) {
      rows = [];
      jobs.forEach((job, index) => {
        const key = this.getRowKey(job);
        const isError = this.isError(job.status);
        rows.push(<InputMetricRow
          key={key}
          job={job}
          isError={isError}
          isMetric={isMetric}
          allInputMetricColumn={allInputMetricColumn}
          hiddenInputParams={hiddenInputParams}
          rowNumber={rowNumber}
          onMetricRowClick={() => onMetricRowClick(job, index)}
        />);
        rowNumber += 1;
      });
    }
    return rows;
  }

  static getInputMetricCellPClass(isError, cellType) {
    return isError ? `error type-${cellType}` : `type-${cellType}`;
  }

  static getInputMetricCellDivClass(isError, rowNumber) {
    return isError ? `job-cell error row-${rowNumber}` : `job-cell row-${rowNumber}`;
  }

  static isError(status) {
    return status.toLowerCase() === 'failed';
  }

  static errorStatus(isError) {
    return isError ? 'failed' : '';
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

  static addBorderToElementWidth(element, borderWidth, hiddenWidth) {
    if (hiddenWidth !== null) {
      return hiddenWidth + borderWidth;
    }
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

  static getInputMetricIsHoverable(inputMetric) {
    if (inputMetric && inputMetric.hoverable !== undefined) {
      return inputMetric.hoverable;
    }
    return true;
  }

  static getFlatArray(array) {
    return array.map((element) => {
      return element.name;
    });
  }

  static getOldFiltersWithoutColumn(oldFilters, newColumnName) {
    return oldFilters.filter(
      (filter) => {
        if (filter.columnName !== newColumnName) {
          return true;
        }
      },
    );
  }

  static getNumberFilters(oldFilters, newMin, newMax, newShowingNotAvailable, newColumnName) {
    const newFilters = this.getOldFiltersWithoutColumn(oldFilters, newColumnName);
    newFilters.push({
      columnName: newColumnName,
      min: newMin,
      max: newMax,
      showingNotAvailable: newShowingNotAvailable,
    });
    return newFilters;
  }

  static getContainFilters(oldFilters, newSearchText, newColumnName) {
    const newFilters = this.getOldFiltersWithoutColumn(oldFilters, newColumnName);
    newFilters.push({
      columnName: newColumnName,
      searchText: newSearchText,
    });
    return newFilters;
  }

  static getBoolFilters(oldFilters, newFormattedBool, newColumnName) {
    const newFilters = this.getOldFiltersWithoutColumn(oldFilters, newColumnName);
    newFilters.push({
      columnName: newColumnName,
      boolCheckboxes: newFormattedBool,
    });
    return newFilters;
  }

  static getDurationFilters(startTime, endTime, columnName) {
    return [{ columnName, startTime, endTime }];
  }

  static getApplyClass(isDisabled) {
    let applyClass = 'b--mat b--affirmative text-upper';
    if (isDisabled()) {
      applyClass += ' b--disabled';
    }
    return applyClass;
  }

  static getInputMetricFilterLeft(metricClass) {
    let style = null;
    const inputBorder = 3;
    if (this.isMetricAndHasContainers(metricClass)) {
      const staticColumnLeft = document.getElementsByClassName('job-static-columns-container')[0].clientWidth;
      const inputParamLeft = document.getElementsByClassName('job-static-columns-container')[1].clientWidth;

      const filterLeft = staticColumnLeft + inputParamLeft + inputBorder;
      style = { left: filterLeft };
    }
    return style;
  }

  static isMetricAndHasContainers(metricClass) {
    return (metricClass === 'is-metric' && document.getElementsByClassName('job-static-columns-container').length > 1);
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

  static getCheckboxes(
    columns, changeLocalParams, showAllFilters, unsetClearFilters, hideAllFilters,
    statusCheckbox = false, unsetHideFilters = () => {},
  ) {
    let checkboxes = null;
    if (columns.length > 0) {
      checkboxes = [];
      columns.forEach((col) => {
        let statusCircle = null;
        if (statusCheckbox) {
          statusCircle = JobListActions.getStatusCircle(col.name);
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
          hideAllFilters={hideAllFilters}
          unsetHideFilters={unsetHideFilters}
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
