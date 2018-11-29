import React from 'react';
import ReactDOM from 'react-dom';
import ShowMoreFilters from '../../js/components/common/filters/ShowMoreFilters';
import { shallow, mount } from 'enzyme';
import configureTests from '../setupTests';

configureTests();

it('Shallow Renders ShowMoreFilters', () => {
  const wrapper = shallow(<ShowMoreFilters/>);
  expect(wrapper).toMatchSnapshot();
});
