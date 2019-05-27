"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""
from mock import patch

from foundations_spec import *
from foundations_production.serving.rest_api_server import RestAPIServer
from foundations_production.serving.package_pool import PackagePool


class TestPredictionsController(Spec):

    @let
    def model_package_id(self):
        return self.faker.uuid4()

    @let
    def user_defined_model_name(self):
        return self.faker.word()

    @set_up
    def set_up(self):
        from foundations_production.serving.rest_api_server_provider import get_rest_api_server

        RestAPIServer()
        self.rest_api_server = get_rest_api_server()
        self.flask = self.rest_api_server.flask
        self.client = self.flask.test_client()

    def test_predictions_route_is_added(self):
        self.assertIn('/v1/<user_defined_model_name>/predictions/', [rule.rule for rule in self.flask.url_map.iter_rules()])

    def test_rest_api_endpoint_for_deploying_models_accepts_only_json(self):
        response = self.client.post("/v1/{}/predictions/".format(self.user_defined_model_name), data='bad data')
        self.assertEqual(400, response.status_code)
        self.assertEqual('Invalid content type', response.json['message'])

    def test_predictions_get_request_returns_404_if_model_package_does_not_exist(self):
        response = self.client.get('/v1/{}/predictions/'.format(self.user_defined_model_name))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'Model package not found: {}'.format(self.user_defined_model_name))

    def test_predictions_get_request_returns_200_if_model_package_exists(self):
        self._set_model_mapping()
        response = self.client.get('/v1/{}/predictions/'.format(self.user_defined_model_name), json={'model_id': self.model_package_id})
        self.assertEqual(response.status_code, 200)

    def test_predictions_head_request_returns_200_if_model_package_exists(self):
        self._set_model_mapping()
        response = self.client.head('/v1/{}/predictions/'.format(self.user_defined_model_name), json={'model_id': self.model_package_id})
        self.assertEqual(response.status_code, 200)

    def test_predictions_fails_with_bad_request_expected_field(self):
        from foundations_production.model_package import ModelPackage
        from integration.fixtures.fake_model_package import preprocessor, model

        with patch('foundations_production.load_model_package') as load_model_package_mock:
            load_model_package_mock.return_value = ModelPackage(preprocessor=preprocessor, model=model)
            self._deploy_model_package()

            #get_communicator_mock = self.patch('foundations_production.serving.package_pool.PackagePool.get_communicator')
            #package_pool_class_mock = self.patch('foundations_production.serving.package_pool.PackagePool')
            #package_pool_mock = Mock()
            #fake_model_package = ModelPackage(preprocessor=preprocessor, model=model)
            #package_pool_mock._model_packages = {self.model_package_id: fake_model_package}
            #package_pool_class_mock.return_value = package_pool_mock

            #self._set_model_mapping()
            payload = {
                'rows': ''
            }
            response = self.client.post("/v1/{}/predictions/".format(self.user_defined_model_name), json=payload)
            print('---->', response.data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual("Missing field in JSON data: features_file", response.json["message"])

    def test_predictions_returns_correct_predictions(self):
        payload = {
        }

        response = self.client.post("/v1/{}/predictions/".format(self.user_defined_model_name), json=payload)

        self.assertEqual(202, response.status_code)
        self.assertEqual({'created_job_uuid': self.retraining_job_id}, response.json)

    def test_predictions_returns_404_when_model_package_not_deployed(self):
        self._set_model_mapping()
        response = self.client.post("/v1/{}/predictions/".format(self.user_defined_model_name), json={})
        self.assertEqual(404, response.status_code)
        self.assertEqual('Model package not found: {}'.format(self.model_package_id), response.json['message'])

    def _set_model_mapping(self):
        from foundations_production.serving.rest_api_server_provider import get_rest_api_server

        rest_api_server = get_rest_api_server()
        model_package_mapping = rest_api_server.get_model_package_mapping()
        model_package_mapping[self.user_defined_model_name] = self.model_package_id

    def _deploy_model_package(self):
        from foundations_production.serving.controllers.model_package_controller import ModelPackageController

        model_package_controller = ModelPackageController()
        model_package_controller.params = {
            'model_id': self.model_package_id,
            'user_defined_model_name': self.user_defined_model_name
        }
        response = model_package_controller.post()
        self.assertEqual(201, response.status())
