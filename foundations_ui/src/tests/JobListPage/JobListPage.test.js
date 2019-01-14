import React from 'react';
import ReactDOM from 'react-dom';
import JobListPage from '../../js/components/JobListPage/JobListPage';
import { shallow, mount } from 'enzyme';
import { MemoryRouter } from 'react-router-dom';
import configureTests from '../setupTests';

configureTests();

it('Shallow Renders Job List Page', () => {
  const wrapper = shallow(<JobListPage/>);
  expect(wrapper).toMatchSnapshot();
});

// Won't actually get anything unless `projectName` is a project name
// in your API
it('Calls Get Job List', async () => {
  <MemoryRouter>
    const wrapper = mount(<JobListPage projectName='myProject'/>); 
    const postState = wrapper.state();
    expect(postState.isLoaded === true);
  </MemoryRouter>
});