import React from 'react';
import LoginHeader from '../../js/components/LoginPage/LoginHeader';
import { shallow, mount } from 'enzyme';
import configureTests from '../setupTests';

configureTests();

it('Shallow Renders LoginHeader', () => {
  const wrapper = shallow(<LoginHeader/>);
  expect(wrapper).toMatchSnapshot();
});