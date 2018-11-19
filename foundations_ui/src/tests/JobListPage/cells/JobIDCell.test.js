import React from 'react';
import ReactDOM from 'react-dom';
import JobIDCell from '../../../js/components/JobListPage/cells/JobIDCell';
import { shallow } from 'enzyme';
import configureTests from '../../setupTests';

configureTests();

it('Shallow Renders Job ID Cell', () => {
  const wrapper = shallow(<JobIDCell/>);
  expect(wrapper).toMatchSnapshot();
});