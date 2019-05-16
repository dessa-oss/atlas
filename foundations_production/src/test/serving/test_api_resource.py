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

    def test_get_returns_get(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.MockWithIndex)
        with self._test_client() as client:
            get_response = client.get(self.uri_path)
            head_response = client.head(self.uri_path)
            self.assertEqual(get_response.json, 'some data')
            self.assertEqual(get_response.headers, head_response.headers)
            self.assertEqual(get_response.status_code, head_response.status_code)

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

    def test_get_returns_get_different_data(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.DifferentMockWithIndex)
        with self._test_client() as client:
            get_response = client.get(self.uri_path)
            head_response = client.head(self.uri_path)
            self.assertEqual(get_response.json, 'some different data')
            self.assertEqual(get_response.headers, head_response.headers)
            self.assertEqual(get_response.status_code, head_response.status_code)

    def test_get_and_post_returns_get_and_post(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.MockWithIndexAndPost)
        with self._test_client() as client:
            post_response = client.post(self.uri_path, json={})
            get_response = client.get(self.uri_path)
            head_response = client.head(self.uri_path)
            self.assertEqual(post_response.json, 'some post data')
            self.assertEqual(get_response.json, 'some index data')
            self.assertEqual(get_response.headers, head_response.headers)
            self.assertEqual(get_response.status_code, head_response.status_code)

    def test_get_returns_empty_params(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.ParamsMockWithIndex)
        with self._test_client() as client:
            get_response = client.get(self.uri_path)
            head_response = client.head(self.uri_path)
            self.assertEqual(get_response.json, {})
            self.assertEqual(get_response.headers, head_response.headers)
            self.assertEqual(get_response.status_code, head_response.status_code)

    def test_get_has_status_code(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.ParamsMockWithIndex)
        with self._test_client() as client:
            get_response = client.get(self.uri_path)
            head_response = client.head(self.uri_path)
            self.assertEqual(get_response.status_code, 200)
            self.assertEqual(head_response.status_code, 200)

    def test_get_has_status_code_different_code(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.ParamsMockWithIndexAndStatus)
        with self._test_client() as client:
            get_response = client.get(self.uri_path)
            head_response = client.head(self.uri_path)
            self.assertEqual(get_response.status_code, 403)
            self.assertEqual(head_response.status_code, 403)

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
            get_response = client.get('/path/to/resource/with/value/params')
            head_response = client.head('/path/to/resource/with/value/params')
            self.assertEqual(get_response.json, {'project_name': 'value'})
            self.assertEqual(get_response.headers, head_response.headers)
            self.assertEqual(get_response.status_code, head_response.status_code)

    def test_get_returns_path_with_query_params(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.ParamsMockWithIndex)
        with self._test_client() as client:
            get_response = client.get(self.uri_path + '?hello=world')
            head_response = client.head(self.uri_path + '?hello=world')
            self.assertEqual(get_response.json, {'hello': 'world'})
            self.assertEqual(get_response.headers, head_response.headers)
            self.assertEqual(get_response.status_code, head_response.status_code)

    def test_get_returns_path_with_query_list_params(self):
        klass = api_resource('/path/to/resource/with/query_list/params')(APIResourceMocks.ParamsMockWithIndex)
        with self._test_client() as client:
            get_response = client.get('/path/to/resource/with/query_list/params?hello=world&hello=lou')
            head_response = client.head('/path/to/resource/with/query_list/params?hello=world&hello=lou')
            self.assertEqual(get_response.json, {'hello': ['world', 'lou']})
            self.assertEqual(get_response.headers, head_response.headers)
            self.assertEqual(get_response.status_code, head_response.status_code)

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

    def test_post_returns_path_param(self):
        def _callback(mock_instance):
            return mock_instance.params

        mock_klass = self._mock_resource('post', _callback)

        klass = api_resource('/path/to/resource/with/<string:project_name>/params/that/uses/post/')(mock_klass)
        with self._test_client() as client:
            response = client.post('/path/to/resource/with/value/params/that/uses/post/', json={'another': 'value'})
            self.assertEqual(response.json, {'project_name': 'value', 'another': 'value'})

    def test_put_returns_path_param(self):
        def _callback(mock_instance):
            return mock_instance.params

        mock_klass = self._mock_resource('put', _callback)

        klass = api_resource('/path/to/resource/with/<string:project_name>/params/that/uses/put/')(mock_klass)
        with self._test_client() as client:
            response = client.put('/path/to/resource/with/value/params/that/uses/put/', json={'another': 'value'})
            self.assertEqual(response.json, {'project_name': 'value', 'another': 'value'})

    def test_missing_put_returns_405(self):
        klass = api_resource(self.uri_path)(APIResourceMocks.MockWithIndexAndPost)
        with self._test_client() as client:
            response = client.put(self.uri_path, json={})
            self.assertEqual(response.status_code, 405)

    def _empty_callback(self, mock_instance):
        return ''

    def _test_client(self):
        from foundations_production.serving.rest_api_server import RestAPIServer
        from foundations_production.serving.rest_api_server_provider import register_rest_api_server, get_rest_api_server

        RestAPIServer()
        rest_api_server = get_rest_api_server()
        return rest_api_server.flask.test_client()

    @staticmethod
    def _mock_resource(method, callback, status=200):
        from foundations_rest_api.lazy_result import LazyResult

        mock_klass = Mock()
        mock_instance = Mock()
        mock_klass.return_value = mock_instance
        result = LazyResult(lambda: callback(mock_instance))
        method_mock = getattr(mock_instance, method)
        method_mock.return_value = Response('Mock', result, status=status)
        return mock_klass
