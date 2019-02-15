import React from 'react';
import ReactDOM from 'react-dom';
import JobListPage from '../../js/components/JobListPage/JobListPage';
import { shallow, mount } from 'enzyme';
import { MemoryRouter } from 'react-router-dom';
import configureTests from '../setupTests';
import JobListActions from '../../js/actions/JobListActions'

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

it('Calls Redirect to the Login Page if QueryStats is 401', () => {
  const wrapper = shallow(<JobListPage />)
  JobListActions.redirect = jest.fn();
  wrapper.setState({
    queryStatus: 401,
  });
  expect(JobListActions.redirect).toBeCalledWith('/login');
});

it('Sets QueryStatus Based On Fetch Response', () => {
  <MemoryRouter>
    JobListActions.getJobs = jest.fn();
    JobListActions.getJobs.status.mockReturnValue({404});
    const wrapper = mount(<JobListPage projectName='myProject'/>);
    const preState = wrapper.state();
    await wrapper.instance().getJobs() 
    const postState = wrapper.state();
    expect(preState.queryStatus === 200);
    expect(postState.queryStatus === 404);
  </MemoryRouter>
});