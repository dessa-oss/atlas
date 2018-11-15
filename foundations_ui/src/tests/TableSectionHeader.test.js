import React from 'react';
import ReactDOM from 'react-dom';
import TableSectionHeader from '../js/components/common/TableSectionHeader';
import { shallow, mount } from 'enzyme';
import configureTests from './setupTests';

configureTests();

it('Shallow Renders TableSectionHeader', () => {
  const wrapper = shallow(<TableSectionHeader/>);
  expect(wrapper).toMatchSnapshot();
});