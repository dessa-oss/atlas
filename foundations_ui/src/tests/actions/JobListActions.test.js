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

const zeroConstParam = {
  name: 'abc',
  source: 'constant',
  value: 0
};
const nonConstParam = {
  name: 'abc',
  source: 'non-constant',
  value: '123'
};
const zeroNonConstParam = {
  name: 'abc',
  source: 'non-constant',
  value: 0
};

const nullConstParam = {
  name: 'abc',
  source: 'constant',
  value: null
};

const isMetric = true;
const noMetric = false;
const columns = ['abc', 'm1', 'm2', 'm3'];
const projectName = 'project name';
const noHiddenStatusFilter = [
  { name: 'Completed', hidden: false },
  { name: 'Processing', hidden: false },
  { name: 'Failed', hidden: false },
];
const hiddenStatusFilter = [
  { name: 'Processing', hidden: false },
  { name: 'Failed', hidden: false },
  { name: 'Completed', hidden: true },
];
const filters = [
  { column: 'Status', value: 'Failed' },
  { column: 'User', value: 'Buck' },
];
const emptyFilters = [];
const filterToRemove = { column: 'Status', value: 'Failed' };
const jobs = [
  {
    user: 'user1'
  },
  {
    user: 'duplicateUser'
  },
  {
    user: 'duplicateUser'
  },
];
const url = 'localhost/';
const isFirst = true;
const isNotFirst = false;
const status = { name: 'Failed', hidden: false };
const colName = 'myCol';
const colValue = 'myVal';
const hasFilter = false;
const noFilter = true;
const hiddenUserFilter = [
  'hidden1',
  'hidden2'
];
const allUsers = [
  'user1',
  'user2',
  'user3',
  'user4'
];
const newHiddenUser = 'user2';
const startValue = '1';
const endValue = '2';
const allFilters = [
  {columnName: 'myCol'}
];
const nonExistingFilter = 'nonExist';
const containValue = 'testPhrase';
const removeFilter = { column: 'myCol' };
const colType = 'number';
const noneHiddenBoolFilter = [{
  boolCheckboxes: [
    {name: 'not-hidden', hidden: false}
  ]
}];
const hiddenBoolFilter = [{
  boolCheckboxes: [
    {name: 'hidden', hidden: true}
  ]
}];
const time = {
  'days': '1',
  'hours': '2',
  'minutes': '3',
  'seconds': '4'
};
const dateTime = 'Tue Mar 24 2015 20:00:00 GMT-0400 (Eastern Daylight Time)';
const singleDigit = '1';
const doubleDigit = '11';
const columnFilter = [
  { column: 'test1' },
  { column: 'test2' }
];
const existingColumn = 'test1';
const nonExistingColumn = 'not here';

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

it('parseDuration should return the duration in milliseconds with seconds', () => {
  const duration = '0d0h0m3s'
  const durationMilliseconds = JobActions.parseDuration(duration);
  expect(durationMilliseconds).toBe(3000);
});

it('parseDuration should return the duration in milliseconds with differnt seconds', () => {
  const duration = '0d0h0m13s'
  const durationMilliseconds = JobActions.parseDuration(duration);
  expect(durationMilliseconds).toBe(13000);
});

it('parseDuration should return the duration in milliseconds with an empty time', () => {
  const duration = '0d0h0m0s'
  const durationMilliseconds = JobActions.parseDuration(duration);
  expect(durationMilliseconds).toBe(1000);
});

it('parseDuration should return the duration in milliseconds with no time', () => {
  const duration = ''
  const durationMilliseconds = JobActions.parseDuration(duration);
  expect(durationMilliseconds).toBe(0);
});

it('parseDuration should return the duration in milliseconds with minutes', () => {
  const duration = '0d0h3m0s'
  const durationMilliseconds = JobActions.parseDuration(duration);
  expect(durationMilliseconds).toBe(180000);
});

it('parseDuration should return the duration in milliseconds with different minutes', () => {
  const duration = '0d0h7m0s'
  const durationMilliseconds = JobActions.parseDuration(duration);
  expect(durationMilliseconds).toBe(420000);
});

it('parseDuration should return the duration in milliseconds with hours', () => {
  const duration = '0d3h0m0s'
  const durationMilliseconds = JobActions.parseDuration(duration);
  expect(durationMilliseconds).toBe(10800000);
});

