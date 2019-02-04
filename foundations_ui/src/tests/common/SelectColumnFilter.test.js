import React from 'react';
import ReactDOM from 'react-dom';
import SelectColumnFilter from '../../js/components/common/filters/SelectColumnFilter';
import { shallow, mount } from 'enzyme';
import configureTests from '../setupTests';

configureTests();

it('Shallow Renders SelectColumnFilter', () => {
  const wrapper = shallow(<SelectColumnFilter/>);
  expect(wrapper).toMatchSnapshot();
});

it('Change input selectColumnFilter', () => {
  const wrapper = mount(<SelectColumnFilter/>);
  const input = wrapper.find('input').getDOMNode();
  const button = wrapper.find('button').at(2);
  input.value = 'Test';
  expect(input.value).toBe('Test');
  wrapper.instance().onClearFilters();
  const updatedInput = wrapper.find('input').getDOMNode();
  expect(updatedInput.value).toBe('');
});