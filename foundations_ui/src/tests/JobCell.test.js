import React from 'react';
import ReactDOM from 'react-dom';
import JobCell from '../js/components/JobListPage/cells/JobCell';
import { shallow } from 'enzyme';
import configureTests from './setupTests';

configureTests();

it('Shallow Renders Job Cell', () => {
  const wrapper = shallow(<JobCell/>);
  expect(wrapper).toMatchSnapshot();
});