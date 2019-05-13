"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

import unittest
from mock import Mock

from foundations_spec import *

class TestRestAPIServer(Spec):

    mock_create_retraining_job = let_patch_mock('foundations_production.serving.create_retraining_job', ConditionalReturn())
    mock_job = let_mock()
    mock_job_deployment = let_mock()

    @let
    def retraining_job_id(self):
        return self.faker.uuid4()

    @let
    def model_package_id(self):
        return self.faker.uuid4()

    @let
    def user_defined_model_name(self):
        return self.faker.word()

    @set_up
    def set_up(self):
        from foundations_production.serving.rest_api_server import RestAPIServer

        self.mock_job_deployment.job_name.return_value = self.retraining_job_id
        self.mock_job.run.return_value = self.mock_job_deployment
        self.mock_create_retraining_job.return_when(
            self.mock_job,
            self.model_package_id,
            features_location='local:///path/to/features/file.pkl',
            targets_location='s3://path/to/targets/file.pkl'
        )

        package_pool_class_mock = self.patch('foundations_production.serving.package_pool.PackagePool')
        self.package_pool_mock = Mock()
        package_pool_class_mock.return_value = self.package_pool_mock
        self.request_mock = self.patch('flask.request')

        self.rest_api_server = RestAPIServer()
        self.manage_model_package_function = self.rest_api_server.flask.view_functions.get('manage_model_package')
        self.train_latest_model_package_function = self.rest_api_server.flask.view_functions.get('train_latest_model_package')

    def test_add_new_model_package_in_manage_model_package_route(self):
        self._deploy_model_package({'model_id': self.model_package_id}, self.user_defined_model_name)
        self.package_pool_mock.add_package.assert_called_with(self.model_package_id)

    def test_add_new_model_package_fails_with_bad_request_if_no_model_id_is_passed(self):
        from werkzeug.exceptions import BadRequest

        with self.assertRaises(BadRequest) as exception_context:
            self._deploy_model_package({'other_id': self.model_package_id}, self.user_defined_model_name)
        self.assertEqual(exception_context.exception.code, 400)
        self.assertEqual('400 Bad Request: Missing field in JSON data: model_id', str(exception_context.exception))

    def test_add_new_model_package_returns_meaningful_response_if_successful(self):
        response = self._deploy_model_package({'model_id': self.model_package_id}, self.user_defined_model_name)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['deployed_model_id'], self.model_package_id)

    def test_train_latest_model_package_returns_202_if_model_deployed(self):
        self._deploy_model_package({'model_id': self.model_package_id}, self.user_defined_model_name)

        self.request_mock.method = 'PUT'
        self.request_mock.get_json.return_value = {
            'targets_file': 's3://path/to/targets/file.pkl',
            'features_file': 'local:///path/to/features/file.pkl'
        }

        with self.rest_api_server.flask.app_context():
            response = self.train_latest_model_package_function(self.user_defined_model_name)

        self.assertEqual(202, response.status_code)

    def test_train_latest_model_package_returns_404_if_model_not_deployed(self):
        self._deploy_model_package({'model_id': self.model_package_id}, self.user_defined_model_name)

        self.request_mock.method = 'PUT'
        self.request_mock.get_json.return_value = {
            'targets_file': 's3://path/to/targets/file.pkl',
            'features_file': 'local:///path/to/features/file.pkl'
        }

        with self.rest_api_server.flask.app_context():
            response = self.train_latest_model_package_function('other_model')

        self.assertEqual(404, response.status_code)

    def test_get_latest_model_package_returns_200(self):
        self._deploy_model_package({'model_id': self.model_package_id}, self.user_defined_model_name)

        self.request_mock.method = 'GET'

        with self.rest_api_server.flask.app_context():
            response = self.train_latest_model_package_function(self.user_defined_model_name)

        self.assertEqual(200, response.status_code)

    def test_get_latest_model_package_returns_404(self):
        self._deploy_model_package({'model_id': self.model_package_id}, self.user_defined_model_name)

        self.request_mock.method = 'GET'

        with self.rest_api_server.flask.app_context():
            response = self.train_latest_model_package_function('other_model')

        self.assertEqual(404, response.status_code)

    def test_train_latest_model_package_creates_retraining_job_and_returns_new_job_id(self):
        self._deploy_model_package({'model_id': self.model_package_id}, self.user_defined_model_name)

        self.request_mock.method = 'PUT'
        self.request_mock.get_json.return_value = {
            'targets_file': 's3://path/to/targets/file.pkl',
            'features_file': 'local:///path/to/features/file.pkl'
        }

        with self.rest_api_server.flask.app_context():
            response = self.train_latest_model_package_function(self.user_defined_model_name)

        self.assertEqual({'created_job_uuid': self.retraining_job_id}, response.json)

    def test_head_latest_model_package_returns_200(self):
        self._deploy_model_package({'model_id': self.model_package_id}, self.user_defined_model_name)

        self.request_mock.method = 'HEAD'

        with self.rest_api_server.flask.app_context():
            response = self.train_latest_model_package_function(self.user_defined_model_name)

        self.assertEqual(200, response.status_code)

    def _deploy_model_package(self, payload, user_defined_model_name):
        self.request_mock.method = 'POST'
        self.request_mock.get_json.return_value = payload
        with self.rest_api_server.flask.app_context():
            return self.manage_model_package_function(user_defined_model_name)