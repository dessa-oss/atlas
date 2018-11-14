import React from 'react';
import ReactDOM from 'react-dom';
import JobTableHeader from '../js/components/JobListPage/JobTableHeader';
import { shallow, mount } from 'enzyme';
import configureTests from './setupTests';

configureTests();

it('Shallow Renders Job Table Header', () => {
  const wrapper = shallow(<JobTableHeader/>);
  expect(wrapper).toMatchSnapshot();
});