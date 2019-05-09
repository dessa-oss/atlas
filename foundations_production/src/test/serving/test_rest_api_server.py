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
from flask import Flask

class TestRestAPIServer(Spec):

    def test_add_new_model_package_in_manage_model_package_route(self):
        from foundations_production.serving.rest_api_server import RestAPIServer

        package_pool_class_mock = self.patch('foundations_production.serving.package_pool.PackagePool')
        package_pool_mock = Mock()
        package_pool_class_mock.return_value = package_pool_mock

        request_mock = self.patch('flask.request')
        request_mock.get_json.return_value = {'model_id': 'some_model_id'}

        rest_api_server = RestAPIServer()
        manage_model_package_function = rest_api_server.app.view_functions.get('manage_model_package')
        manage_model_package_function('some_model')

        package_pool_mock.add_package.assert_called_with('some_model_id')