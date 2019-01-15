import React from 'react';
import ReactDOM from 'react-dom';
import { shallow, mount } from 'enzyme';
import configureTests from '../setupTests';
import ErrorMessage from '../../js/components/common/ErrorMessage';

configureTests();

it('Shallow Renders ErrorMessage', () => {
  const wrapper = shallow(<ErrorMessage/>);
  expect(wrapper).toMatchSnapshot();
});