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

// function mockFetchError(data, status) {
//   return jest.fn().mockImplementation(() => {
//     Promise.reject(new Error())
//   });
// }

it('Gets Result and Status from API', async () => {
  fetch = mockFetch('data', 404);
  const [status, result] = await BaseActions.getFromAPI('some_query_url');
  expect(status).toEqual(404);
  expect(result).toEqual('data');
  expect(fetch).toHaveBeenCalledTimes(1);
});

it('Gets Result and Status from BetaAPI', async () => {
  fetch = mockFetch('other_data', 500);
  const [status, result] = await BaseActions.getBetaFromAPI('some_query_url');
  expect(status).toEqual(500);
  expect(result).toEqual('other_data');
  expect(fetch).toHaveBeenCalledTimes(1);
});

it('Posts Results to API', async () => {
  fetch = mockFetch('OK', 200);
  const [status, result] = await BaseActions.postToAPI('login', 'some body');
  expect(status).toEqual(200);
  expect(result).toEqual('OK');
  expect(fetch).toHaveBeenCalledTimes(1);
  expect(fetch).toBeCalledWith( 
    'http://private-83924-dessa.apiary-mock.com/api/v1/login', 
    {
      method: 'POST',
      body: 'some body'
    }
  )
});


it('Posts Results to API Different Data', async () => {
  fetch = mockFetch('banana', 400);
  const [status, result] = await BaseActions.postToAPI('login', 'some body else');
  expect(status).toEqual(400);
  expect(result).toEqual('banana');
  expect(fetch).toHaveBeenCalledTimes(1);
  expect(fetch).toBeCalledWith( 
    'http://private-83924-dessa.apiary-mock.com/api/v1/login', 
    {
      method: 'POST',
      body: 'some body else'
    }
  )
});

// it('Posts Results Returns Null If Error', async () => {
//   // expect.assertions(1);
//   fetch = mockFetchError();
//   const result = await BaseActions.postToAPI('login', 'some body else');
//   expect(result).toEqual(null);
//   expect(fetch).toHaveBeenCalledTimes(1);
// });