it('parseDuration should return the duration in milliseconds with different hours', () => {
  const duration = '0d7h0m0s'
  const durationMilliseconds = JobActions.parseDuration(duration);
  expect(durationMilliseconds).toBe(25200000);
});

it('parseDuration should return the duration in milliseconds with days', () => {
  const duration = '3d0h0m0s'
  const durationMilliseconds = JobActions.parseDuration(duration);
  expect(durationMilliseconds).toBe(259200000);
});

it('parseDuration should return the duration in milliseconds with different days', () => {
  const duration = '7d0h0m0s'
  const durationMilliseconds = JobActions.parseDuration(duration);
  expect(durationMilliseconds).toBe(604800000);
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
  const arrow = JobActions.getJobColumnHeaderArrowClass(isNotStatus, colType, isMetric);
  expect(arrow).toBe('arrow-down float-right number is-metric');
});

it('gets JobColumnHeaderArrowClass isStatus', () => {
  const arrow = JobActions.getJobColumnHeaderArrowClass(isStatus, colType, isMetric);
  expect(arrow).toBe('arrow-down number is-metric');
});

it('getJobColumnHeaderDivClass', () => {
  const div = JobActions.getJobColumnHeaderDivClass(colType, isMetric);
  expect(div).toBe('number status-header');
});

