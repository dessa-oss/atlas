import React from 'react';
import ReactDOM from 'react-dom';
import { shallow, mount } from 'enzyme';
import { Redirect } from 'react-router-dom';
import configureTests from '../setupTests';
import BaseActions from '../../js/actions/BaseActions';

configureTests();

function mockFetch(data, status) {
  return jest.fn().mockImplementation(() =>
    Promise.resolve({
      status: status,
      json: () => data
    })
  );
}

it('Gets Result and Status from API', async () => {
  fetch = mockFetch('data', 404);
  const response = await BaseActions.getFromAPI('some_query_url')
  expect(response.status).toEqual(404);
  expect(response.result).toEqual('data')
  expect(fetch).toHaveBeenCalledTimes(1);
});

it('Gets Result and Status from BetaAPI', async () => {
  fetch = mockFetch('other_data', 500);
  const response = await BaseActions.getBetaFromAPI('some_query_url')
  expect(response.status).toEqual(500);
  expect(response.result).toEqual('other_data')
  expect(fetch).toHaveBeenCalledTimes(1);
});