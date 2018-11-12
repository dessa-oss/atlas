import React from 'react';
import ReactDOM from 'react-dom';
import ProjectHeader from '../js/components/ProjectPage/ProjectHeader';
import { shallow, mount } from 'enzyme';
import configureTests from './setupTests';

configureTests();

it('Shallow Renders ProjectHeader', () => {
  const wrapper = shallow(<ProjectHeader/>);
  expect(wrapper).toMatchSnapshot();
});

it('Has Projects', () => {
  const numProjects = 3;
  const wrapper = mount(<ProjectHeader numProjects={numProjects}/>); 
  const state = wrapper.state();
  expect(state.numProjects > 0);
});