import React from 'react';
import ReactDOM from 'react-dom';
import { shallow, mount } from 'enzyme';
import { Redirect } from 'react-router-dom';
import configureTests from '../setupTests';
import ProjectActions from '../../js/actions/ProjectActions';

configureTests();

const projects = [
  {
    name: 'proj1',
    created_at: 'today'
  },
  {
    name: 'proj2',
    created_at: 'yesterday'
  }
];
const funcStub = () => {};

it('get AllProjects', () => {
  const allProjects = ProjectActions.getAllProjects(projects, funcStub);
  expect(allProjects.length).toBe(2);
});
