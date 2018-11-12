import React from 'react';
import ReactDOM from 'react-dom';
import ProjectSummary from '../js/components/ProjectPage/ProjectSummary';
import { shallow, mount } from 'enzyme';
import configureTests from './setupTests';

configureTests();

it('Shallow Renders ProjectSummary', () => {
  const wrapper = shallow(<ProjectSummary/>);
  expect(wrapper).toMatchSnapshot();
});

it('Has Projects', () => {
  const project = {
      name: "test",
      owner: "me",
      created_at: "today",
  };
  const wrapper = mount(<ProjectSummary project={project}/>); 
  const state = wrapper.state();
  expect(state.project.name.length > 0);
  expect(state.project.owner.length > 0);
  expect(state.project.created_at.length > 0);
});
