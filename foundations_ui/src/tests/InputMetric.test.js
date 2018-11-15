import React from 'react';
import ReactDOM from 'react-dom';
import InputMetric from '../js/components/common/InputMetric';
import { shallow, mount } from 'enzyme';
import configureTests from './setupTests';

configureTests();

it('Shallow Renders InputMetric', () => {
  const wrapper = shallow(<InputMetric/>);
  expect(wrapper).toMatchSnapshot();
});