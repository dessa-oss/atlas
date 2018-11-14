import React from 'react';
import ReactDOM from 'react-dom';
import JobListPage from '../../js/components/JobListPage/JobListPage';
import { shallow, mount } from 'enzyme';
import configureTests from '../setupTests';

configureTests();

it('Shallow Renders Job List Page', () => {
  const wrapper = shallow(<JobListPage/>);
  expect(wrapper).toMatchSnapshot();
});