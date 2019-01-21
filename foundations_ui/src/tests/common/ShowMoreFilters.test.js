import React from 'react';
import ReactDOM from 'react-dom';
import ShowMoreFilters from '../../js/components/common/filters/ShowMoreFilters';
import { shallow, mount } from 'enzyme';
import configureTests from '../setupTests';

configureTests();

it('Shallow Renders ShowMoreFilters', () => {
  const wrapper = shallow(<ShowMoreFilters/>);
  expect(wrapper).toMatchSnapshot();
});

it('Calls Callback On Close Button Click', () =>{
  const mockCallback = jest.fn();
  const hiddenBubble = [{id: 'Status-Completed'}];
  const wrapper = shallow(<ShowMoreFilters hiddenBubbles={hiddenBubble} 
    removeFilterCallback={mockCallback}/>
  );
  wrapper.find('button').simulate('click');
  expect(mockCallback).toBeCalledWith({ column:'Status', value:'Completed'});
});
