"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

from mock import patch, Mock

from foundations_spec import *
from foundations_production.serving.rest_api_server import RestAPIServer


class TestRetrainModelPackageController(Spec):

    load_model_package_mock = let_patch_mock('foundations_production.load_model_package')
    model_package_mock = let_mock()
    mock_job = let_mock()
    mock_job_deployment = let_mock()
    model_mock = let_mock()

    mock_os_chdir = let_patch_mock('os.chdir')
    mock_prepare_job_workspace = let_patch_mock('foundations_production.serving.prepare_job_workspace')

    @let
    def retraining_job_id(self):
        return self.faker.uuid4()

    @let
    def retrain_model_package_id(self):
        return self.faker.uuid4()

    @let
    def user_defined_model_name(self):
        return self.faker.word()

    def _run(self):
        self._retraining_job_run = True
        return self.mock_job_deployment

    @set_up
    def set_up(self):
        from foundations_production.serving.rest_api_server_provider import get_rest_api_server

        self.mock_job_deployment.job_name.return_value = self.retraining_job_id
        self.mock_job.run.side_effect = self._run

        self.model_mock.retrain.return_value = self.mock_job
        self.model_package_mock.model = self.model_mock
        self.load_model_package_mock.return_value = self.model_package_mock


        self.rest_api_server = get_rest_api_server()
        self.flask = self.rest_api_server.flask
        self.api = self.rest_api_server.api()
        self.client = self.flask.test_client()

    def test_retrain_model_package_route_is_added(self):
        self.assertIn('/v1/<user_defined_model_name>/model/', [rule.rule for rule in self.flask.url_map.iter_rules()])

    def test_rest_api_endpoint_for_deploying_models_accepts_only_json(self):
        response = self.client.put("/v1/{}/model/".format(self.user_defined_model_name), data='bad data')
        self.assertEqual(400, response.status_code)
        self.assertEqual('Invalid content type', response.json['message'])

    def test_retrain_get_request_returns_404_if_model_package_does_not_exist(self):
        response = self.client.get('/v1/{}/model/'.format(self.user_defined_model_name))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'Model package not found: {}'.format(self.user_defined_model_name))

    def test_retrain_get_request_returns_200_if_model_package_exists(self):
        self._set_model_mapping()
        response = self.client.get('/v1/{}/model/'.format(self.user_defined_model_name), json={'model_id': self.retrain_model_package_id})
        self.assertEqual(response.status_code, 200)

    def test_retrain_head_request_returns_200_if_model_package_exists(self):
        self._set_model_mapping()
        response = self.client.head('/v1/{}/model/'.format(self.user_defined_model_name), json={'model_id': self.retrain_model_package_id})
        self.assertEqual(response.status_code, 200)

    def test_retrain_model_package_fails_with_bad_request_if_missing_target_file(self):
        self._set_model_mapping()
        payload = {
            'features_file': 'local:///path/to/features/file.pkl'
        }
        response = self.client.put("/v1/{}/model/".format(self.user_defined_model_name), json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual("Missing field in JSON data: targets_file", response.json["message"])

    def test_retrain_model_package_fails_with_bad_request_if_missing_features_file(self):
        self._set_model_mapping()
        payload = {
            'targets_file': 's3://path/to/targets/file.pkl',
        }
        response = self.client.put("/v1/{}/model/".format(self.user_defined_model_name), json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual("Missing field in JSON data: features_file", response.json["message"])

    def test_retraining_creates_job_succesfully_and_returns_correct_model_id(self):
        self._deploy_model_package()

        payload = {
            'model_id': self.retrain_model_package_id,
            'targets_file': 's3://path/to/targets/file.pkl',
            'features_file': 'local:///path/to/features/file.pkl'
        }

        response = self.client.put("/v1/{}/model/".format(self.user_defined_model_name), json=payload)

        self.assertEqual(202, response.status_code)
        self.assertEqual({'created_job_uuid': self.retraining_job_id}, response.json)

    def test_retraining_returns_404_when_model_package_not_deployed(self):
        from foundations_production.exceptions import MissingModelPackageException

        self._set_model_mapping()
        self.load_model_package_mock.side_effect = MissingModelPackageException(self.retrain_model_package_id)

        payload = {
            'model_id': self.retrain_model_package_id,
            'user_defined_model_name': self.user_defined_model_name,
            'targets_file': 's3://path/to/targets/file.pkl',
            'features_file': 'local:///path/to/features/file.pkl'
        }

        response = self.client.put("/v1/{}/model/".format(self.user_defined_model_name), json=payload)
        self.assertEqual(404, response.status_code)
        self.assertEqual('Model package not found: {}'.format(self.retrain_model_package_id), response.json['message'])

    def test_retrain_model_package_chdir_back_to_original_cwd_after_job_deployed(self):
        self._deploy_model_package()

        payload = {
            'model_id': self.retrain_model_package_id,
            'user_defined_model_name': self.user_defined_model_name,
            'targets_file': 's3://path/to/targets/file.pkl',
            'features_file': 'local:///path/to/features/file.pkl'
        }

        response = self.client.put("/v1/{}/model/".format(self.user_defined_model_name), json=payload)
        self.assertEqual(202, response.status_code)
        self.assertEqual(2, self.mock_os_chdir.call_count)

    def test_retrain_model_package_prepares_job_workspace(self):
        self._deploy_model_package()

        payload = {
            'model_id': self.retrain_model_package_id,
            'user_defined_model_name': self.user_defined_model_name,
            'targets_file': 's3://path/to/targets/file.pkl',
            'features_file': 'local:///path/to/features/file.pkl'
        }

        response = self.client.put("/v1/{}/model/".format(self.user_defined_model_name), json=payload)
        self.assertEqual(202, response.status_code)
        self.mock_prepare_job_workspace.assert_called_with(self.retrain_model_package_id)

    def _set_model_mapping(self):
        from foundations_production.serving.rest_api_server_provider import get_rest_api_server

        rest_api_server = get_rest_api_server()
        model_package_mapping = rest_api_server.get_model_package_mapping()
        model_package_mapping[self.user_defined_model_name] = self.retrain_model_package_id

    def _deploy_model_package(self):
        from foundations_production.serving.controllers.model_package_controller import ModelPackageController

        model_package_controller = ModelPackageController()
        model_package_controller.params = {
            'model_id': self.retrain_model_package_id,
            'user_defined_model_name': self.user_defined_model_name
        }
        response = model_package_controller.post()
        self.assertEqual(201, response.status())
