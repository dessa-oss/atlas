import React from 'react';
import ReactDOM from 'react-dom';
import { shallow, mount } from 'enzyme';
import configureTests from '../setupTests';
import JobActions from '../../js/actions/JobListActions';

configureTests();

const isStatus = true;
const isNotStatus = false;
const emptyHeader = '';
const header = 'abc';
const allJobs = [
  {
    input_params: [
      {
        name: 'param1',
        source: 'constant'
      },
      {
        name: 'param2',
        source: 'constant'
      },
      {
        name: 'param3',
        source: 'non-constant'
      }
    ],
    output_metrics: [
      {
        name: 'm1',
        value: 'met'
      },
      {
        name: 'm2',
        value: 'ric'
      }
    ]
  },
  {
    input_params: [
      {
        name: 'param1',
        type: 'constant'
      },
      {
        name: 'param3',
        type: 'non-constant'
      },
    ],
    output_metrics: [
      {
        name: 'm2',
        value: 'met'
      },
      {
        name: 'm3',
        value: 'ric'
      }
    ]
  }
];

const constParam = {
  name: 'abc',
  source: 'constant',
  value: 'abc'
};

const nonConstParam = {
  name: 'abc',
  source: 'non-constant',
  value: '123'
};
const isMetric = true;
const noMetric = false;
const columns = ['abc', 'm1', 'm2', 'm3'];

it('getDateDiff', () => {
  const now = Date.now();
  const day1 = now;
  const day2 = now + 1000;
  const diff = JobActions.getDateDiff(day1, day2);
  expect(diff).toBe(1000);
});

it('getDateDiff no 2nd time', () => {
  const now = Date.now();
  const day1 = now;
  const day2 = null;
  const diff = JobActions.getDateDiff(day1, day2);
  expect(diff).toBeGreaterThanOrEqual(0);
});

it('getFormatedDate no date', () => {
  const date = null;
  const formatedDate = JobActions.getFormatedDate(date);
  expect(formatedDate).toBe('');
});

it('getFormatedDate has date', () => {
  const date = '2018-08-23T09:30:00';
  const formatedDate = JobActions.getFormatedDate(date);
  expect(formatedDate).toBe('2018/08/23');
});

it('getFormatedTime no date', () => {
  const date = null;
  const formatedTime = JobActions.getFormatedTime(date);
  expect(formatedTime).toBe('');
});

it('getFormatedTime has date', () => {
  const date = '2018-08-23T09:30:00';
  const formatedTime = JobActions.getFormatedTime(date);
  expect(formatedTime).toBe('09:30:00');
});

it('getDurationDays', () => {
  const time = '86400500';
  const duration = JobActions.getDurationDays(time);
  expect(duration).toBe(1);
});

it('getDurationHours', () => {
  const time = '7205000';
  const duration = JobActions.getDurationHours(time);
  expect(duration).toBe(2);
});

it('getDurationMinutes', () => {
  const time = '183000';
  const duration = JobActions.getDurationMinutes(time);
  expect(duration).toBe(3);
});

it('getDurationSeconds', () => {
  const time = '17500';
  const duration = JobActions.getDurationSeconds(time);
  expect(duration).toBe(17);
});

it('checks if field hidden, is not hidden', () => {
  const hidden = ['hidden1', 'hidden2'];
  const fieldToCheck = 'visibleField';
  const isHidden = JobActions.isFieldHidden(hidden, fieldToCheck);
  expect(isHidden).toBe(false);
});

it('checks if field hidden, is hidden', () => {
  const hidden = ['hidden1', 'hidden2'];
  const fieldToCheck = 'hidden1';
  const isHidden = JobActions.isFieldHidden(hidden, fieldToCheck);
  expect(isHidden).toBe(true);
});

it('getStatusCircle green', () => {
  const status = 'completed';
  const circleClass = JobActions.getStatusCircle(status);
  expect(circleClass).toBe('status status-green');
});

it('gets JobColumnHeaderH4Class', () => {
  const header = JobActions.getJobColumnHeaderH4Class(isNotStatus);
  expect(header).toBe('blue-border-bottom');
});

it('gets JobColumnHeaderH4Class isStatus', () => {
  const header = JobActions.getJobColumnHeaderH4Class(isStatus);
  expect(header).toBe('blue-border-bottom status-header');
});

it('gets JobColumnHeaderArrowClass', () => {
  const arrow = JobActions.getJobColumnHeaderArrowClass(isNotStatus);
  expect(arrow).toBe('arrow-down float-right');
});

it('gets JobColumnHeaderArrowClass isStatus', () => {
  const arrow = JobActions.getJobColumnHeaderArrowClass(isStatus);
  expect(arrow).toBe('arrow-down');
});

it('gets TableSectionHeaderDivClass', () => {
  const div = JobActions.getTableSectionHeaderDivClass(header);
  expect(div).toBe('table-section-header blue-header');
});

it('gets TableSectionHeaderDivClass emptyHeader', () => {
  const div = JobActions.getTableSectionHeaderDivClass(emptyHeader);
  expect(div).toBe('table-section-header');
});

