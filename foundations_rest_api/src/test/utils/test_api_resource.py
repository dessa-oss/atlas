"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch
from foundations_rest_api.utils.api_resource import api_resource


class TestAPIResource(unittest.TestCase):
    class Mock(object):
        pass

    class MockWithIndex(object):
        def index(self):
            from foundations_rest_api.response import Response
            def _index():
                return 'some data'
            return Response('Mock', _index)

    class ParamsMockWithIndex(object):
        def index(self):
            from foundations_rest_api.response import Response
            def _index():
                return self.params
            return Response('Mock', _index)

    class DifferentMockWithIndex(object):
        def index(self):
            from foundations_rest_api.response import Response
            def _index():
                return 'some different data'
            return Response('Mock', _index)

    def test_returns_class(self):
        klass = api_resource('path/to/resource')(self.Mock)
        self.assertEqual(klass, self.Mock)

    def test_get_returns_index(self):
        from json import loads
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/resource')(self.MockWithIndex)
        with app_manager.app().test_client() as client:
            response = client.get('/path/to/resource')
            self.assertEqual(loads(response.data), 'some data')

    def test_get_returns_index_different_data(self):
        from json import loads
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/different/resource')(self.DifferentMockWithIndex)
        with app_manager.app().test_client() as client:
            response = client.get('/path/to/different/resource')
            self.assertEqual(loads(response.data), 'some different data')

    def test_get_returns_empty_params(self):
        from json import loads
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/resource/with/params')(self.ParamsMockWithIndex)
        with app_manager.app().test_client() as client:
            response = client.get('/path/to/resource/with/params')
            self.assertEqual(loads(response.data), {})

    def test_get_returns_path_param(self):
        from json import loads
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/resource/with/<string:project_name>/params')(self.ParamsMockWithIndex)
        with app_manager.app().test_client() as client:
            response = client.get('/path/to/resource/with/value/params')
            self.assertEqual(loads(response.data), {'project_name': 'value'})

    def test_get_returns_path_with_query_params(self):
        from json import loads
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/resource/with/query/params')(self.ParamsMockWithIndex)
        with app_manager.app().test_client() as client:
            response = client.get('/path/to/resource/with/query/params?hello=world')
            self.assertEqual(loads(response.data), {'hello': 'world'})

    def test_get_returns_path_with_query_list_params(self):
        from json import loads
        from foundations_rest_api.global_state import app_manager

        klass = api_resource('/path/to/resource/with/query_list/params')(self.ParamsMockWithIndex)
        with app_manager.app().test_client() as client:
            response = client.get('/path/to/resource/with/query_list/params?hello=world&hello=lou')
            self.assertEqual(loads(response.data), {'hello': ['world', 'lou']})