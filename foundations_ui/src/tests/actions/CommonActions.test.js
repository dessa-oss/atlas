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
const job = {
  input_params: [
    {
      name: 'param1',
    },
    {
      name: 'param2',
    }
  ]
};
const cellWidths = [ 100, 200 ];
const jobs = [
  {
    job_id: 'job1',
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
    input_params: [
      {
        name: 'param1',
      },
      {
        name: 'param2',
      }
    ]
  }
];
const functionStub = () => null;

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
  expect(className).toBe('blue-header-text font-regular no-margin');
});

it('getTableSectionHeaderDiv with header', () => {
  const header = 'header';
  const className = CommonActions.getTableSectionHeaderDiv(header);
  expect(className).toBe('table-section-header blue-header');
});

it('getTableSectionHeaderArrow with header', () => {
  const header = 'header';
  const className = CommonActions.getTableSectionHeaderArrow(header);
  expect(className).toBe('arrow-down blue-header-arrow');
});

it('getTableSectionHeaderText with header', () => {
  const header = 'header';
  const className = CommonActions.getTableSectionHeaderText(header);
  expect(className).toBe('blue-header-text font-regular');
});

it('get InputMetricColumnHeaders', () => {
  const headers = CommonActions.getInputMetricColumnHeaders(inputParams, functionStub);
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

it('get InputMetricCells', () => {
  const cells = CommonActions.getInputMetricCells(job, cellWidths);
  expect(cells.length).toBe(2);
});

it('get InputMetricRows', () => {
  const rows = CommonActions.getInputMetricRows(jobs, cellWidths);
  expect(rows.length).toBe(2);
});