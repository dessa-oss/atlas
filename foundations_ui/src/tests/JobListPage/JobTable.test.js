import React from 'react';
import ReactDOM from 'react-dom';
import JobTable from '../../js/components/JobListPage/JobTable';
import { shallow, mount } from 'enzyme';
import configureTests from '../setupTests';

configureTests();

it('Shallow Renders Job Table', () => {
  const wrapper = shallow(<JobTable/>);
  expect(wrapper).toMatchSnapshot();
});