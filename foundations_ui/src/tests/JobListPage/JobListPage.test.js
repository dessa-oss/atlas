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

// Won't actually get anything unless `projectName` is a project name
// in your API
it('Calls Get Job List', async () => {
  const wrapper = mount(<JobListPage/>); 
  const preState = wrapper.state();
  await wrapper.instance().getJobs('projectName');
  const postState = wrapper.state();
  expect(preState.isLoaded === false);
  expect(postState.isLoaded === true);
});