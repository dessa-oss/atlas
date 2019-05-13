"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

import unittest
from mock import Mock

from foundations_spec.helpers import let, let_now, let_patch_mock, set_up
from foundations_spec.helpers.spec import Spec

class TestRestAPIServer(Spec):

    @set_up
    def set_up(self):
        from foundations_production.serving.rest_api_server import RestAPIServer

        package_pool_class_mock = self.patch('foundations_production.serving.package_pool.PackagePool')
        self.package_pool_mock = Mock()
        package_pool_class_mock.return_value = self.package_pool_mock
        self.request_mock = self.patch('flask.request')

        self.rest_api_server = RestAPIServer()
        self.manage_model_package_function = self.rest_api_server.flask.view_functions.get('manage_model_package')

    def test_add_new_model_package_in_manage_model_package_route(self):
        self._deploy_model_package({'model_id': 'some_model_id'}, 'some_model')
        self.package_pool_mock.add_package.assert_called_with('some_model_id')

    def test_add_new_model_package_fails_with_bad_request_if_no_model_id_is_passed(self):
        from werkzeug.exceptions import BadRequest

        with self.assertRaises(BadRequest) as exception_context:
            self._deploy_model_package({'other_id': 'some_model_id'}, 'some_model')
        self.assertEqual(exception_context.exception.code, 400)
        self.assertEqual('400 Bad Request: Missing field in JSON data: model_id', str(exception_context.exception))

    def test_add_new_model_package_returns_meaningful_response_if_successful(self):
        response = self._deploy_model_package({'model_id': 'some_model_id'}, 'some_model')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['deployed_model_id'], 'some_model_id')

    def _deploy_model_package(self, payload, user_defined_model_name):
        self.request_mock.method = 'POST'
        self.request_mock.get_json.return_value = payload
        with self.rest_api_server.flask.app_context():
            return self.manage_model_package_function(user_defined_model_name)