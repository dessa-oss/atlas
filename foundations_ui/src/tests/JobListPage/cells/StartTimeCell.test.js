import React from 'react';
import ReactDOM from 'react-dom';
import StartTimeCell from '../../../js/components/JobListPage/cells/StartTimeCell';
import { shallow } from 'enzyme';
import configureTests from '../../setupTests';

configureTests();

it('Shallow Renders Start Time Cell', () => {
  const wrapper = shallow(<StartTimeCell/>);
  expect(wrapper).toMatchSnapshot();
});

it('Sets Expand State Upon Hover', () => {
  const wrapper = shallow(<StartTimeCell/>);
  wrapper.find('div').first().simulate('mouseEnter');
  expect(wrapper.state("expand")).toEqual(true);
  wrapper.find('div').first().simulate('mouseLeave');
  expect(wrapper.state("expand")).toEqual(false);
});