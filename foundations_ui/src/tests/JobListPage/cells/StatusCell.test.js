import React from 'react';
import ReactDOM from 'react-dom';
import { shallow } from 'enzyme';
import StatusCell from '../../../js/components/JobListPage/cells/StatusCell';
import configureTests from '../../setupTests';

configureTests();

it('Shallow Renders Status Cell', () => {
  const wrapper = shallow(<StatusCell />);
  expect(wrapper).toMatchSnapshot();
});
