import React from 'react';
import ReactDOM from 'react-dom';
import JobTable from '../js/components/JobListPage/JobTable';
import { shallow, mount } from 'enzyme';
import configureTests from './setupTests';

configureTests();

it('Shallow Renders Job Table', () => {
  const wrapper = shallow(<JobTable/>);
  expect(wrapper).toMatchSnapshot();
});

// Won't actually get anything unless `projectName` is a project name
// in your API
it('Calls Get Job List', async () => {
  const wrapper = mount(<JobTable/>); 
  const preState = wrapper.state();
  await wrapper.instance().getJobs('projectName');
  const postState = wrapper.state();
  expect(preState.isLoaded === false);
  expect(postState.isLoaded === true);
});