import React from 'react';
import ReactDOM from 'react-dom';
import JobTableRow from '../../js/components/JobListPage/JobTableRow';
import { shallow, mount } from 'enzyme';
import configureTests from '../setupTests';

configureTests();

it('Shallow Renders Job Table Row', () => {
  const wrapper = shallow(<JobTableRow/>);
  expect(wrapper).toMatchSnapshot();
});
