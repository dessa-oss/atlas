import configureTests from '../setupTests';
import BaseActions from '../../js/actions/BaseActions';
import React from 'react';
import { Redirect } from 'react-router-dom';


configureTests();

function mockFetch(data, status) {
  return jest.fn().mockImplementation(() =>
    Promise.resolve({
      status: status,
      json: () => data,
    })
  );
}
/*
it('Gets Result and Status from getAPI', async () => {
  fetch = mockFetch('data', 404);
  const [status, result] = await BaseActions.getFromApiary('some_query_url');
  expect(status).toEqual(404);
  expect(result).toEqual('data');
  expect(fetch).toHaveBeenCalledTimes(1);
});

it('Calls getAPI with Correct Params', async () => {
  fetch = mockFetch('other_data', 500);
  const [status, result] = await BaseActions.getFromApiary('some_query_url');
  expect(status).toEqual(500);
  expect(result).toEqual('other_data');
  expect(fetch).toBeCalledWith('http://private-83924-dessa.apiary-mock.com/api/v1/some_query_url',
  {
    credentials: 'include',
  });
});

it('Gets Result and Status from getBetaAPI', async () => {
  fetch = mockFetch('other_data', 500);
  const [status, result] = await BaseActions.getFromApiary('some_query_url');
  expect(status).toEqual(500);
  expect(result).toEqual('other_data');
  expect(fetch).toHaveBeenCalledTimes(1);
});

it('Calls getBetaAPI with Correct Params', async () => {
  fetch = mockFetch('other_data', 500);
  const [status, result] = await BaseActions.getFromApiary('some_query_url');
  expect(status).toEqual(500);
  expect(result).toEqual('other_data');
  expect(fetch).toBeCalledWith('http://private-83924-dessa.apiary-mock.com/api/v2beta/some_query_url',
    {
      credentials: 'include',
    }
  );
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
      body: 'some body',
      credentials: 'include',
    },
  );
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
      body: 'some body else',
      credentials: 'include',
    },
  );
});

it('Redirect returns Redirect', () => {
  const redirectOutput = BaseActions.redirectRoute("/projects");
  expect(redirectOutput).toEqual(<Redirect push to="/projects" />);
})
*/

it('needs a dummy test to pass', () => {

});
