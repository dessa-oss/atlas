import React from 'react';
import ReactDOM from 'react-dom';
import HoverCell from '../../../js/components/JobListPage/cells/HoverCell';
import { shallow, mount } from 'enzyme';
import configureTests from '../../setupTests';

configureTests();

it('Shallow Renders HoverCell', () => {
    const wrapper = shallow(<HoverCell/>);
    expect(wrapper).toMatchSnapshot();
  });