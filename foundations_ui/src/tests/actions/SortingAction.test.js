import React from 'react';
import ReactDOM from 'react-dom';
import { shallow, mount } from 'enzyme';
import configureTests from '../setupTests';
import SortingActions from '../../js/actions/SortingActions';

configureTests();

const jobSortArray = [
  {
    'value': 3,
    'string': 'd',
    'bool': false
  },
  {
    'value': 5,
    'string': 'b',
    'bool': true
  },
  {
    'value': 1,
    'string': 'a',
    'bool': false
  },
  {
    'value': 4,
    'string': 'e',
    'bool': false
  },
  {
    'value': 2,
    'string': 'c',
    'bool': true
  }
];
const sortColNumber = ['value'];
const sortColString = ['string'];
const sortColBool = ['bool'];
const multipleColumnSort = ['bool', 'value'];

it('get sortbyColumn number', () => {
  const sortedArray = SortingActions.sortbyColumn(jobSortArray, sortColNumber);
  expect(sortedArray[0].value).toBe(1);
  expect(sortedArray[1].value).toBe(2);
  expect(sortedArray[2].value).toBe(3);
  expect(sortedArray[3].value).toBe(4);
  expect(sortedArray[4].value).toBe(5);
});

it('get sortbyColumn string', () => {
  const sortedArray = SortingActions.sortbyColumn(jobSortArray, sortColString);
  expect(sortedArray[0].string).toBe('a');
  expect(sortedArray[1].string).toBe('b');
  expect(sortedArray[2].string).toBe('c');
  expect(sortedArray[3].string).toBe('d');
  expect(sortedArray[4].string).toBe('e');
});

it('get sortbyColumn bool', () => {
  const sortedArray = SortingActions.sortbyColumn(jobSortArray, sortColBool);
  expect(sortedArray[0].bool).toBe(false);
  expect(sortedArray[1].bool).toBe(false);
  expect(sortedArray[2].bool).toBe(false);
  expect(sortedArray[3].bool).toBe(true);
  expect(sortedArray[4].bool).toBe(true);
});

it('get sortbyColumn multiple columns', () => {
  const sortedArray = SortingActions.sortbyColumn(jobSortArray, multipleColumnSort);
  expect(sortedArray[0].bool).toBe(false);
  expect(sortedArray[1].bool).toBe(false);
  expect(sortedArray[2].bool).toBe(false);
  expect(sortedArray[3].bool).toBe(true);
  expect(sortedArray[4].bool).toBe(true);
  expect(sortedArray[0].value).toBe(1);
  expect(sortedArray[1].value).toBe(3);
  expect(sortedArray[2].value).toBe(4);
  expect(sortedArray[3].value).toBe(2);
  expect(sortedArray[4].value).toBe(5);
});