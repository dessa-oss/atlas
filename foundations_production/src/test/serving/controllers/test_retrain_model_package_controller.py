"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

from mock import patch, call

from foundations_spec import *
from foundations_production.serving.rest_api_server import RestAPIServer

class TestRetrainModelPackageController(Spec):

    mock_create_retraining_job = let_patch_mock('foundations_production.serving.create_retraining_job', ConditionalReturn())
    package_pool_class_mock = let_patch_mock('foundations_production.serving.package_pool.PackagePool')
    workspace_path_mock = let_patch_mock('foundations_production.serving.workspace_path')
    mock_prepare_job_workspace = let_patch_mock('foundations_production.serving.prepare_job_workspace')
    mock_os_chdir = let_patch_mock('os.chdir')

    package_pool_mock = let_mock()
    mock_job_deployment = let_mock()
    mock_job = let_mock()

    @let
    def retrain_model_package_id(self):
        return self.faker.uuid4()

    @let
    def user_defined_model_name(self):
        return self.faker.word()

    @let
    def retraining_job_id(self):
        return self.faker.uuid4()

    @set_up
    def set_up(self):
        from foundations_production.serving.controllers.retrain_model_package_controller import RetrainModelPackageController

        self.mock_job_deployment.job_name.return_value = self.retraining_job_id
        self.mock_job.run.return_value = self.mock_job_deployment
        self.mock_create_retraining_job.return_when(
            self.mock_job,
            self.retrain_model_package_id,
            features_location='local:///path/to/features/file.pkl',
            targets_location='s3://path/to/targets/file.pkl'
        )

        self.package_pool_class_mock.return_value = self.package_pool_mock
        self.retrain_model_package_controller = RetrainModelPackageController()
        RestAPIServer()

    def test_retraining_returns_404_when_model_package_not_deployed(self):
        from werkzeug.exceptions import NotFound
        self.retrain_model_package_controller.params = {
            'model_id': self.retrain_model_package_id,
            'user_defined_model_name': self.user_defined_model_name,
            'targets_file': 's3://path/to/targets/file.pkl',
            'features_file': 'local:///path/to/features/file.pkl'
        }
        with self.assertRaises(NotFound):
            response = self.retrain_model_package_controller.put()
            self.assertEqual(404, response.status())

    @patch.object(RestAPIServer, 'get_model_package_mapping')
    def test_retraining_returns_202_when_model_package_is_deployed(self, get_model_package_mapping_mock):
        get_model_package_mapping_mock.return_value = {self.user_defined_model_name: self.retrain_model_package_id}
        response = self._call_retrain_model_package()
        self.assertEqual(202, response.status())

    @patch.object(RestAPIServer, 'get_model_package_mapping')
    def test_retraining_calls_prepare_workspace(self, get_model_package_mapping_mock):
        get_model_package_mapping_mock.return_value = {self.user_defined_model_name: self.retrain_model_package_id}
        self._call_retrain_model_package().evaluate()
        self.mock_prepare_job_workspace.assert_called_with(self.retrain_model_package_id)


    @patch.object(RestAPIServer, 'get_model_package_mapping')
    def test_retraining_calls_workspace_path(self, get_model_package_mapping_mock):
        get_model_package_mapping_mock.return_value = {self.user_defined_model_name: self.retrain_model_package_id}
        self._call_retrain_model_package().evaluate()
        self.workspace_path_mock.assert_called_with(self.retrain_model_package_id)

    @patch.object(RestAPIServer, 'get_model_package_mapping')
    def test_retraining_calls_chdir(self, get_model_package_mapping_mock):
        import os
        self.workspace_path_mock.return_value = 'some/fake/workspace/path'
        get_model_package_mapping_mock.return_value = {self.user_defined_model_name: self.retrain_model_package_id}
        self._call_retrain_model_package().evaluate()
        chdir_calls = [
            call('some/fake/workspace/path'),
            call(os.getcwd())
        ]
        self.mock_os_chdir.has_calls(chdir_calls)

    @patch.object(RestAPIServer, 'get_model_package_mapping')
    def test_retraining_calls_create_retraining_job(self, get_model_package_mapping_mock):
        get_model_package_mapping_mock.return_value = {self.user_defined_model_name: self.retrain_model_package_id}
        self._call_retrain_model_package().evaluate()
        self.mock_create_retraining_job.assert_called_with(
            self.retrain_model_package_id,
            targets_location='s3://path/to/targets/file.pkl',
            features_location='local:///path/to/features/file.pkl')

    @patch.object(RestAPIServer, 'get_model_package_mapping')
    def test_retraining_calls_retraining_job_run_method(self, get_model_package_mapping_mock):
        get_model_package_mapping_mock.return_value = {self.user_defined_model_name: self.retrain_model_package_id}
        self._call_retrain_model_package().evaluate()
        self.mock_job.run.assert_called()

    @patch.object(RestAPIServer, 'get_model_package_mapping')
    def test_retraining_returns_model_package_id_when_model_package_is_deployed(self, get_model_package_mapping_mock):
        get_model_package_mapping_mock.return_value = {self.user_defined_model_name: self.retrain_model_package_id}
        response = self._call_retrain_model_package()
        self.assertEqual({'created_job_uuid': self.retraining_job_id}, response.as_json())

    def _call_retrain_model_package(self):
        self.retrain_model_package_controller.params = {
            'model_id': self.retrain_model_package_id,
            'user_defined_model_name': self.user_defined_model_name,
            'targets_file': 's3://path/to/targets/file.pkl',
            'features_file': 'local:///path/to/features/file.pkl'
        }
        return self.retrain_model_package_controller.put()
