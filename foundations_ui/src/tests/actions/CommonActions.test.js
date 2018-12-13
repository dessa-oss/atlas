import React from 'react';
import ReactDOM from 'react-dom';
import { shallow, mount } from 'enzyme';
import configureTests from '../setupTests';
import CommonActions from '../../js/actions/CommonActions';

configureTests();

const inputParams = [
  'myParam',
  'my2ndParam',
];
const emptyHeader = '';
const header = 'abc';
const emptyJob = {};
const job = {
  job_id: 'myid',
  input_params: [
    {
      name: 'param1',
      source: 'constant',
      value: '1',
    },
    {
      name: 'param2',
      source: 'constant',
      value: '3',
    }
  ],
  output_metrics:[
      {
        name:'metric1',
        value: 'm'
      },
      {
        name:'metric2',
        value: 'm'
      },
      {
        name:'metric3',
        value: 'm'
      },
    ],
};
const jobs = [
  {
    job_id: 'job1',
    status: 'completed',
    input_params: [
      {
        name: 'param1',
      },
      {
        name: 'param2',
      }
    ]
  },
  {
    job_id: 'job2',
    status: 'running',
    input_params: [
      {
        name: 'param1',
        type: 'number',
      },
      {
        name: 'param2',
      }
    ]
  }
];
const noError = false;
const error = true;
const hiddenParams = ['param2'];
const noMetric = false;
const metric = true;
const columns = ['param1', 'param2'];
const metricCols = ['metric1', 'metric2', 'metric3'];
const hidden = ['param2', 'metric3'];
const columnsToFormat = [
  {name:'col1'}, {name:'col2'}, {name:'metric3'}
];
const emptyArray = [];
const changedParams = ['alreadyHere'];
const toAddParams = ['alreadyHere'];
const multipleParams = ['notHere', 'alsonothere', 'alreadyHere'];
const noParams = [];
const newParam = 'newParam';
const oldParam = 'alreadyHere';
const noSearch = '';
const search = '1';
const element = { 
  clientWidth: 100,
};
const border = 2;
const smallElementWidth = 10;
const parentWidth = 100;
const largeElementWidth = 200;
const cellType = 'number';
const allFilters = [
  {columnName: 'myCol'}
];
const min = 1;
const max = 5;
const colName = 'newCol';
const existingColName = 'myCol';
const missingColName = 'dontexist';
const containsText = 'testPhrase';
const hiddenSize = null;

it('getTableSectionHeaderDiv empty header', () => {
  const header = '';
  const className = CommonActions.getTableSectionHeaderDiv(header);
  expect(className).toBe('table-section-header');
});

it('getTableSectionHeaderArrow empty header', () => {
  const header = '';
  const className = CommonActions.getTableSectionHeaderArrow(header);
  expect(className).toBe('');
});

it('getTableSectionHeaderText empty header', () => {
  const header = '';
  const className = CommonActions.getTableSectionHeaderText(header);
  expect(className).toBe('blue-header-text text-white no-margin');
});

it('getTableSectionHeaderDiv with header', () => {
  const header = 'header';
  const className = CommonActions.getTableSectionHeaderDiv(header);
  expect(className).toBe('table-section-header blue-header');
});

it('getTableSectionHeaderArrow with header', () => {
  const header = 'header';
  const className = CommonActions.getTableSectionHeaderArrow(header);
  expect(className).toBe('blue-header-arrow border-input-metric-arrow');
});

it('getTableSectionHeaderText with header', () => {
  const header = 'header';
  const className = CommonActions.getTableSectionHeaderText(header);
  expect(className).toBe('blue-header-text text-white');
});

it('get InputMetricColumnHeaders', () => {
  const headers = CommonActions.getInputMetricColumnHeaders(inputParams, hiddenParams);
  expect(headers.length).toBe(2);
});

it('isHeaderNotEmpty isFull', () => {
  const headers = CommonActions.isHeaderNotEmpty(header);
  expect(headers).toBe(true);
})

it('isHeaderNotEmpty isEmpty', () => {
  const headers = CommonActions.isHeaderNotEmpty(emptyHeader);
  expect(headers).toBe(false);
})

it('get InputMetricCells no metric, has jobs', () => {
  const cells = CommonActions.getInputMetricCells(job, error, noMetric, columns, hidden);
  expect(cells.length).toBe(1);
});

it('get InputMetricCells no metric, no job', () => {
  const cells = CommonActions.getInputMetricCells(emptyJob, error, noMetric, columns, hidden);
  expect(cells).toBe(null);
});

it('get InputMetricCells metric, has jobs', () => {
  const cells = CommonActions.getInputMetricCells(job, error, metric, metricCols, hidden);
  expect(cells.length).toBe(3);
});

it('get InputMetricCells metric, no job', () => {
  const cells = CommonActions.getInputMetricCells(emptyJob, error, metric, metricCols, hidden);
  expect(cells).toBe(null);
});

it('get InputMetricRows no jobs, ', () => {
  const rows = CommonActions.getInputMetricRows(emptyJob, noMetric, columns, hidden);
  expect(rows).toBe(null);
});

it('get InputMetricRows jobs', () => {
  const rows = CommonActions.getInputMetricRows(jobs, noMetric, columns, hidden);
  expect(rows.length).toBe(2);
  expect(rows[0]).not.toBe(null);
  expect(rows[1]).not.toBe(null);
});

it('get InputMetricCellPClass', () => {
  const metricClass = CommonActions.getInputMetricCellPClass(noError, cellType);
  expect(metricClass).toBe('type-number');
});

