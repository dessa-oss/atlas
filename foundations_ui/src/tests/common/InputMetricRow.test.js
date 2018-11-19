import React from 'react';
import ReactDOM from 'react-dom';
import InputMetricRow from '../../js/components/common/InputMetricRow';
import { shallow, mount } from 'enzyme';
import configureTests from '../setupTests';

configureTests();

it('Shallow Renders InputMetricRow', () => {
  const wrapper = shallow(<InputMetricRow/>);
  expect(wrapper).toMatchSnapshot();
});