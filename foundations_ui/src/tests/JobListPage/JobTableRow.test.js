import React from 'react';
import ReactDOM from 'react-dom';
import JobTableRow from '../../js/components/JobListPage/JobTableRow';
import { shallow, mount } from 'enzyme';
import configureTests from '../setupTests';

configureTests();

const job = {
  status: 'completed',
};

it('Shallow Renders Job Table Row', () => {
  const wrapper = shallow(<JobTableRow job={job} />);
  expect(wrapper).toMatchSnapshot();
});
