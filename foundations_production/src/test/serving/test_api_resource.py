"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch, Mock
from foundations_production.serving.api_resource import api_resource
from test.serving.helpers.api_resource_mocks import APIResourceMocks
from foundations_rest_api.lazy_result import LazyResult
from foundations_rest_api.response import Response

from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers import let, let_patch_mock

class TestAPIResource(Spec):

    @let
    def uri_path(self):
        return '/' + self.faker.uri_path(10)

    def test_returns_class(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.Mock)
        self.assertEqual(klass, APIResourceMocks.Mock)

    def test_get_returns_index(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.MockWithIndex)
        with self._test_client() as client:
            response = client.get(self.uri_path)
            self.assertEqual(response.json, 'some data')
    
    def test_post_returns_post(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.MockWithPost)
        with self._test_client() as client:
            response = client.post(self.uri_path, json={})
            self.assertEqual(response.json, 'some data')

    def test_post_sets_params(self):
        def _callback(mock_instance):
            return mock_instance.params

        mock_klass = self._mock_resource('post', _callback)

        klass = api_resource(self.uri_path)(mock_klass)
        with self._test_client() as client:
            response = client.post(self.uri_path, json={'password': 'world'})
            self.assertEqual(response.json, {'password': 'world'})

    def test_post_sets_params_different_params(self):
        def _callback(mock_instance):
            return mock_instance.params

        mock_klass = self._mock_resource('post', _callback)

        klass = api_resource(self.uri_path)(mock_klass)
        with self._test_client() as client:
            response = client.post(self.uri_path, json={'password': 'world', 'cat': 'dog'})
            self.assertEqual(response.json, {'password': 'world', 'cat': 'dog'})

    def test_get_returns_index_different_data(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.DifferentMockWithIndex)
        with self._test_client() as client:
            response = client.get(self.uri_path)
            self.assertEqual(response.json, 'some different data')
    
    def test_get_and_post_returns_index_and_post(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.MockWithIndexAndPost)
        with self._test_client() as client:
            post_response = client.post(self.uri_path, json={})
            get_response = client.get(self.uri_path)
            self.assertEqual(post_response.json, 'some post data')
            self.assertEqual(get_response.json, 'some index data')

    def test_get_returns_empty_params(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.ParamsMockWithIndex)
        with self._test_client() as client:
            response = client.get(self.uri_path)
            self.assertEqual(response.json, {})

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
            response = client.post(self.uri_path, json={})
            self.assertEqual(response.status_code, 200)

    def test_post_has_status_code_different_code(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.ParamsMockWithPostAndStatus)
        with self._test_client() as client:
            response = client.post(self.uri_path, json={})
            self.assertEqual(response.status_code, 403)

    def test_get_returns_path_param(self):
        klass = api_resource('/path/to/resource/with/<string:project_name>/params')(APIResourceMocks.ParamsMockWithIndex)
        with self._test_client() as client:
            response = client.get('/path/to/resource/with/value/params')
            self.assertEqual(response.json, {'project_name': 'value'})

    def test_get_returns_path_with_query_params(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.ParamsMockWithIndex)
        with self._test_client() as client:
            response = client.get(self.uri_path + '?hello=world')
            self.assertEqual(response.json, {'hello': 'world'})

    def test_get_returns_path_with_query_list_params(self):
        klass = api_resource('/path/to/resource/with/query_list/params')(APIResourceMocks.ParamsMockWithIndex)
        with self._test_client() as client:
            response = client.get('/path/to/resource/with/query_list/params?hello=world&hello=lou')
            self.assertEqual(response.json, {'hello': ['world', 'lou']})

    def test_put_request_returns_return_value_of_resource_put_method(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.MockWithPut)
        with self._test_client() as client:
            response = client.put(self.uri_path, json={})
            self.assertEqual(response.json, 'some put data')

    def test_put_sets_params(self):
        def _callback(mock_instance):
            return mock_instance.params

        fake_put_data = self.faker.pydict(3, False, 'int', 'str', 'float')
        mock_klass = self._mock_resource('put', _callback)

        klass = api_resource(self.uri_path)(mock_klass)
        with self._test_client() as client:
            response = client.put(self.uri_path, json=fake_put_data)
            self.assertEqual(response.json, fake_put_data)

    def test_put_has_status_code(self):
        fake_status_code = self.faker.pyint()
        APIResourceMocks.ParamsMockWithPutAndStatus.status_code = fake_status_code
        klass = api_resource(self.uri_path)(APIResourceMocks.ParamsMockWithPutAndStatus)
        with self._test_client() as client:
            response = client.put(self.uri_path, json={})
            self.assertEqual(response.status_code, fake_status_code)

    def test_head_returns_path_param(self):
        klass = api_resource('/path/to/resource/with/<string:project_name>/params')(APIResourceMocks.ParamsMockWithIndex)
        with self._test_client() as client:
            print('>>>>>>>>>>>', client.head('/path/to/resource/with/value/params').json)
            response = client.head('/path/to/resource/with/value/params')
            self.assertEqual(response.json, {'project_name': 'value'})

    def test_head_returns_path_with_query_params(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.ParamsMockWithIndex)
        with self._test_client() as client:
            response = client.head(self.uri_path + '?hello=world')
            self.assertEqual(response.json, {'hello': 'world'})

    def test_head_returns_path_with_query_list_params(self):
        klass = api_resource('/path/to/resource/with/query_list/params')(APIResourceMocks.ParamsMockWithIndex)
        with self._test_client() as client:
            response = client.head('/path/to/resource/with/query_list/params?hello=world&hello=lou')
            self.assertEqual(response.json, {'hello': ['world', 'lou']})

    def _empty_callback(self, mock_instance):
        return ''

    def _test_client(self):
        from foundations_production.serving.rest_api_server import RestAPIServer 

        app_manager = RestAPIServer()
        return app_manager.flask.test_client()

    def _mock_resource(self, method, callback, status=200):
        from foundations_rest_api.lazy_result import LazyResult

        mock_klass = Mock()
        mock_instance = Mock()
        mock_klass.return_value = mock_instance
        result = LazyResult(lambda: callback(mock_instance))
        getattr(mock_instance, method).side_effect = lambda: Response('Mock', result, status=status)
        return mock_klass
