import React from 'react';
import ReactDOM from 'react-dom';
import StartTimeCell from '../js/components/JobListPage/cells/StartTimeCell';
import { shallow } from 'enzyme';
import configureTests from './setupTests';

configureTests();

it('Shallow Renders Start Time Cell', () => {
  const wrapper = shallow(<StartTimeCell/>);
  expect(wrapper).toMatchSnapshot();
});