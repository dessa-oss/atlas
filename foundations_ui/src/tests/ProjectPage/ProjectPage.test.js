import React from 'react';
import ReactDOM from 'react-dom';
import ProjectPage from '../../js/components/ProjectPage/ProjectPage';
import { shallow, mount } from 'enzyme';
import { MemoryRouter } from 'react-router-dom';
import configureTests from '../setupTests';
import ProjectActions from '../../js/actions/ProjectActions';
import LoginPage from '../../js/components/LoginPage/LoginPage';

configureTests();

it('Shallow Renders ProjectPage', () => {
  const wrapper = shallow(<ProjectPage/>);
  expect(wrapper).toMatchSnapshot();
});

it('Calls Get All Projects', async () => {
  <MemoryRouter>
    const wrapper = mount(<ProjectPage/>); 
    const preState = wrapper.state();
    await wrapper.instance().getAllProjects();
    const postState = wrapper.state();
    expect(preState.isLoaded === false);
    expect(postState.isLoaded === true);
  </MemoryRouter>
});

// Assumes your API has projects
it('Has at least One Project', async () => {
  <MemoryRouter>
    const wrapper = mount(<ProjectPage/>); 
    const preState = wrapper.state();
    await wrapper.instance().getAllProjects();
    const postState = wrapper.state();
    expect(preState.projects.length === 0);
    expect(postState.projects.length > 0);
  </MemoryRouter>
});

it('Sets QueryStatus Based on getProjects Response', async () => {
  <MemoryRouter>
    ProjectActions.getProjects = jest.fn();
    ProjectActions.getProjects.status.mockReturnValue({404});
    const wrapper = mount(<ProjectPage/>); 
    const preState = wrapper.state();
    await wrapper.instance().getAllProjects();
    expect(preState.queryStatus).toEqual(200);
    expect(wrapper.state.queryStatus).toEqual(404);
  </MemoryRouter>
});

it('Calls Redirect to the Login Page if QueryStatus is 401', () => {
  const wrapper = shallow(<ProjectPage />)
  ProjectActions.redirect = jest.fn();
  wrapper.setState({
    queryStatus: 401,
    isLoaded: true,
  });
  expect(ProjectActions.redirect).toBeCalledWith('/login');
});
