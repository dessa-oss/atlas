import React from 'react';
import ReactDOM from 'react-dom';
import UserCell from '../js/components/JobListPage/cells/UserCell';
import { shallow } from 'enzyme';
import configureTests from './setupTests';

configureTests();

it('Shallow Renders User Cell', () => {
  const wrapper = shallow(<UserCell/>);
  expect(wrapper).toMatchSnapshot();
});