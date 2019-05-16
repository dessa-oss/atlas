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

    package_pool_class_mock = let_patch_mock('foundations_production.serving.package_pool.PackagePool')
    package_pool_mock = Mock()
    mock_job = let_mock()
    mock_job_deployment = let_mock()
    communicator = let_mock()

    mock_os_chdir = let_patch_mock('os.chdir')
    mock_os_getcwd = let_patch_mock('os.getcwd')
    mock_prepare_job_workspace = let_patch_mock('foundations_production.serving.prepare_job_workspace')

    @let
    def retraining_job_id(self):
        return self.faker.uuid4()

    @let
    def model_package_id(self):
        return self.faker.uuid4()

    @let
    def user_defined_model_name(self):
        return self.faker.word()

    @let
    def initial_working_directory(self):
        return self.faker.file_path()

    @let
    def workspace_path(self):
        from foundations_production.serving import workspace_path
        return workspace_path(self.model_package_id)

    def _create_retraining_job(self, *args, **kwargs):
        expected_args = (self.model_package_id,)
        expected_kwargs = {
            'features_location': 'local:///path/to/features/file.pkl',
            'targets_location':'s3://path/to/targets/file.pkl'
        }

        if (args, kwargs) != (expected_args, kwargs):
            raise AssertionError('create_retraining_job not called with ' + str(expected_args) + ' ' + str(expected_kwargs))

        if self._working_directory != self.workspace_path:
            raise AssertionError('create_retraining_job called when not in workspace path')

        return self.mock_job

    def _run(self):
        self._retraining_job_run = True
        return self.mock_job_deployment

    def _chdir(self, path):
        if self._working_directory == self.initial_working_directory:
            if not self._workspace_prepared:
                raise AssertionError('pls do not chdir before prepping workspace dir')

            self._working_directory = path
            return

        if path != self.initial_working_directory or not self._retraining_job_run:
            raise AssertionError('need to change back to previous cwd after running retrain job')

    def _prepare_job_workspace(self, job_id):
        self._workspace_prepared = True

    @set_up
    def set_up(self):
        from foundations_production.serving.rest_api_server import RestAPIServer

        self._workspace_prepared = False
        self._working_directory = self.initial_working_directory
        self._retraining_job_run = False

        self.mock_os_chdir.side_effect = self._chdir
        self.mock_os_getcwd.side_effect = lambda: self._working_directory
        self.mock_prepare_job_workspace.side_effect = self._prepare_job_workspace

        self.mock_job_deployment.job_name.return_value = self.retraining_job_id
        self.mock_job.run.side_effect = self._run
        self.mock_create_retraining_job = self.patch('foundations_production.serving.create_retraining_job', self._create_retraining_job)

        self.package_pool_class_mock.return_value = self.package_pool_mock
        self.package_pool_mock.get_communicator = ConditionalReturn()
        self.package_pool_mock.get_communicator.return_when(self.communicator, self.model_package_id)
        self.request_mock = self.patch('flask.request')

        self.rest_api_server = RestAPIServer()
        self.manage_model_package_function = self.rest_api_server.flask.view_functions.get('manage_model_package')
        self.train_latest_model_package_function = self.rest_api_server.flask.view_functions.get('train_latest_model_package')
        self.predictions_from_model_package_function = self.rest_api_server.flask.view_functions.get('predictions_from_model_package')

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
    
    def test_predictions_from_model_package_returns_200_if_predictions_successful(self):
        self._deploy_model_package({'model_id': self.model_package_id}, self.user_defined_model_name)
        self.communicator.get_response.return_value = {}

        self.request_mock.method = 'PUT'
        self.request_mock.get_json.return_value = {
            'rows': [['value', 43234], ['spider', 323]], 
            'schema': [{'name': '1st column', 'type': 'string'}, {'name': '2nd column', 'type': 'int'}]
        }

        with self.rest_api_server.flask.app_context():
            response = self.predictions_from_model_package_function(self.user_defined_model_name)

        self.assertEqual(200, response.status_code)

    def test_predictions_from_model_package_returns_predicitions_in_body(self):
        import json
        
        self._deploy_model_package({'model_id': self.model_package_id}, self.user_defined_model_name)

        expected_prediction_json = {
            'rows': [['value transformed predicted', 43667], ['spider transformed predicted', 756]], 
            'schema': [{'name': '1st column', 'type': 'object'}, {'name': '2nd column', 'type': 'int64'}]
        }
        self.communicator.get_response.return_value = expected_prediction_json

        self.request_mock.method = 'PUT'
        self.request_mock.get_json.return_value = {
            'rows': [['value', 43234], ['spider', 323]], 
            'schema': [{'name': '1st column', 'type': 'string'}, {'name': '2nd column', 'type': 'int'}]
        }

        with self.rest_api_server.flask.app_context():
            response = self.predictions_from_model_package_function(self.user_defined_model_name)

        self.assertEqual(expected_prediction_json, json.loads(response.get_data()))
    

    def test_predictions_from_model_package_sets_action_request_for_prediction(self):
        self._deploy_model_package({'model_id': self.model_package_id}, self.user_defined_model_name)

        prediction_input_json = {
            'rows': [['value', 43234], ['spider', 323]], 
            'schema': [{'name': '1st column', 'type': 'string'}, {'name': '2nd column', 'type': 'int'}]
        }

        self.request_mock.get_json.return_value = prediction_input_json
        self.communicator.get_response.return_value = {}

        self.request_mock.method = 'PUT'

        with self.rest_api_server.flask.app_context():
            response = self.predictions_from_model_package_function(self.user_defined_model_name)

        self.communicator.set_action_request.assert_called_with(prediction_input_json)

    def test_predictions_from_model_package_returns_500_when_prediction_returns_error(self):
        import json
        from werkzeug.exceptions import InternalServerError

        self._deploy_model_package({'model_id': self.model_package_id}, self.user_defined_model_name)

        expected_prediction_json = {
            'name': 'Exception',
            'value': 'Something went wrong :('
        }
        self.communicator.get_response.return_value = expected_prediction_json

        self.request_mock.method = 'PUT'
        self.request_mock.get_json.return_value = {}

        with self.assertRaises(InternalServerError) as error_context: 
            with self.rest_api_server.flask.app_context():
                response = self.predictions_from_model_package_function(self.user_defined_model_name)

    def test_train_latest_model_package_chdir_back_to_original_cwd_after_job_deployed(self):
        self._deploy_model_package({'model_id': self.model_package_id}, self.user_defined_model_name)

        self.request_mock.method = 'PUT'
        self.request_mock.get_json.return_value = {
            'targets_file': 's3://path/to/targets/file.pkl',
            'features_file': 'local:///path/to/features/file.pkl'
        }

        with self.rest_api_server.flask.app_context():
            response = self.train_latest_model_package_function(self.user_defined_model_name)

        self.assertEqual(2, self.mock_os_chdir.call_count)

    def test_train_latest_model_package_prepares_job_workspace(self):
        self._deploy_model_package({'model_id': self.model_package_id}, self.user_defined_model_name)

        self.request_mock.method = 'PUT'
        self.request_mock.get_json.return_value = {
            'targets_file': 's3://path/to/targets/file.pkl',
            'features_file': 'local:///path/to/features/file.pkl'
        }

        with self.rest_api_server.flask.app_context():
            response = self.train_latest_model_package_function(self.user_defined_model_name)

        self.mock_prepare_job_workspace.assert_called_with(self.model_package_id)

    def _deploy_model_package(self, payload, user_defined_model_name):
        self.request_mock.method = 'POST'
        self.request_mock.get_json.return_value = payload
        with self.rest_api_server.flask.app_context():
            return self.manage_model_package_function(user_defined_model_name)