it('get InputMetricCellPClass error', () => {
  const metricClass = CommonActions.getInputMetricCellPClass(error, cellType);
  expect(metricClass).toBe('error type-number');
});

it('get InputMetricCellDivClass', () => {
  const metricClass = CommonActions.getInputMetricCellDivClass(noError);
  expect(metricClass).toBe('job-cell');
});

it('get InputMetricCellPDivlass error', () => {
  const metricClass = CommonActions.getInputMetricCellDivClass(error);
  expect(metricClass).toBe('job-cell error');
});

it('get InputParamHeaders', () => {
  const headers = CommonActions.getInputParamHeaders(inputParams, hidden);
  expect(headers.length).toBe(2);
});

it('isError', () => {
  const isError = CommonActions.isError(jobs[0].status);
  expect(isError).toBe(false);
});

it('get InputCellsFromInputParams', () => {
  const cells = CommonActions.getInputCellsFromInputParams(job, noError, columns, noMetric, hidden);
  expect(cells.length).toBe(1);
  expect(cells[0]).not.toBe(null);
});

it('get MetricCellsFromOutputMetrics', () => {
  const cells = CommonActions.getMetricCellsFromOutputMetrics(job, noError, metricCols, metric, hidden);
  expect(cells.length).toBe(3);
  expect(cells[0]).not.toBe(null);
  expect(cells[1]).not.toBe(null);
  expect(cells[2]).toBe(null);
});

it('formatColumns, no cols', () => {
  const formatedCols = CommonActions.formatColumns(emptyArray, hidden, noSearch);
  expect(formatedCols).toEqual([]);
});

it('formatColumns, has cols', () => {
  const formatedCols = CommonActions.formatColumns(columnsToFormat, hidden, noSearch);
  expect(formatedCols.length).toEqual(3);
  expect(formatedCols[1].hidden).toEqual(false);
  expect(formatedCols[2].hidden).toEqual(true);
});

it('formatColumns, search', () => {
  const formatedCols = CommonActions.formatColumns(columnsToFormat, hidden, search);
  expect(formatedCols.length).toEqual(1);
});

it('get ChangedCheckboxes, old', () => {
  const changedArray = CommonActions.getChangedCheckboxes(changedParams, oldParam);
  expect(changedArray.length).toBe(0);
});

it('get ChangedCheckboxes, newParam', () => {
  const changedArray = CommonActions.getChangedCheckboxes(toAddParams, newParam);
  expect(changedArray.length).toBe(2);
  expect(changedArray[1]).toBe(newParam);
});

it('get ChangedCheckboxes, more than 1 element, none are colName', () => {
  const changedArray = CommonActions.getChangedCheckboxes(multipleParams, newParam);
  expect(changedArray.length).toBe(4);
  expect(changedArray[3]).toBe(newParam);
});

it('get ChangedCheckboxes, more than 1 element, one is colName', () => {
  const changedArray = CommonActions.getChangedCheckboxes(multipleParams, oldParam);
  expect(changedArray.length).toBe(2);
});

it('get ChangedCheckboxes, 0 elements', () => {
  const changedArray = CommonActions.getChangedCheckboxes(noParams, newParam);
  expect(changedArray.length).toBe(1);
  expect(changedArray[0]).toBe(newParam);
});

it('get RowKey', () => {
  const key = CommonActions.getRowKey(job);
  expect(key).toBe('myid-input-metric-row');
});

it('addBorderToElementWidth', () => {
  const size = CommonActions.addBorderToElementWidth(element, border, hiddenSize);
  expect(size).toBe(102);
});

it('elementsWidthLargerThanParent smaller', () => {
  const isLarger = CommonActions.elementsWidthLargerThanParent(smallElementWidth, parentWidth);
  expect(isLarger).toBe(false);
});

it('elementsWidthLargerThanParent larger', () => {
  const isLarger = CommonActions.elementsWidthLargerThanParent(largeElementWidth, parentWidth);
  expect(isLarger).toBe(true);
});

it('getInputMetricCellType, has type', () => {
  const type = CommonActions.getInputMetricCellType(jobs[1].input_params[0]);
  expect(type).toBe('number');
});

it('getInputMetricCellType, not available', () => {
  const type = CommonActions.getInputMetricCellType(jobs[1].input_params[1]);
  expect(type).toBe('not-available');
});

it('getFlatArray', () => {
  const flatArray = CommonActions.getFlatArray(columnsToFormat);
  expect(flatArray.length).toBe(3);
  expect(flatArray[0]).toBe('col1');
});

it('getNumberFilters', () => {
  const numberFilters = CommonActions.getNumberFilters(allFilters, min, max, colName);
  expect(numberFilters.length).toBe(2);
});

it('getOldFiltersWithoutColumn, has column to remove', () => {
  const newFilters = CommonActions.getOldFiltersWithoutColumn(allFilters, existingColName);
  expect(newFilters.length).toBe(0);
});

it('getOldFiltersWithoutColumn, missing column to remove', () => {
  const newFilters = CommonActions.getOldFiltersWithoutColumn(allFilters, missingColName);
  expect(newFilters.length).toBe(1); 
});

it('getContainFilters, existing column', () => {
  const newFilters = CommonActions.getContainFilters(allFilters, containsText, existingColName);
  expect(newFilters.length).toBe(1);
});

it('getContainFilters, non existing column', () => {
  const newFilters = CommonActions.getContainFilters(allFilters, containsText, missingColName);
  expect(newFilters.length).toBe(2);
});

