import React from 'react'
import ReactDOM from 'react-dom'
import { shallow, mount } from 'enzyme'
import { Redirect } from 'react-router-dom'
import configureTests from '../setupTests'
import LoginActions from '../../js/actions/LoginActions'
import BaseActions from '../../js/actions/BaseActions'

configureTests()

it('postLogin calls BaseActions.postToAPI', () => {
  BaseActions.postToAPI = jest.fn();
  LoginActions.postLogin('some body once told me');
  expect(BaseActions.postToAPI).toBeCalledWith('login', 'some body once told me');
});

it('Redirect returns Redirect', () => {
  const redirectOutput = LoginActions.redirect('/projects');
  expect(redirectOutput).toEqual(<Redirect push to='/projects' />);
});
