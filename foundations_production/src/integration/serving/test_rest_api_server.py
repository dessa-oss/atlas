"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

import unittest
from mock import Mock

from foundations_spec import *
from flask import Flask

class TestRestAPIServer(Spec):
    package_pool_mock = let_patch_mock('foundations_production.serving.package_pool.PackagePool')

    @set_up
    def set_up(self):
        from foundations_production.serving.rest_api_server import RestAPIServer
        from foundations_production.serving.rest_api_server_provider import get_rest_api_server

        RestAPIServer()
        self.rest_api_server = get_rest_api_server()
        self.flask = self.rest_api_server.flask
        self.client = self.flask.test_client()

    @let_now
    def mock_json_request_kwargs(self):

        return {'json': dict(foo='bar')}

    def test_manage_model_package_route_has_get_method(self):
        response = self.client.get('/v1/some_model/')
        self.assertNotIn(response.status_code, [405, 500])

    def test_manage_model_package_route_has_post_method(self):
        response = self.client.post('/v1/some_model/', **self.mock_json_request_kwargs)
        self.assertNotIn(response.status_code, [405, 500])

    def test_manage_model_package_route_has_head_method(self):
        response = self.client.head('/v1/some_model/')
        self.assertNotIn(response.status_code, [405, 500])

    def test_manage_model_package_route_has_delete_method(self):
        response = self.client.delete('/v1/some_model/', **self.mock_json_request_kwargs)
        self.assertNotIn(response.status_code, [405, 500])

    def test_manage_model_route_has_no_put_method(self):
        response = self.client.put('/v1/some_model/', **self.mock_json_request_kwargs)
        self.assertEqual(response.status_code, 405)

    def test_training_all_model_packages_route_has_get_method(self):
        response = self.client.get('/v1/some_model/model/')
        self.assertNotIn(response.status_code, [405, 500])

    def test_training_all_model_packages_route_has_put_method(self):
        response = self.client.put('/v1/some_model/model/', **self.mock_json_request_kwargs)
        self.assertNotIn(response.status_code, [405, 500])

    def test_training_all_model_packages_route_has_head_method(self):
        response = self.client.head('/v1/some_model/model/')
        self.assertNotIn(response.status_code, [405, 500])

    def test_training_all_model_packages_route_has_no_post_method(self):
        response = self.client.post('/v1/some_model/model/', **self.mock_json_request_kwargs)
        self.assertEqual(response.status_code, 405)

    def test_training_all_model_packages_route_has_no_delete_method(self):
        response = self.client.delete('/v1/some_model/model/', **self.mock_json_request_kwargs)
        self.assertEqual(response.status_code, 405)

    def test_training_one_model_package_route_has_get_method(self):
        response = self.client.get('/v1/some_model/model/some_version')
        self.assertNotIn(response.status_code, [405, 500])

    def test_training_one_model_package_route_has_put_method(self):
        response = self.client.put('/v1/some_model/model/some_version', **self.mock_json_request_kwargs)
        self.assertNotIn(response.status_code, [405, 500])

    def test_training_one_model_package_route_has_head_method(self):
        response = self.client.head('/v1/some_model/model/some_version')
        self.assertNotIn(response.status_code, [405, 500])

    def test_training_one_model_package_route_has_no_post_method(self):
        response = self.client.post('/v1/some_model/model/', **self.mock_json_request_kwargs)
        self.assertEqual(response.status_code, 405)

    def test_training_one_model_package_route_has_no_delete_method(self):
        response = self.client.delete('/v1/some_model/model/', **self.mock_json_request_kwargs)
        self.assertEqual(response.status_code, 405)

    def test_predictions_from_model_package_route_has_get_method(self):
        response = self.client.get('/v1/some_model/predictions/')
        self.assertNotIn(response.status_code, [405, 500])

    def test_predictions_from_model_package_route_has_post_method(self):
        response = self.client.post('/v1/some_model/predictions/', **self.mock_json_request_kwargs)
        self.assertNotIn(response.status_code, [405, 500])

    def test_predictions_from_model_package_route_has_no_put_method(self):
        response = self.client.put('/v1/some_model/predictions/', **self.mock_json_request_kwargs)
        self.assertEqual(response.status_code, 405)

    def test_predictions_from_model_package_route_has_no_delete_method(self):
        response = self.client.delete('/v1/some_model/predictions/', **self.mock_json_request_kwargs)
        self.assertEqual(response.status_code, 405)

    def test_predict_with_model_package_route_has_get_method(self):
        response = self.client.get('/v1/some_model/predictions/some_id/')
        self.assertNotIn(response.status_code, [405, 500])

    def test_predict_with_model_package_route_has_head_method(self):
        response = self.client.head('/v1/some_model/predictions/some_id/')
        self.assertNotIn(response.status_code, [405, 500])
