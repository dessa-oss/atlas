import React from 'react';
import ReactDOM from 'react-dom';
import fake from 'faker';
import LoginPage from '../../js/components/LoginPage/LoginPage';
import { shallow, mount } from 'enzyme';
import { MemoryRouter } from 'react-router-dom';
import configureTests from '../setupTests';
import ErrorMessage from '../../js/components/common/ErrorMessage';

import LoginActions from '../../js/actions/LoginActions';

configureTests();

it('Shallow Renders ProjectPage', () => {
  const wrapper = shallow(<LoginPage/>);
  expect(wrapper).toMatchSnapshot();
});

it('isLoggedIn is null by Default', () => {
    const wrapper = shallow(<LoginPage/>);
    expect(wrapper.state('isLoggedIn')).toEqual(null)
});

// it("Sets isLoggedIn to True on Login", async () => {
//     LoginActions.getLogin = jest.fn().mockResolvedValue([200, 'OK']);
//     const wrapper = shallow(<LoginPage/>);
//     await wrapper.instance().login('user', 'pass')
//     expect(wrapper.state('isLoggedIn')).toEqual(true)
// });

it("Sets isLoggedIn to False on Login", async () => {
    LoginActions.getLogin = jest.fn().mockResolvedValue([401, 'Unauthorized']);
    const wrapper = shallow(<LoginPage/>);
    const fake_user = fake.lorem.word();
    const fake_pass = fake.lorem.word();
    await wrapper.instance().login(fake_user, fake_pass)
    expect(wrapper.state('isLoggedIn')).toEqual(false)
});

it("Sets loginResponse on Login", async () => {
    LoginActions.getLogin = jest.fn().mockResolvedValue([200, 'OK']);
    const wrapper = shallow(<LoginPage/>);
    await wrapper.instance().login('user', 'pass')
    expect(wrapper.state('loginResponse')).toEqual([200, 'OK'])
});