import React from 'react';
import ReactDOM from 'react-dom';
import { shallow, mount } from 'enzyme';
import configureTests from '../setupTests';
import ErrorMessage from '../../js/components/common/ErrorMessage';

configureTests();

it('Shallow Renders ErrorMessage', () => {
  const wrapper = shallow(<ErrorMessage/>);
  expect(wrapper).toMatchSnapshot();
});

it('Calls Correct Function for 500 Error', () => {
  const spy_content = jest.spyOn(ErrorMessage.prototype, 'setContent');
  const spy_500 = jest.spyOn(ErrorMessage.prototype, 'setInternalServerError');
  const wrapper = shallow(<ErrorMessage errorCode={500}/>);
  expect(spy_content).toHaveBeenCalled();
  expect(spy_500).toHaveBeenCalled();
});

it('Returns Correct Banner and Subtext for 500 Error', () => {
  const wrapper = shallow(<ErrorMessage errorCode={500}/>);
  const returnValues = wrapper.instance().setContent();
  expect(returnValues.errorBanner).toEqual('500 Internal Server Error');
  expect(returnValues.errorSubtext).toEqual('Our servers are having problems '
  + 'going through the astroid belts.'
  + ' Check back again shortly.')
});

it('Calls Correct Function for 404 Error', () => {
  const spy_content = jest.spyOn(ErrorMessage.prototype, 'setContent');
  const spy_404 = jest.spyOn(ErrorMessage.prototype, 'setNotFoundError');
  const wrapper = shallow(<ErrorMessage errorCode={404}/>);
  expect(spy_content).toHaveBeenCalled();
  expect(spy_404).toHaveBeenCalled();
});

it('Returns Correct Banner and Subtext for 404 Error', () => {
  const wrapper = shallow(<ErrorMessage errorCode={404}/>);
  const returnValues = wrapper.instance().setContent();
  expect(returnValues.errorBanner).toEqual('404 Page Not Found');
  expect(returnValues.errorSubtext).toEqual('Services are having temporary issues.'
  + ' Contact our front desk support at support@dessa.com or call us toll free at 1-899-623-5578.')
});