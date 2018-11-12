import React from 'react';
import ReactDOM from 'react-dom';
import Toolbar from '../js/components/common/Toolbar';
import { shallow } from 'enzyme';
import configureTests from './setupTests';

configureTests();

it('Shallow Renders Toolbar Home', () => {
  const wrapper = shallow(<Toolbar/>);
  expect(wrapper).toMatchSnapshot();
});