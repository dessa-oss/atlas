import React from 'react';
import ReactDOM from 'react-dom';
import Tooltip from '../../js/components/common/Tooltip';
import { shallow } from 'enzyme';
import configureTests from '../setupTests';

configureTests();

it('Shallow Renders Tooltip', () => {
  const wrapper = shallow(<Tooltip/>);
  expect(wrapper).toMatchSnapshot();
});