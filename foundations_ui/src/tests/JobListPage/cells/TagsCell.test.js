import React from 'react';
import ReactDOM from 'react-dom';
import TagsCell from '../../../js/components/JobListPage/cells/TagsCell';
import { shallow } from 'enzyme';
import configureTests from '../../setupTests';

configureTests();

it('Shallow Renders Tags Cell', () => {
  const wrapper = shallow(<TagsCell/>);
  expect(wrapper).toMatchSnapshot();
});