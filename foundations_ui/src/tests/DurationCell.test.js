import React from 'react';
import ReactDOM from 'react-dom';
import DurationCell from '../js/components/JobListPage/cells/DurationCell';
import { shallow } from 'enzyme';
import configureTests from './setupTests';

configureTests();

it('Shallow Render Duration Cell', () => {
  const wrapper = shallow(<DurationCell/>);
  expect(wrapper).toMatchSnapshot();
});