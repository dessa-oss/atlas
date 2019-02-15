"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch, Mock
from foundations_rest_api.utils.api_resource import api_resource
from test.helpers.api_resource_mocks import APIResourceMocks
from foundations_rest_api.lazy_result import LazyResult
from foundations_rest_api.response import Response

from foundations_internal.testing.helpers.spec import Spec
from foundations_internal.testing.helpers import let, let_patch_mock

class TestAPIResource(Spec):

    @let
    def random_cookie(self):
        return {self.random_cookie_key: self.random_cookie_value}

    @let
    def cookie_string(self):
        return '{}={}'.format(self.random_cookie_key, self.random_cookie_value)

    @let
    def cookie_header(self):
        return {'Cookie': 'auth_token={}'.format(self.random_cookie_value)}

    @let
    def uri_path(self):
        return '/' + self.faker.uri_path()

    @let
    def random_cookie_key(self):
        return self.faker.name()

    @let
    def random_cookie_value(self):
        return self.faker.sha256()

    @let
    def faker(self):
        from faker import Faker
        return Faker()
        

    authorization_mock = let_patch_mock('foundations_rest_api.v1.models.session.Session.is_authorized')

    def test_returns_class(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.Mock)
        self.assertEqual(klass, APIResourceMocks.Mock)

    def test_get_returns_index(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.MockWithIndex)
        with self._test_client() as client:
            response = client.get(self.uri_path)
            self.assertEqual(self._json_response(response), 'some data')
    
    def test_post_returns_post(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.MockWithPost)
        with self._test_client() as client:
            response = client.post(self.uri_path)
            self.assertEqual(self._json_response(response), 'some data')
        
    
    def test_post_sets_params(self):
        def _callback(mock_instance):
            return mock_instance.params

        mock_klass = self._mock_resource('post', _callback)

        klass = api_resource(self.uri_path)(mock_klass)
        with self._test_client() as client:
            response = client.post(self.uri_path, data={'password': 'world'})
            self.assertEqual(self._json_response(response), {'password': 'world'})

    def test_post_sets_params_different_params(self):
        def _callback(mock_instance):
            return mock_instance.params

        mock_klass = self._mock_resource('post', _callback)

        klass = api_resource(self.uri_path)(mock_klass)
        with self._test_client() as client:
            response = client.post(self.uri_path, data={'password': 'world', 'cat': 'dog'})
            self.assertEqual(self._json_response(response), {'password': 'world', 'cat': 'dog'})

    def test_get_returns_index_different_data(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.DifferentMockWithIndex)
        with self._test_client() as client:
            response = client.get(self.uri_path)
            self.assertEqual(self._json_response(response), 'some different data')
    
    def test_get_and_post_returns_index_and_post(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.MockWithIndexAndPost)
        with self._test_client() as client:
            post_response = client.post(self.uri_path)
            get_response = client.get(self.uri_path)
            self.assertEqual(self._json_response(post_response), 'some post data')
            self.assertEqual(self._json_response(get_response), 'some index data')

    def test_get_returns_empty_params(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.ParamsMockWithIndex)
        with self._test_client() as client:
            response = client.get(self.uri_path)
            self.assertEqual(self._json_response(response), {})

    def test_get_has_status_code(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.ParamsMockWithIndex)
        with self._test_client() as client:
            response = client.get(self.uri_path)
            self.assertEqual(response.status_code, 200)

    def test_get_has_status_code_different_code(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.ParamsMockWithIndexAndStatus)
        with self._test_client() as client:
            response = client.get(self.uri_path)
            self.assertEqual(response.status_code, 403)

    def test_post_has_status_code(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.MockWithIndexAndPost)
        with self._test_client() as client:
            response = client.post(self.uri_path)
            self.assertEqual(response.status_code, 200)

    def test_post_has_status_code_different_code(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.ParamsMockWithPostAndStatus)
        with self._test_client() as client:
            response = client.post(self.uri_path)
            self.assertEqual(response.status_code, 403)

    def test_post_has_cookie(self):
        def _callback(mock_instance):
            return mock_instance.params

        mock_klass = self._mock_resource('post', _callback, cookie=self.random_cookie, )
        klass = api_resource(self.uri_path)(mock_klass)
        with self._test_client() as client:
            response = client.post(self.uri_path, data={'password': 'world'})
            self.assertEqual(self.cookie_string, response.headers.get('Set-Cookie'))

    def test_get_returns_path_param(self):
        klass = api_resource('/path/to/resource/with/<string:project_name>/params')(APIResourceMocks.ParamsMockWithIndex)
        with self._test_client() as client:
            response = client.get('/path/to/resource/with/value/params')
            self.assertEqual(self._json_response(response), {'project_name': 'value'})

    def test_get_returns_path_with_query_params(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.ParamsMockWithIndex)
        with self._test_client() as client:
            response = client.get(self.uri_path + '?hello=world')
            self.assertEqual(self._json_response(response), {'hello': 'world'})

    def test_get_returns_path_with_query_list_params(self):
        klass = api_resource('/path/to/resource/with/query_list/params')(APIResourceMocks.ParamsMockWithIndex)
        with self._test_client() as client:
            response = client.get('/path/to/resource/with/query_list/params?hello=world&hello=lou')
            self.assertEqual(self._json_response(response), {'hello': ['world', 'lou']})

    def test_get_returns_unauthorized_when_not_authenticated(self):
        mock_klass = self._mock_resource('index', self._empty_callback)
        klass = api_resource(self.uri_path)(mock_klass)

        self.authorization_mock.return_value = False
        headers = {'Cookie': 'auth_token={}'.format(self.random_cookie_value)}
        with self._test_client() as client:
            response = client.get(self.uri_path, headers=self.cookie_header)
            self.assertEqual(self._json_response(response), 'Unauthorized')
    
    def test_get_calls_session_is_authorized_with_correct_parameters(self):
        mock_klass = self._mock_resource('index', self._empty_callback)
        klass = api_resource(self.uri_path)(mock_klass)

        with self._test_client() as client:
            response = client.get(self.uri_path, headers=self.cookie_header)
            self.authorization_mock.assert_called_with({'auth_token': self.random_cookie_value})

    def _empty_callback(self, mock_instance):
        return ''

    def _test_client(self):
        from foundations_rest_api.global_state import app_manager
        return app_manager.app().test_client()

    def _mock_resource(self, method, callback, status=200, cookie=None):
        from foundations_rest_api.lazy_result import LazyResult

        mock_klass = Mock()
        mock_instance = Mock()
        mock_klass.return_value = mock_instance
        result = LazyResult(lambda: callback(mock_instance))
        getattr(mock_instance, method).side_effect = lambda: Response('Mock', result, status=status, cookie=cookie)
        return mock_klass

    def _json_response(self, response):
        from foundations.utils import string_from_bytes
        from json import loads, dumps

        data = string_from_bytes(response.data)

        return loads(data)