it('gets TableSectionHeaderArrowClass', () => {
  const arrow = JobActions.getTableSectionHeaderArrowClass(header);
  expect(arrow).toBe('arrow-down blue-header-arrow');
});

it('gets TableSectionHeaderArrowClass emptyHeader', () => {
  const arrow = JobActions.getTableSectionHeaderArrowClass(emptyHeader);
  expect(arrow).toBe('');
});

it('gets TableSectionHeaderTextClass', () => {
  const text = JobActions.getTableSectionHeaderTextClass(header);
  expect(text).toBe('blue-header-text');
});

it('gets TableSectionHeaderTextClass emptyHeader', () => {
  const text = JobActions.getTableSectionHeaderTextClass(emptyHeader);
  expect(text).toBe('blue-header-text no-margin');
});

it('getStatusCircle red', () => {
  const status = 'error';
  const circleClass = JobActions.getStatusCircle(status);
  expect(circleClass).toBe('status status-red');
});

it('getDurationClass days', () => {
  const desiredTime = 'days';
  const days = '3';
  const hours = '6';
  const minutes = '12';
  const seconds = '30';
  let timeUI = JobActions.getDurationClass(desiredTime, days, hours, minutes, seconds);
  // Note JSON Stringify is needed for test to pass, known jest issue: https://github.com/facebook/jest/issues/5998
  timeUI = JSON.stringify(timeUI);
  expect(timeUI).toBe(JSON.stringify(<span className="font-bold">3<span className="">d </span></span>));
});

it('getDurationClass hours', () => {
  const desiredTime = 'hours';
  const days = '3';
  const hours = '6';
  const minutes = '12';
  const seconds = '30';
  let timeUI = JobActions.getDurationClass(desiredTime, days, hours, minutes, seconds);
  // Note JSON Stringify is needed for test to pass, known jest issue: https://github.com/facebook/jest/issues/5998
  timeUI = JSON.stringify(timeUI);
  expect(timeUI).toBe(JSON.stringify(<span className="font-bold">6<span className="">h </span></span>));
});

it('getDurationClass minutes', () => {
  const desiredTime = 'minutes';
  const days = '3';
  const hours = '6';
  const minutes = '12';
  const seconds = '30';
  let timeUI = JobActions.getDurationClass(desiredTime, days, hours, minutes, seconds);
  // Note JSON Stringify is needed for test to pass, known jest issue: https://github.com/facebook/jest/issues/5998
  timeUI = JSON.stringify(timeUI);
  expect(timeUI).toBe(JSON.stringify(<span className="font-bold">12<span className="">m </span></span>));
});

it('getDurationClass seconds', () => {
  const desiredTime = 'seconds';
  const days = '3';
  const hours = '6';
  const minutes = '12';
  const seconds = '30';
  let timeUI = JobActions.getDurationClass(desiredTime, days, hours, minutes, seconds);
  // Note JSON Stringify is needed for test to pass, known jest issue: https://github.com/facebook/jest/issues/5998
  timeUI = JSON.stringify(timeUI);
  expect(timeUI).toBe(JSON.stringify(<span className="font-bold">30<span className="">s</span></span>));
});

it('getAllInputParams', () => {
  const allParams = JobActions.getAllInputParams(allJobs);
  expect(allParams.length).toBe(3);
});

it('getConstantInputParams all const', () => {
  const constInputParams = JobActions.getConstantInputParams(allJobs[0].input_params);
  expect(constInputParams.length).toBe(3);
});

it('getConstantInputParams with non const', () => {
  const constInputParams = JobActions.getConstantInputParams(allJobs[0].input_params);
  expect(constInputParams.length).toBe(3);
});

it('getInputMetricValue metric const', () => {
  const value = JobActions.getInputMetricValue(constParam, isMetric, columns);
  expect(value).toBe('abc');
});

it('getInputMetricValue metric non const', () => {
  const value = JobActions.getInputMetricValue(nonConstParam, isMetric, columns);
  expect(value).toBe('123');
});

it('getInputMetricValue no metric const', () => {
  const value = JobActions.getInputMetricValue(constParam, noMetric, columns);
  expect(value).toBe('abc');
});

it('getInputMetricValue no metric non const', () => {
  const value = JobActions.getInputMetricValue(nonConstParam, noMetric, columns);
  expect(value).toBe('123');
});

it('get AllMetrics', () => {
  const metrics = JobActions.getAllMetrics(allJobs);
  expect(metrics.length).toBe(3);
});

it('getConstantInputParams all const', () => {
  const constInputParams = JobActions.getConstantInputParams(allJobs[0].input_params);
  expect(constInputParams.length).toBe(2);
});

it('getConstantInputParams with non const', () => {
  const constInputParams = JobActions.getConstantInputParams(allJobs[0].input_params);
  expect(constInputParams.length).toBe(2);
});

it('filterJobs', () => {

});

it('getBaseJobListingURL', () => {

});

it('getFilterURL', () => {

});

it('areStatusesHidden', () => {

});
