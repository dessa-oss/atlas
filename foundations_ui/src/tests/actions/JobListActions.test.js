import React from 'react';
import ReactDOM from 'react-dom';
import { shallow, mount } from 'enzyme';
import { Redirect } from 'react-router-dom';
import configureTests from '../setupTests';
import JobListActions from '../../js/actions/JobListActions';

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
  const formatedDate = JobListActions.getFormatedDate(date);
  expect(formatedDate).toBe('');
});

it('getFormatedDate has date', () => {
  const date = '2018-08-23T09:30:00';
  const formatedDate = JobListActions.getFormatedDate(date);
  expect(formatedDate).toBe('2018/08/23');
});

it('getFormatedTime no date', () => {
  const date = null;
  const formatedTime = JobListActions.getFormatedTime(date);
  expect(formatedTime).toBe('');
});

it('getFormatedTime has date', () => {
  const date = '2018-08-23T09:30:00';
  const formatedTime = JobListActions.getFormatedTime(date);
  expect(formatedTime).toBe('5:30 am EST');
});

it('getDurationDays', () => {
  const time = '86400500';
  const duration = JobListActions.getDurationDays(time);
  expect(duration).toBe(1);
});

it('getDurationHours', () => {
  const time = '7205000';
  const duration = JobListActions.getDurationHours(time);
  expect(duration).toBe(2);
});

it('getDurationMinutes', () => {
  const time = '183000';
  const duration = JobListActions.getDurationMinutes(time);
  expect(duration).toBe(3);
});

it('getDurationSeconds', () => {
  const time = '17500';
  const duration = JobListActions.getDurationSeconds(time);
  expect(duration).toBe(17);
});

it('parseDuration should return the duration in milliseconds with seconds', () => {
  const duration = '0d0h0m3s'
  const durationMilliseconds = JobListActions.parseDuration(duration);
  expect(durationMilliseconds).toBe(3000);
});

it('parseDuration should return the duration in milliseconds with differnt seconds', () => {
  const duration = '0d0h0m13s'
  const durationMilliseconds = JobListActions.parseDuration(duration);
  expect(durationMilliseconds).toBe(13000);
});

it('parseDuration should return the duration in milliseconds with an empty time', () => {
  const duration = '0d0h0m0s'
  const durationMilliseconds = JobListActions.parseDuration(duration);
  expect(durationMilliseconds).toBe(1000);
});

it('parseDuration should return the duration in milliseconds with no time', () => {
  const duration = ''
  const durationMilliseconds = JobListActions.parseDuration(duration);
  expect(durationMilliseconds).toBe(0);
});

it('parseDuration should return the duration in milliseconds with minutes', () => {
  const duration = '0d0h3m0s'
  const durationMilliseconds = JobListActions.parseDuration(duration);
  expect(durationMilliseconds).toBe(180000);
});

it('parseDuration should return the duration in milliseconds with different minutes', () => {
  const duration = '0d0h7m0s'
  const durationMilliseconds = JobListActions.parseDuration(duration);
  expect(durationMilliseconds).toBe(420000);
});

it('parseDuration should return the duration in milliseconds with hours', () => {
  const duration = '0d3h0m0s'
  const durationMilliseconds = JobListActions.parseDuration(duration);
  expect(durationMilliseconds).toBe(10800000);
});

it('parseDuration should return the duration in milliseconds with different hours', () => {
  const duration = '0d7h0m0s'
  const durationMilliseconds = JobListActions.parseDuration(duration);
  expect(durationMilliseconds).toBe(25200000);
});

it('parseDuration should return the duration in milliseconds with days', () => {
  const duration = '3d0h0m0s'
  const durationMilliseconds = JobListActions.parseDuration(duration);
  expect(durationMilliseconds).toBe(259200000);
});

it('parseDuration should return the duration in milliseconds with different days', () => {
  const duration = '7d0h0m0s'
  const durationMilliseconds = JobListActions.parseDuration(duration);
  expect(durationMilliseconds).toBe(604800000);
});

