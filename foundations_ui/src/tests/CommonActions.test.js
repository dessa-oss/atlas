import React from 'react';
import ReactDOM from 'react-dom';
import CommonActions from '../js/actions/CommonActions';
import { shallow, mount } from 'enzyme';
import configureTests from './setupTests';

configureTests();

const inputParams = [
  'myParam',
  'my2ndParam',
];

it('get InputMetricColumnHeaders', () => {
  const headers = CommonActions.getInputMetricColumnHeaders(inputParams);
  expect(headers.length).toBe(2);
});