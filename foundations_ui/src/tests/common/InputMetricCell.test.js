import React from 'react';
import ReactDOM from 'react-dom';
import InputMetricCell from '../../js/components/common/InputMetricCell';
import { shallow, mount } from 'enzyme';
import configureTests from '../setupTests';

configureTests();

it('Shallow Renders InputMetricCell', () => {
  const wrapper = shallow(<InputMetricCell/>);
  expect(wrapper).toMatchSnapshot();
});