it('checks if field hidden, is not hidden', () => {
  const hidden = ['hidden1', 'hidden2'];
  const fieldToCheck = 'visibleField';
  const isHidden = JobListActions.isFieldHidden(hidden, fieldToCheck);
  expect(isHidden).toBe(false);
});

it('checks if field hidden, is hidden', () => {
  const hidden = ['hidden1', 'hidden2'];
  const fieldToCheck = 'hidden1';
  const isHidden = JobListActions.isFieldHidden(hidden, fieldToCheck);
  expect(isHidden).toBe(true);
});

it('getStatusCircle green', () => {
  const status = 'completed';
  const circleClass = JobListActions.getStatusCircle(status);
  expect(circleClass).toBe('status status-green');
});

it('gets JobColumnHeaderH4Class', () => {
  const header = JobListActions.getJobColumnHeaderH4Class(isNotStatus);
  expect(header).toBe('');
});

it('gets JobColumnHeaderH4Class isStatus', () => {
  const header = JobListActions.getJobColumnHeaderH4Class(isStatus);
  expect(header).toBe('status-header');
});

it('gets JobColumnHeaderArrowClass', () => {
  const arrow = JobListActions.getJobColumnHeaderArrowClass(isNotStatus, colType, isMetric);
  expect(arrow).toBe('arrow-down float-right number is-metric');
});

it('gets JobColumnHeaderArrowClass isStatus', () => {
  const arrow = JobListActions.getJobColumnHeaderArrowClass(isStatus, colType, isMetric);
  expect(arrow).toBe('arrow-down number is-metric');
});

it('getJobColumnHeaderDivClass', () => {
  const div = JobListActions.getJobColumnHeaderDivClass(colType, isMetric);
  expect(div).toBe('number status-header');
});

it('getJobColumnHeaderPresentationClass', () => {
  const div = JobListActions.getJobColumnHeaderPresentationClass(colType, isMetric);
  expect(div).toBe('arrow-container number is-metric');
});

it('gets TableSectionHeaderDivClass', () => {
  const div = JobListActions.getTableSectionHeaderDivClass(header);
  expect(div).toBe('table-section-header blue-header');
});

it('gets TableSectionHeaderDivClass emptyHeader', () => {
  const div = JobListActions.getTableSectionHeaderDivClass(emptyHeader);
  expect(div).toBe('table-section-header');
});

it('gets TableSectionHeaderArrowClass', () => {
  const arrow = JobListActions.getTableSectionHeaderArrowClass(header);
  expect(arrow).toBe('arrow-down blue-header-arrow');
});

it('gets TableSectionHeaderArrowClass emptyHeader', () => {
  const arrow = JobListActions.getTableSectionHeaderArrowClass(emptyHeader);
  expect(arrow).toBe('');
});

it('gets TableSectionHeaderTextClass', () => {
  const text = JobListActions.getTableSectionHeaderTextClass(header);
  expect(text).toBe('blue-header-text');
});

it('gets TableSectionHeaderTextClass emptyHeader', () => {
  const text = JobListActions.getTableSectionHeaderTextClass(emptyHeader);
  expect(text).toBe('blue-header-text no-margin');
});

it('getStatusCircle red', () => {
  const status = 'Failed';
  const circleClass = JobListActions.getStatusCircle(status);
  expect(circleClass).toBe('status status-red');
});

it('getDurationClass days', () => {
  const desiredTime = 'days';
  const days = '3';
  const hours = '6';
  const minutes = '12';
  const seconds = '30';
  let timeUI = JobListActions.getDurationClass(desiredTime, days, hours, minutes, seconds);
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
  let timeUI = JobListActions.getDurationClass(desiredTime, days, hours, minutes, seconds);
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
  let timeUI = JobListActions.getDurationClass(desiredTime, days, hours, minutes, seconds);
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
  let timeUI = JobListActions.getDurationClass(desiredTime, days, hours, minutes, seconds);
  // Note JSON Stringify is needed for test to pass, known jest issue: https://github.com/facebook/jest/issues/5998
  timeUI = JSON.stringify(timeUI);
  expect(timeUI).toBe(JSON.stringify(<span className="font-bold">30<span className="">s</span></span>));
});

