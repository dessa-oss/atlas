import React from 'react';
import ReactDOM from 'react-dom';
import TableStaticColumns from '../../js/components/JobListPage/TableStaticColumns';
import { shallow, mount } from 'enzyme';
import configureTests from '../setupTests';

configureTests();

it('Shallow Renders TableStaticColumns', () => {
  const wrapper = shallow(<TableStaticColumns/>);
  expect(wrapper).toMatchSnapshot();
});
