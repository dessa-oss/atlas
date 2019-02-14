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
from foundations_internal.testing.helpers import let

class TestAPIResource(Spec):

    @let
    def random_cookie(self):
        from faker import Faker
        return Faker().sha256()

    def test_returns_class(self):
        klass = api_resource('/path/to/resource')(APIResourceMocks.Mock)
        self.assertEqual(klass, APIResourceMocks.Mock)

    def test_get_returns_index(self):
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/resource')(APIResourceMocks.MockWithIndex)
        with app_manager.app().test_client() as client:
            response = client.get('/path/to/resource')
            self.assertEqual(self._json_response(response), 'some data')
    
    def test_post_returns_post(self):
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/resource')(APIResourceMocks.MockWithPost)
        with app_manager.app().test_client() as client:
            response = client.post('/path/to/resource')
            self.assertEqual(self._json_response(response), 'some data')
        
    
    def test_post_sets_params(self):
        from foundations_rest_api.global_state import app_manager

        def _callback(mock_instance):
            return mock_instance.params

        mock_klass = self._mock_resource('post', _callback)

        klass = api_resource('/path/to/resource/with/query/params')(mock_klass)
        with app_manager.app().test_client() as client:
            response = client.post('/path/to/resource/with/query/params', data={'password': 'world'})
            self.assertEqual(self._json_response(response), {'password': 'world'})

    def test_post_sets_params_different_params(self):
        from foundations_rest_api.global_state import app_manager

        def _callback(mock_instance):
            return mock_instance.params

        mock_klass = self._mock_resource('post', _callback)

        klass = api_resource('/path/to/different/resource/with/query/params')(mock_klass)
        with app_manager.app().test_client() as client:
            response = client.post('/path/to/different/resource/with/query/params', data={'password': 'world', 'cat': 'dog'})
            self.assertEqual(self._json_response(response), {'password': 'world', 'cat': 'dog'})

    def test_get_returns_index_different_data(self):
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/different/resource')(APIResourceMocks.DifferentMockWithIndex)
        with app_manager.app().test_client() as client:
            response = client.get('/path/to/different/resource')
            self.assertEqual(self._json_response(response), 'some different data')
    
    def test_get_and_post_returns_index_and_post(self):
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/another/resource')(APIResourceMocks.MockWithIndexAndPost)
        with app_manager.app().test_client() as client:
            post_response = client.post('/path/to/another/resource')
            get_response = client.get('/path/to/another/resource')
            self.assertEqual(self._json_response(post_response), 'some post data')
            self.assertEqual(self._json_response(get_response), 'some index data')

    def test_get_returns_empty_params(self):
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/resource/with/params')(APIResourceMocks.ParamsMockWithIndex)
        with app_manager.app().test_client() as client:
            response = client.get('/path/to/resource/with/params')
            self.assertEqual(self._json_response(response), {})

    def test_get_has_status_code(self):
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/resource/with/params')(APIResourceMocks.ParamsMockWithIndex)
        with app_manager.app().test_client() as client:
            response = client.get('/path/to/resource/with/params')
            self.assertEqual(response.status_code, 200)

    def test_get_has_status_code_different_code(self):
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/resource/with/params/and/status/code')(APIResourceMocks.ParamsMockWithIndexAndStatus)
        with app_manager.app().test_client() as client:
            response = client.get('/path/to/resource/with/params/and/status/code')
            self.assertEqual(response.status_code, 403)

    def test_post_has_status_code(self):
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/another/resource')(APIResourceMocks.MockWithIndexAndPost)
        with app_manager.app().test_client() as client:
            response = client.post('/path/to/another/resource')
            self.assertEqual(response.status_code, 200)

    def test_post_has_status_code_different_code(self):
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/posty/path/to/resource/with/params/and/status/code')(APIResourceMocks.ParamsMockWithPostAndStatus)
        with app_manager.app().test_client() as client:
            response = client.post('/posty/path/to/resource/with/params/and/status/code')
            self.assertEqual(response.status_code, 403)

    def test_post_has_cookie(self):
        from foundations_rest_api.global_state import app_manager

        def _callback(mock_instance):
            return mock_instance.params

        mock_klass = self._mock_resource('post', _callback, cookie=self.random_cookie, )
        klass = api_resource('/path/to/post/resource/with/a/cookie/yum')(mock_klass)
        with app_manager.app().test_client() as client:
            response = client.post('/path/to/post/resource/with/a/cookie/yum', data={'password': 'world'})
            self.assertEqual(self.random_cookie, response.headers.get('Set-Cookie'))

    def test_get_returns_path_param(self):
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/resource/with/<string:project_name>/params')(APIResourceMocks.ParamsMockWithIndex)
        with app_manager.app().test_client() as client:
            response = client.get('/path/to/resource/with/value/params')
            self.assertEqual(self._json_response(response), {'project_name': 'value'})

    def test_get_returns_path_with_query_params(self):
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/resource/with/query/params')(APIResourceMocks.ParamsMockWithIndex)
        with app_manager.app().test_client() as client:
            response = client.get('/path/to/resource/with/query/params?hello=world')
            self.assertEqual(self._json_response(response), {'hello': 'world'})

    def test_get_returns_path_with_query_list_params(self):
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/resource/with/query_list/params')(APIResourceMocks.ParamsMockWithIndex)
        with app_manager.app().test_client() as client:
            response = client.get('/path/to/resource/with/query_list/params?hello=world&hello=lou')
            self.assertEqual(self._json_response(response), {'hello': ['world', 'lou']})

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