it('getConstantInputParams all const', () => {
  const constInputParams = JobListActions.getConstantInputParams(allJobs[0].input_params);
  expect(constInputParams.length).toBe(3);
});

it('getConstantInputParams with non const', () => {
  const constInputParams = JobListActions.getConstantInputParams(allJobs[0].input_params);
  expect(constInputParams.length).toBe(3);
});

it('getInputMetricValue metric const', () => {
  const value = JobListActions.getInputMetricValue(constParam, isMetric, columns);
  expect(value).toBe('abc');
});

it('getInputMetricValue metric non const', () => {
  const value = JobListActions.getInputMetricValue(nonConstParam, isMetric, columns);
  expect(value).toBe('123');
});

it('getInputMetricValue no metric const', () => {
  const value = JobListActions.getInputMetricValue(constParam, noMetric, columns);
  expect(value).toBe('abc');
});

it('getInputMetricValue no metric non const', () => {
  const value = JobListActions.getInputMetricValue(nonConstParam, noMetric, columns);
  expect(value).toBe('123');
});

it('getInputMetricValue metric const value 0', () => {
  const value = JobListActions.getInputMetricValue(zeroConstParam, isMetric, columns);
  expect(value).toBe(0);
});

it('getInputMetricValue no metric const value 0', () => {
  const value = JobListActions.getInputMetricValue(zeroConstParam, noMetric, columns);
  expect(value).toBe(0);
});

it('getInputMetricValue metric non const value 0', () => {
  const value = JobListActions.getInputMetricValue(zeroNonConstParam, isMetric, columns);
  expect(value).toBe(0);
});

it('getInputMetricValue no metric non const value 0', () => {
  const value = JobListActions.getInputMetricValue(zeroNonConstParam, noMetric, columns);
  expect(value).toBe(0);
});

it('getInputMetricValue metric const value null', () => {
  const value = JobListActions.getInputMetricValue(nullConstParam, isMetric, columns);
  expect(value).toBe('not available');
});

it('getInputMetricValue no metric const value null', () => {
  const value = JobListActions.getInputMetricValue(nullConstParam, noMetric, columns);
  expect(value).toBe('not available');
});

it('getInputMetricValue rounds positive constant metric number to 5 significant figures', () => {
  const param = {
    name: 'abc',
    source: 'constant',
    value: 1.1234567
  };

  const value = JobListActions.getInputMetricValue(param, isMetric, columns);
  expect(value).toBe(1.1235);
});

it('getInputMetricValue rounds negative non-constant non metric number to 5 significant figures', () => {
  const param = {
    name: 'abc',
    source: 'non-constant',
    value: -3.00065456e-3
  };

  const value = JobListActions.getInputMetricValue(param, noMetric, columns);
  expect(value).toBe(-3.0007e-3);
});

it('getInputMetricValue rounds megative constant metric number to 5 significant figures', () => {
  const param = {
    name: 'abc',
    source: 'constant',
    value: -1.1234567
  };

  const value = JobListActions.getInputMetricValue(param, isMetric, columns);
  expect(value).toBe(-1.1235);
});

it('getInputMetricValue rounds positive non-constant non metric number to 5 significant figures', () => {
  const param = {
    name: 'abc',
    source: 'non-constant',
    value: 3.00065456e-3
  };

  const value = JobListActions.getInputMetricValue(param, noMetric, columns);
  expect(value).toBe(3.0007e-3);
});

