import React from 'react';
import ReactDOM from 'react-dom';
import LoginPage from '../../js/components/LoginPage/LoginPage';
import { shallow, mount } from 'enzyme';
import { MemoryRouter } from 'react-router-dom';
import configureTests from '../setupTests';
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


it('Calls HandleSubmit on Submit', () => {
    <MemoryRouter>
        const fakeEvent = {preventDefault: () => console.log('preventDefault') };
        const mockedSubmitFunction = jest.fn(event => {
            console.log("Mocked function");
        });
        const wrapper = mount(<LoginPage/>);
        console.log(wrapper.find('form'))
        wrapper.find('form').simulate('submit', fakeEvent)
        expect(wrapper.instance().handleSubmit()).toBeCalled()
    </MemoryRouter>
});

// it("Sets loginResponse and isLoggedIn on Login", () => {
//     LoginActions.postLogin = jest.fn();
//     LoginActions.postLogin.mockReturnValueOnce = [200, 'OK'];
//     const wrapper = shallow(<LoginPage/>);
//     wrapper.instance().login('data')
//     expect(LoginActions.postLogin).toBeCalled()
//     expect(wrapper.state('isLoggedIn')).toEqual(true)
//     expect(wrapper.state('loginResponse')).toEqual([999, 'OK'])

// });

