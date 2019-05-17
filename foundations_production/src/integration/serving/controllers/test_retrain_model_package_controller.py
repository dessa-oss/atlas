"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

# from mock import patch

from foundations_spec import *
from foundations_production.serving.rest_api_server import RestAPIServer
from foundations_production.serving.controllers.retrain_model_package_controller import RetrainModelPackageController

class TestRetrainModelPackageController(Spec):

    # mock_create_retraining_job = let_patch_mock('foundations_production.serving.create_retraining_job', ConditionalReturn())
    # package_pool_class_mock = let_patch_mock('foundations_production.serving.package_pool.PackagePool')
    # package_pool_mock = Mock()
    # mock_job_deployment = let_mock()
    # mock_job = let_mock()
    # communicator = let_mock()

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
        from foundations_production.serving.rest_api_server import RestAPIServer
        from foundations_production.serving.rest_api_server_provider import get_rest_api_server

        RestAPIServer()
        self.rest_api_server = get_rest_api_server()
        self.flask = self.rest_api_server.flask
        self.api = self.rest_api_server.api()
        self.client = self.flask.test_client()
        # from foundations_production.serving.controllers.retrain_model_package_controller import RetrainModelPackageController

        # self.mock_job_deployment.job_name.return_value = self.retraining_job_id
        # self.mock_job.run.return_value = self.mock_job_deployment
        # self.mock_create_retraining_job.return_when(
        #     self.mock_job,
        #     self.retrain_model_package_id,
        #     features_location='local:///path/to/features/file.pkl',
        #     targets_location='s3://path/to/targets/file.pkl'
        # )

        # self.package_pool_class_mock.return_value = self.package_pool_mock
        # self.package_pool_mock.get_communicator = ConditionalReturn()
        # self.package_pool_mock.get_communicator.return_when(self.communicator, self.retrain_model_package_id)

        # self.retrain_model_package_controller = RetrainModelPackageController()
        # RestAPIServer()

    @tear_down
    def tear_down(self):
        from foundations_production.serving.rest_api_server_provider import _RestAPIServerProvider
        _RestAPIServerProvider.reset()

    def test_retrain_get_request_returns_404_if_model_package_does_not_exist(self):
        response = self.client.get('/v1/some_model/model/', json={'model_id': 'some_model_id'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, 'model package not found')

    def test_retrain_get_request_returns_200_if_model_package_exists(self):
        response = self.client.get('/v1/some_model/model/', json={'model_id': 'some_model_id'})
        self.assertEqual(response.status_code, 200)

    def test_retrain_model_package_fails_with_bad_request_if_missing_target_file(self):
        self._set_model_mapping()
        payload = {
                'features_file': 'local:///path/to/features/file.pkl'
        }
        response = self.client.put("/v1/{}/model/".format(self.user_defined_model_name), json=payload)
        print(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual("Missing field in JSON data: targets_file", response.json["message"])

    def test_retraining_creates_job_scuccesfully_and_returns_correct_model_id(self):
        self._set_model_mapping()

        payload = {
            'model_id': self.retrain_model_package_id,
            'targets_file': 's3://path/to/targets/file.pkl',
            'features_file': 'local:///path/to/features/file.pkl'
        }

        response = self.client.put("/v1/{}/model/".format(self.user_defined_model_name), json=payload)

        self.assertEqual(202, response.status_code)
        self.assertEqual({'created_job_uuid': self.retraining_job_id}, response.json)

    def test_retraining_returns_404_when_model_package_not_deployed(self):

        payload = {
            'model_id': self.retrain_model_package_id,
            'user_defined_model_name': self.user_defined_model_name,
            'targets_file': 's3://path/to/targets/file.pkl',
            'features_file': 'local:///path/to/features/file.pkl'
        }

        response = self.client.put("/v1/{}/model/".format(self.user_defined_model_name), json=payload)
        self.assertEqual(404, response.status_code)

    def _set_model_mapping(self):
        from foundations_production.serving.rest_api_server_provider import get_rest_api_server

        rest_api_server = get_rest_api_server()
        model_package_mapping = rest_api_server.get_model_package_mapping()
        model_package_mapping[self.user_defined_model_name] = self.retrain_model_package_id