it('getInputMetricValue const metric returns NaN if given NaN', () => {
  const param = {
    name: 'abc',
    source: 'constant',
    value: NaN
  };

  const value = JobListActions.getInputMetricValue(param, isMetric, columns);
  expect(value).toBe(NaN);
});

it('getInputMetricValue non-const no metric returns NaN if given NaN', () => {
  const param = {
    name: 'abc',
    source: 'non-constant',
    value: NaN
  };

  const value = JobListActions.getInputMetricValue(param, noMetric, columns);
  expect(value).toBe(NaN);
});

it('getBaseJobListingURL', () => {
  const URL = JobListActions.getBaseJobListingURL(projectName);
  expect(URL).toBe('projects/project name/job_listing');
});

it('getFilterURL only 1 type', () => {
  const URL = JobListActions.getFilterURL(hiddenStatusFilter, emptyFilters, emptyFilters, emptyFilters, emptyFilters, emptyFilters, emptyFilters, emptyFilters);
  expect(URL).toBe('status=Processing,Failed');
});

it('getFilterURL more than 1 type', () => {
  const URL = JobListActions.getFilterURL(hiddenStatusFilter, hiddenUserFilter, emptyFilters, emptyFilters, emptyFilters, emptyFilters, emptyFilters, emptyFilters);
  expect(URL).toBe('status=Processing,Failed&user=hidden1,hidden2');
});

it('areStatusesHidden hidden', () => {
  const areHidden = JobListActions.areStatusesHidden(hiddenStatusFilter);
  expect(areHidden).toBe(true)
});

it('areStatusesHidden not hidden', () => {
  const areHidden = JobListActions.areStatusesHidden(noHiddenStatusFilter);
  expect(areHidden).toBe(false)
});

it('getAllFilters', () => {
  const updatedFilters = JobListActions.getAllFilters(hiddenStatusFilter, allUsers, hiddenUserFilter, emptyFilters, emptyFilters, emptyFilters, emptyFilters, emptyFilters, emptyFilters);
  expect(updatedFilters.length).toBe(6);

});

it('getStatusFilters', () => {
  const updatedFilters = JobListActions.getStatusFilters(filters, hiddenStatusFilter);
  expect(updatedFilters.length).toBe(3);
});

it('removeFilter', () => {
  const updatedFilters = JobListActions.removeFilter(filters, filterToRemove);
  expect(updatedFilters.length).toBe(1);
  expect(updatedFilters[0].value).toBe('Buck');
});

it('getAllJobUsers', () => {
  const allUsers = JobListActions.getAllJobUsers(jobs);
  expect(allUsers.length).toBe(2);
});

it('addtoURL, first status', () => {
  const updatedUrl = JobListActions.addToURL(url, isFirst, colValue, colName);
  expect(updatedUrl).toBe('localhost/myCol=myVal');
});

it('addtoURL, not first status', () => {
  const updatedUrl = JobListActions.addToURL(url, isNotFirst, colValue, colName);
  expect(updatedUrl).toBe('localhost/,myVal');
});

it('getFilterObject', () => {
  const filteredObject = JobListActions.getFilterObject(colName, colValue);
  expect(filteredObject).toEqual({ column: 'myCol', value: 'myVal' });
});

it('addStatusToURLNotHidden, not hidden', () => {
  const updatedUrl = JobListActions.addStatusToURLNotHidden(url, isFirst, status);
  expect(updatedUrl).toBe('localhost/status=Failed');
});

it('addStatusToURLNotHidden, hidden', () => {
  status.hidden = true;
  const updatedUrl = JobListActions.addStatusToURLNotHidden(url, isFirst, status);
  expect(updatedUrl).toBe('localhost/');
});

it('getOldStatusFilters', () => {
  const oldFilters = JobListActions.getOldStatusFilters(filters);
  expect(oldFilters.length).toBe(1);
  expect(oldFilters[0].column).toBe('User');
});