it('getJobColumnHeaderPresentationClass', () => {
  const div = JobActions.getJobColumnHeaderPresentationClass(colType, isMetric);
  expect(div).toBe('arrow-container number is-metric');
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
  const status = 'Failed';
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

it('getInputMetricValue metric const value 0', () => {
  const value = JobActions.getInputMetricValue(zeroConstParam, isMetric, columns);
  expect(value).toBe(0);
});

it('getInputMetricValue no metric const value 0', () => {
  const value = JobActions.getInputMetricValue(zeroConstParam, noMetric, columns);
  expect(value).toBe(0);
});

it('getInputMetricValue metric non const value 0', () => {
  const value = JobActions.getInputMetricValue(zeroNonConstParam, isMetric, columns);
  expect(value).toBe(0);
});

it('getInputMetricValue no metric non const value 0', () => {
  const value = JobActions.getInputMetricValue(zeroNonConstParam, noMetric, columns);
  expect(value).toBe(0);
});

it('getInputMetricValue metric const value null', () => {
  const value = JobActions.getInputMetricValue(nullConstParam, isMetric, columns);
  expect(value).toBe('not available');
});

it('getInputMetricValue no metric const value null', () => {
  const value = JobActions.getInputMetricValue(nullConstParam, noMetric, columns);
  expect(value).toBe('not available');
});

it('getBaseJobListingURL', () => {
  const URL = JobActions.getBaseJobListingURL(projectName);
  expect(URL).toBe('projects/project name/job_listing');
});

it('getFilterURL only 1 type', () => {
  const URL = JobActions.getFilterURL(hiddenStatusFilter, emptyFilters, emptyFilters, emptyFilters, emptyFilters, emptyFilters, emptyFilters, emptyFilters);
  expect(URL).toBe('status=Processing,Failed');
});

it('getFilterURL more than 1 type', () => {
  const URL = JobActions.getFilterURL(hiddenStatusFilter, hiddenUserFilter, emptyFilters, emptyFilters, emptyFilters, emptyFilters, emptyFilters, emptyFilters);
  expect(URL).toBe('status=Processing,Failed&user=hidden1,hidden2');
});

it('areStatusesHidden hidden', () => {
  const areHidden = JobActions.areStatusesHidden(hiddenStatusFilter);
  expect(areHidden).toBe(true)
});

it('areStatusesHidden not hidden', () => {
  const areHidden = JobActions.areStatusesHidden(noHiddenStatusFilter);
  expect(areHidden).toBe(false)
});

it('getAllFilters', () => {
  const updatedFilters = JobActions.getAllFilters(hiddenStatusFilter, allUsers, hiddenUserFilter, emptyFilters, emptyFilters, emptyFilters, emptyFilters, emptyFilters, emptyFilters);
  expect(updatedFilters.length).toBe(6);

});

it('getStatusFilters', () => {
  const updatedFilters = JobActions.getStatusFilters(filters, hiddenStatusFilter);
  expect(updatedFilters.length).toBe(3);
});

it('removeFilter', () => {
  const updatedFilters = JobActions.removeFilter(filters, filterToRemove);
  expect(updatedFilters.length).toBe(1);
  expect(updatedFilters[0].value).toBe('Buck');
});

it('getAllJobUsers', () => {
  const allUsers = JobActions.getAllJobUsers(jobs);
  expect(allUsers.length).toBe(2);
});

it('addtoURL, first status', () => {
  const updatedUrl = JobActions.addToURL(url, isFirst, colValue, colName);
  expect(updatedUrl).toBe('localhost/myCol=myVal');
});

it('addtoURL, not first status', () => {
  const updatedUrl = JobActions.addToURL(url, isNotFirst, colValue, colName);
  expect(updatedUrl).toBe('localhost/,myVal');
});

it('getFilterObject', () => {
  const filteredObject = JobActions.getFilterObject(colName, colValue);
  expect(filteredObject).toEqual({ column: 'myCol', value: 'myVal' });
});

it('addStatusToURLNotHidden, not hidden', () => {
  const updatedUrl = JobActions.addStatusToURLNotHidden(url, isFirst, status);
  expect(updatedUrl).toBe('localhost/status=Failed');
});

it('addStatusToURLNotHidden, hidden', () => {
  status.hidden = true;
  const updatedUrl = JobActions.addStatusToURLNotHidden(url, isFirst, status);
  expect(updatedUrl).toBe('localhost/');
});

it('getOldStatusFilters', () => {
  const oldFilters = JobActions.getOldStatusFilters(filters);
  expect(oldFilters.length).toBe(1);
  expect(oldFilters[0].column).toBe('User');
});

it('addNewStatusFilters', () => {
  const newFilters = [];
  JobActions.addNewStatusFilters(hiddenStatusFilter, newFilters);
  expect(newFilters.length).toBe(2);
});

it('getUpdatedStatusesFromOldStatuses', () => {
  const newStatuses = [];
  JobActions.getUpdatedStatusesFromOldStatuses(filters, status, isNotFirst, newStatuses);
  expect(newStatuses.length).toBe(1);
});

it('updateStatusesIfNoFilters, has filters', () => {
  JobActions.updateStatusesIfNoFilters(hasFilter, hiddenStatusFilter);
  expect(hiddenStatusFilter[2].hidden).toBe(true);
});

it('updateStatusesIfNoFilters, no filters', () => {
  JobActions.updateStatusesIfNoFilters(noFilter, hiddenStatusFilter);
  expect(hiddenStatusFilter[0].hidden).toBe(false);
});

it('addToURLNotHidden first', () => {
  const newURL = JobActions.addToURLNotHidden(url, isFirst, colValue, colName);
  expect(newURL).toBe('localhost/myCol=myVal');
});

it('addToURLNotHidden not first', () => {
  const newURL = JobActions.addToURLNotHidden(url, isNotFirst, colValue, colName);
  expect(newURL).toBe('localhost/,myVal');
});

it('addAndIfNotFirstFilter, first', () => {
  const newURL = JobActions.addAndIfNotFirstFilter(url, isFirst);
  expect(newURL).toBe('localhost/');
});

it('addAndIfNotFirstFilter, not first', () => {
  const newURL = JobActions.addAndIfNotFirstFilter(url, isNotFirst);
  expect(newURL).toBe('localhost/&');
});

it('updateHiddenParams', () => {
  const newHiddenParams = JobActions.updateHiddenParams(allUsers, newHiddenUser, hiddenUserFilter);
  expect(newHiddenParams.length === 3);
  expect(newHiddenParams[2]).toBe('user2');

});

it('willHideAllParams', () => {
  const willHide = JobActions.willHideAllParams(allUsers, hiddenUserFilter);
  expect(willHide).toBe(false);
});

it('addToURLRangeNotHidden', () => {
  const newURL = JobActions.addToURLRangeNotHidden(url, startValue, endValue, colName);
  expect(newURL).toBe('localhost/myCol_starts=1&myCol_ends=2');
});

it('getRangeFilter', () => {
  const rangeFilter = JobActions.getRangeFilter(colName, startValue, endValue);
  expect(rangeFilter).toEqual({"column": "myCol", "value": "1 - 2"});
});

it('getExistingValuesForFilter, not existing', () => {
  const existingValues = JobActions.getExistingValuesForFilter(allFilters, colName);
  expect(existingValues).not.toEqual(null);
});

it('getExistingValuesForFilter, existing', () => {
  const existingValues = JobActions.getExistingValuesForFilter(allFilters, nonExistingFilter);
  expect(existingValues).toBe(null);
});

it('removeFilterByName, not exists', () => {
  const updatedFilters = JobActions.removeFilterByName(allFilters, nonExistingFilter);
  expect(updatedFilters.length).toBe(1);
});

it('removeFilterByName, exists', () => {
  const updatedFilters = JobActions.removeFilterByName(allFilters, removeFilter);
  expect(updatedFilters.length).toBe(0);
});

it('addToURLContainFilter', () => {
  const newURL = JobActions.addToURLContainFilter(url, containValue, colName)
  expect(newURL).toBe('localhost/myCol_contains=testPhrase');
});

it('getContainFilter', () => {
  const containFilter = JobActions.getContainFilter(colName, containValue);
  expect(containFilter).toEqual({"column": "myCol", "value": "\"testPhrase\""});
});

it('boolFilterArrayHasHidden, has hidden', () => {
  const hasHidden = JobActions.boolFilterArrayHasHidden(hiddenBoolFilter);
  expect(hasHidden).toBe(true);
});

it('boolFilterArrayHasHidden, none hidden', () => {
  const hasHidden = JobActions.boolFilterArrayHasHidden(noneHiddenBoolFilter);
  expect(hasHidden).toBe(false);
});

it('boolFilterHasHidden, had hidden', () => {
  const hasHidden = JobActions.boolFilterHasHidden(hiddenBoolFilter[0]);
  expect(hasHidden).toBe(true);
});

it('boolFilterHasHidden, none hidden', () => {
  const hasHidden = JobActions.boolFilterHasHidden(noneHiddenBoolFilter[0]);
  expect(hasHidden).toBe(false);
});

it('boolFilterGetNonHidden, has hidden', () => {
  const hidden = JobActions.boolFilterGetNonHidden(hiddenBoolFilter[0]);
  expect(hidden.length).toBe(0);
});

it('boolFilterGetNonHidden, none hidden', () => {
  const hidden = JobActions.boolFilterGetNonHidden(noneHiddenBoolFilter[0]);
  expect(hidden.length).toBe(1);
});

it('boolFilterGetHidden, has hidden', () => {
  const hidden = JobActions.boolFilterGetHidden(hiddenBoolFilter[0].boolCheckboxes);
  expect(hidden.length).toBe(1);
});

it('boolFilterGetHidden, none hidden', () => {
  const hidden = JobActions.boolFilterGetHidden(noneHiddenBoolFilter[0].boolCheckboxes);
  expect(hidden.length).toBe(0);
});

it('getTimeForDurationURL', () => {
  const urlTime = JobActions.getTimeForDurationURL(time);
  expect(urlTime).toBe('1_2_3_4');
});

it('getTimeForDurationBubble', () => {
  const bubbleTime = JobActions.getTimeForDurationBubble(time);
  expect(bubbleTime).toBe('1d2h3m4s');
});

it('areNoFilters, no filters', () => {
  const noFilters = JobActions.areNoFilters(emptyFilters, emptyFilters, emptyFilters, emptyFilters, emptyFilters, emptyFilters, emptyFilters, emptyFilters);
  expect(noFilters).toBe(true);
});

it('areNoFilters, has filters', () => {
  const noFilters = JobActions.areNoFilters(emptyFilters, emptyFilters, emptyFilters, emptyFilters, hiddenBoolFilter, emptyFilters, emptyFilters, emptyFilters);
  expect(noFilters).toBe(false);
});

// Pending cause of Jenkins Timezone UTC vs EST issue
xit('getTimeForStartTimeURL', () => {
  const newURL = JobActions.getTimeForStartTimeURL(dateTime);
  expect(newURL).toBe('03_24_2015_20_00');
});

it('prependZero, single digit', () =>{
  const newDigit = JobActions.prependZero(singleDigit);
  expect(newDigit).toBe('01');
});

it('prependZero, 2 digit', () => {
  const newDigit = JobActions.prependZero(doubleDigit);
  expect(newDigit).toBe('11');
});

// Pending cause of Jenkins Timezone UTC vs EST issue
xit('getTimeForStartTimeBubble', () => {
  const bubble = JobActions.getTimeForStartTimeBubble(dateTime);
  expect(bubble).toBe('03/24/15 20:00');
});

it('isColumnFiltered, is filtered', () => {
  const isFiltered = JobActions.isColumnFiltered(columnFilter, existingColumn);
  expect(isFiltered).toBe(true);
});

it('isColumnFiltered, not filter', () => {
  const isFiltered = JobActions.isColumnFiltered(columnFilter, nonExistingColumn);
  expect(isFiltered).toBe(false);
});
