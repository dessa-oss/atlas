import React from 'react';
import ReactDOM from 'react-dom';
import StatusFilter from '../../js/components/common/filters/StatusFilter';
import { shallow, mount } from 'enzyme';
import configureTests from '../setupTests';

configureTests();

it('Shallow Renders StatusFilter', () => {
  const wrapper = shallow(<StatusFilter/>);
  expect(wrapper).toMatchSnapshot();
});
