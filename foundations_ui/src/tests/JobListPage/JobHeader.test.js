import React from 'react';
import ReactDOM from 'react-dom';
import JobHeader from '../../js/components/JobListPage/JobHeader';
import { shallow, mount } from 'enzyme';
import configureTests from '../setupTests';

configureTests();

it('Shallow Renders Job List Page', () => {
  const wrapper = shallow(<JobHeader/>);
  expect(wrapper).toMatchSnapshot();
});
