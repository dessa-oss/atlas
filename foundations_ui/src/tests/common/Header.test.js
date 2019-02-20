import React from 'react';
import ReactDOM from 'react-dom';
import Header from '../../js/components/common/Header';
import { shallow, mount } from 'enzyme';
import configureTests from '../setupTests';

configureTests();

it('Shallow Renders ProjectHeader', () => {
  const wrapper = shallow(<Header/>);
  expect(wrapper).toMatchSnapshot();
});

it('Has Projects', () => {
  const numProjects = 3;
  const wrapper = mount(<Header pageTitle='Projects' numProjects={numProjects}/>); 
  const state = wrapper.state();
  expect(state.numProjects > 0);
});

it('Has No Projects', () => {
    const wrapper = mount(<Header pageTitle='Login'/>); 
    const state = wrapper.state();
    expect(state.numProjects === 0);
});

it('Has default pageTitle of Projects', () => {
    const wrapper = mount(<Header />);
    expect(wrapper.state.pageTitle === 'Projects')
})