it('addNewStatusFilters', () => {
  const newFilters = [];
  JobListActions.addNewStatusFilters(hiddenStatusFilter, newFilters);
  expect(newFilters.length).toBe(2);
});

it('getUpdatedStatusesFromOldStatuses', () => {
  const newStatuses = [];
  JobListActions.getUpdatedStatusesFromOldStatuses(filters, status, isNotFirst, newStatuses);
  expect(newStatuses.length).toBe(1);
});

it('updateStatusesIfNoFilters, has filters', () => {
  JobListActions.updateStatusesIfNoFilters(hasFilter, hiddenStatusFilter);
  expect(hiddenStatusFilter[2].hidden).toBe(true);
});

it('updateStatusesIfNoFilters, no filters', () => {
  JobListActions.updateStatusesIfNoFilters(noFilter, hiddenStatusFilter);
  expect(hiddenStatusFilter[0].hidden).toBe(false);
});

it('addToURLNotHidden first', () => {
  const newURL = JobListActions.addToURLNotHidden(url, isFirst, colValue, colName);
  expect(newURL).toBe('localhost/myCol=myVal');
});

it('addToURLNotHidden not first', () => {
  const newURL = JobListActions.addToURLNotHidden(url, isNotFirst, colValue, colName);
  expect(newURL).toBe('localhost/,myVal');
});

it('addAndIfNotFirstFilter, first', () => {
  const newURL = JobListActions.addAndIfNotFirstFilter(url, isFirst);
  expect(newURL).toBe('localhost/');
});

it('addAndIfNotFirstFilter, not first', () => {
  const newURL = JobListActions.addAndIfNotFirstFilter(url, isNotFirst);
  expect(newURL).toBe('localhost/&');
});

it('updateHiddenParams', () => {
  const newHiddenParams = JobListActions.updateHiddenParams(allUsers, newHiddenUser, hiddenUserFilter);
  expect(newHiddenParams.length === 3);
  expect(newHiddenParams[2]).toBe('user2');

});

it('willHideAllParams', () => {
  const willHide = JobListActions.willHideAllParams(allUsers, hiddenUserFilter);
  expect(willHide).toBe(false);
});

it('addToURLRangeNotHidden', () => {
  const newURL = JobListActions.addToURLRangeNotHidden(url, startValue, endValue, colName);
  expect(newURL).toBe('localhost/myCol_starts=1&myCol_ends=2');
});

it('getRangeFilter', () => {
  const rangeFilter = JobListActions.getRangeFilter(colName, startValue, endValue);
  expect(rangeFilter).toEqual({"column": "myCol", "value": "1 - 2"});
});

it('getExistingValuesForFilter, not existing', () => {
  const existingValues = JobListActions.getExistingValuesForFilter(allFilters, colName);
  expect(existingValues).not.toEqual(null);
});

it('getExistingValuesForFilter, existing', () => {
  const existingValues = JobListActions.getExistingValuesForFilter(allFilters, nonExistingFilter);
  expect(existingValues).toBe(null);
});

it('removeFilterByName, not exists', () => {
  const updatedFilters = JobListActions.removeFilterByName(allFilters, nonExistingFilter);
  expect(updatedFilters.length).toBe(1);
});

it('removeFilterByName, exists', () => {
  const updatedFilters = JobListActions.removeFilterByName(allFilters, removeFilter);
  expect(updatedFilters.length).toBe(0);
});

it('addToURLContainFilter', () => {
  const newURL = JobListActions.addToURLContainFilter(url, containValue, colName)
  expect(newURL).toBe('localhost/myCol_contains=testPhrase');
});

it('getContainFilter', () => {
  const containFilter = JobListActions.getContainFilter(colName, containValue);
  expect(containFilter).toEqual({"column": "myCol", "value": "\"testPhrase\""});
});

it('boolFilterArrayHasHidden, has hidden', () => {
  const hasHidden = JobListActions.boolFilterArrayHasHidden(hiddenBoolFilter);
  expect(hasHidden).toBe(true);
});

