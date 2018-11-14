import React from 'react';
import ReactDOM from 'react-dom';
import { shallow, mount } from 'enzyme';
import configureTests from '../setupTests';
import JobActions from '../../js/actions/JobListActions';

configureTests();

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
  expect(timeUI).toBe(JSON.stringify(<span className="duration-day-number header-4 font-bold">3<span className="font-regular">d </span></span>));
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
  expect(timeUI).toBe(JSON.stringify(<span className="duration-hour-number header-4 font-bold">6<span className="font-regular">h </span></span>));
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
  expect(timeUI).toBe(JSON.stringify(<span className="duration-minute-number header-4 font-bold">12<span className="font-regular">m </span></span>));
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
  expect(timeUI).toBe(JSON.stringify(<span className="duration-second-number header-4 font-bold">30<span className="font-regular">s</span></span>));
});