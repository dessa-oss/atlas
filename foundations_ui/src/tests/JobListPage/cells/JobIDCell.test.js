import React from 'react';
import ReactDOM from 'react-dom';
import JobIDCell from '../../../js/components/JobListPage/cells/JobIDCell';
import { shallow } from 'enzyme';
import configureTests from '../../setupTests';

configureTests();

it('Shallow Renders Job ID Cell', () => {
  const wrapper = shallow(<JobIDCell/>);
  expect(wrapper).toMatchSnapshot();
});

it('Sets Expand State Upon Hover', () => {
  const wrapper = shallow(<JobIDCell/>);
  wrapper.find('div').first().simulate('mouseEnter');
  expect(wrapper.state("expand")).toEqual(true);
  wrapper.find('div').first().simulate('mouseLeave');
  expect(wrapper.state("expand")).toEqual(false);
});
