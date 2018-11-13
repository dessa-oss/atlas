import React from 'react';
import ReactDOM from 'react-dom';
import JobColumnHeader from '../js/components/common/JobColumnHeader';
import { shallow, mount } from 'enzyme';
import configureTests from './setupTests';

configureTests();

it('Shallow Renders Job Column Header', () => {
  const wrapper = shallow(<JobColumnHeader/>);
  expect(wrapper).toMatchSnapshot();
});