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
    package_pool_mock = let_patch_mock('foundations_production.serving.package_pool.PackagePool')
    
    @set_up
    def set_up(self):
        from foundations_production.serving.rest_api_server import RestAPIServer

        self.rest_api_server = RestAPIServer()
        self.flask = self.rest_api_server.flask
        self.client = self.flask.test_client()
    
    @let_now
    def mock_json_request_kwargs(self):

        return {'json': dict(foo='bar')}

    def test_manage_model_package_route_is_added(self):
        self.assertIn('manage_model_package', self.flask.view_functions)

    def test_training_all_model_packages_route_is_added(self):
        self.assertIn('train_all_model_packages', self.flask.view_functions)

    def test_training_one_model_package_route_is_added(self):
        self.assertIn('train_one_model_package', self.flask.view_functions)

    def test_predictions_from_model_package_route_is_added(self):
        self.assertIn('predictions_from_model_package', self.flask.view_functions)

    def test_predict_with_model_package_route_is_added(self):
        self.assertIn('predict_with_model_package', self.flask.view_functions)

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
        response = self.client.get('/v1/some_model/predictions')
        self.assertNotIn(response.status_code, [405, 500])

    def test_predictions_from_model_package_route_has_post_method(self):
        response = self.client.post('/v1/some_model/predictions', **self.mock_json_request_kwargs)
        self.assertNotIn(response.status_code, [405, 500])

    def test_predictions_from_model_package_route_has_no_put_method(self):
        response = self.client.put('/v1/some_model/predictions', **self.mock_json_request_kwargs)
        self.assertEqual(response.status_code, 405)

    def test_predictions_from_model_package_route_has_no_delete_method(self):
        response = self.client.delete('/v1/some_model/predictions', **self.mock_json_request_kwargs)
        self.assertEqual(response.status_code, 405)

    def test_predict_with_model_package_route_has_get_method(self):
        response = self.client.get('/v1/some_model/predictions/some_id')
        self.assertNotIn(response.status_code, [405, 500])

    def test_predict_with_model_package_route_has_head_method(self):
        response = self.client.head('/v1/some_model/predictions/some_id')
        self.assertNotIn(response.status_code, [405, 500])

    def test_predict_with_model_package_route_has_no_post_method(self):
        response = self.client.post('/v1/some_model/predictions/some_id', **self.mock_json_request_kwargs)
        self.assertEqual(response.status_code, 405)

    def test_predict_with_model_package_route_has_no_put_method(self):
        response = self.client.put('/v1/some_model/predictions/some_id', **self.mock_json_request_kwargs)
        self.assertEqual(response.status_code, 405)

    def test_predict_with_model_package_route_has_no_delete_method(self):
        response = self.client.delete('/v1/some_model/predictions/some_id', **self.mock_json_request_kwargs)
        self.assertEqual(response.status_code, 405)

    def test_rest_api_accepts_only_json(self):
        response = self.client.post('/v1/some_model/', data='bad data')
        self.assertEqual(response.status_code, 400)

    def test_deploy_new_model_package_happens_with_post_request(self):
        response = self.client.post('/v1/some_model/', json={'model_id': 'some_model_id'})
        self.assertEqual(response.json['deployed_model_id'], 'some_model_id')

    def test_deploy_new_model_package_doesnt_happen_with_get_request(self):
        response = self.client.get('/v1/some_model/', json={'model_id': 'some_model_id'})
        self.assertNotIn('deployed_model_id', response.data.decode())
