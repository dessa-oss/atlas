"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""
from foundations_spec import *
from foundations_production.serving.rest_api_server import RestAPIServer


class TestRestAPIServer(Spec):
    flask_app_run_mock = let_patch_mock('flask.Flask.run')
    flaskrestful_api_mock = let_patch_mock('flask_restful.Api')

    @let
    def fake_host(self):
        return self.faker.word()

    @let
    def fake_port(self):
        return self.faker.pyint

    @set_up
    def set_up(self):
        from foundations_production.serving.rest_api_server_provider import get_rest_api_server

        RestAPIServer()
        self.rest_api_server = get_rest_api_server()

    @tear_down
    def tear_down(self):
        from foundations_production.serving.rest_api_server_provider import _RestAPIServerProvider
        _RestAPIServerProvider.reset()

    def test_api_server_calls_creates_restful_api_instance(self):
        self.flaskrestful_api_mock.assert_called()

    def test_api_server_calls_flask_app_run_method(self):
        self.rest_api_server.run(host=self.fake_host, port=self.fake_port)
        self.flask_app_run_mock.assert_called_with(host=self.fake_host, port=self.fake_port)
