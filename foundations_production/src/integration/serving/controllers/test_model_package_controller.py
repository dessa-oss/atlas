"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""
from mock import patch
from foundations_spec import *

from foundations_production.serving.rest_api_server import RestAPIServer

class TestModelPackageController(Spec):

    @set_up
    def set_up(self):
        from foundations_production.serving.rest_api_server_provider import get_rest_api_server

        self.rest_api_server = get_rest_api_server()
        self.flask = self.rest_api_server.flask
        self.api = self.rest_api_server.api()
        self.client = self.flask.test_client()

    @let
    def model_package_id(self):
        return self.faker.uuid4()

    @let
    def user_defined_model_name(self):
        return self.faker.word()

    def test_manage_model_package_route_is_added(self):
        self.assertIn('/v1/<user_defined_model_name>/', [rule.rule for rule in self.flask.url_map.iter_rules()])

    def test_add_new_model_package_fails_with_bad_request_if_no_model_id_is_passed(self):
        response = self.client.post("/v1/{}/".format(self.user_defined_model_name), json={"other_id": self.model_package_id})
        self.assertEqual(response.status_code, 400)
        self.assertEqual("Missing field in JSON data: model_id", response.json["message"])

    def test_rest_api_endpoint_for_deploying_models_accepts_only_json(self):
        response = self.client.post("/v1/{}/".format(self.user_defined_model_name), data='bad data')
        self.assertEqual(400, response.status_code)
        self.assertEqual('Invalid content type', response.json['message'])

    @patch.object(RestAPIServer, 'get_package_pool')
    def test_deploy_new_model_package_happens_with_post_request(self, blh):
        response = self.client.post("/v1/{}/".format(self.user_defined_model_name), json={'model_id': self.model_package_id})
        self.assertEqual(201, response.status_code)
        self.assertEqual(response.json['deployed_model_id'], self.model_package_id)

    def test_deploy_new_model_package_doesnt_happen_with_get_request(self):
        response = self.client.get("/v1/{}/".format(self.user_defined_model_name))
        self.assertEqual(response.status_code, 404)
        self.assertEqual('Model package not found: {}'.format(self.user_defined_model_name), response.json['message'])