it('boolFilterArrayHasHidden, none hidden', () => {
  const hasHidden = JobListActions.boolFilterArrayHasHidden(noneHiddenBoolFilter);
  expect(hasHidden).toBe(false);
});

it('boolFilterHasHidden, had hidden', () => {
  const hasHidden = JobListActions.boolFilterHasHidden(hiddenBoolFilter[0]);
  expect(hasHidden).toBe(true);
});

it('boolFilterHasHidden, none hidden', () => {
  const hasHidden = JobListActions.boolFilterHasHidden(noneHiddenBoolFilter[0]);
  expect(hasHidden).toBe(false);
});

it('boolFilterGetNonHidden, has hidden', () => {
  const hidden = JobListActions.boolFilterGetNonHidden(hiddenBoolFilter[0]);
  expect(hidden.length).toBe(0);
});

it('boolFilterGetNonHidden, none hidden', () => {
  const hidden = JobListActions.boolFilterGetNonHidden(noneHiddenBoolFilter[0]);
  expect(hidden.length).toBe(1);
});

it('boolFilterGetHidden, has hidden', () => {
  const hidden = JobListActions.boolFilterGetHidden(hiddenBoolFilter[0].boolCheckboxes);
  expect(hidden.length).toBe(1);
});

it('boolFilterGetHidden, none hidden', () => {
  const hidden = JobListActions.boolFilterGetHidden(noneHiddenBoolFilter[0].boolCheckboxes);
  expect(hidden.length).toBe(0);
});

it('getTimeForDurationURL', () => {
  const urlTime = JobListActions.getTimeForDurationURL(time);
  expect(urlTime).toBe('1_2_3_4');
});

it('getTimeForDurationBubble', () => {
  const bubbleTime = JobListActions.getTimeForDurationBubble(time);
  expect(bubbleTime).toBe('1d2h3m4s');
});

it('areNoFilters, no filters', () => {
  const noFilters = JobListActions.areNoFilters(emptyFilters, emptyFilters, emptyFilters, emptyFilters, emptyFilters, emptyFilters, emptyFilters, emptyFilters);
  expect(noFilters).toBe(true);
});

it('areNoFilters, has filters', () => {
  const noFilters = JobListActions.areNoFilters(emptyFilters, emptyFilters, emptyFilters, emptyFilters, hiddenBoolFilter, emptyFilters, emptyFilters, emptyFilters);
  expect(noFilters).toBe(false);
});

// Pending cause of Jenkins Timezone UTC vs EST issue
xit('getTimeForStartTimeURL', () => {
  const newURL = JobListActions.getTimeForStartTimeURL(dateTime);
  expect(newURL).toBe('03_24_2015_20_00');
});

it('prependZero, single digit', () =>{
  const newDigit = JobListActions.prependZero(singleDigit);
  expect(newDigit).toBe('01');
});

it('prependZero, 2 digit', () => {
  const newDigit = JobListActions.prependZero(doubleDigit);
  expect(newDigit).toBe('11');
});

// Pending cause of Jenkins Timezone UTC vs EST issue
xit('getTimeForStartTimeBubble', () => {
  const bubble = JobListActions.getTimeForStartTimeBubble(dateTime);
  expect(bubble).toBe('03/24/15 20:00');
});

it('isColumnFiltered, is filtered', () => {
  const isFiltered = JobListActions.isColumnFiltered(columnFilter, existingColumn);
  expect(isFiltered).toBe(true);
});

it('isColumnFiltered, not filter', () => {
  const isFiltered = JobListActions.isColumnFiltered(columnFilter, nonExistingColumn);
  expect(isFiltered).toBe(false);
});

it('Redirect returns Redirect', () => {
  const redirectOutput = JobListActions.redirect("/login");
  expect(redirectOutput).toEqual(<Redirect push to="/login" />);
})