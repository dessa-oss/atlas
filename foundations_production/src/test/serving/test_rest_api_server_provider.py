"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

from foundations_spec import *
from foundations_production.serving.rest_api_server_provider import get_rest_api_server, register_rest_api_server

class TestRestAPIServerProvider(Spec):

    @set_up
    def set_up(self):
        from foundations_production.serving.rest_api_server_provider import _RestAPIServerProvider
        _RestAPIServerProvider.reset()

    @tear_down
    def tear_down(self):
        from foundations_production.serving.rest_api_server_provider import _RestAPIServerProvider
        _RestAPIServerProvider.reset()

    @let
    def fake_path(self):
        return self.faker.uri_path()

    def test_get_rest_api_server_returns_placeholder_as_default_if_server_is_not_running(self):
        from foundations_production.serving.rest_api_server_provider import _RestAPIServerProvider

        rest_api_server_like_object = get_rest_api_server()
        self.assertIsInstance(rest_api_server_like_object, _RestAPIServerProvider)

    def test_get_rest_api_server_returns_the_server_if_server_is_running(self):
        mock_rest_api_server_instance = Mock()

        register_rest_api_server(mock_rest_api_server_instance)

        rest_api_server_like_object = get_rest_api_server()
        self.assertEqual(rest_api_server_like_object, mock_rest_api_server_instance)

    def test_if_add_resource_called_and_server_not_running_route_and_resource_are_added_to_queue(self):
        mock_rest_api_server_instance = Mock()
        mock_resource = Mock()

        rest_api_server_provider = get_rest_api_server()
        rest_api_server_provider.api().add_resource(mock_resource, self.fake_path)

        register_rest_api_server(mock_rest_api_server_instance)

        mock_rest_api_server_instance.api().add_resource.assert_called_with(mock_resource, self.fake_path)

    def test_placeholder_not_used_if_api_server_is_running(self):
        mock_rest_api_server_instance = Mock()
        mock_resource = Mock()

        rest_api_server_like_object = get_rest_api_server()
        register_rest_api_server(mock_rest_api_server_instance)

        rest_api_server_like_object.api().add_resource(mock_resource, self.fake_path)

        mock_rest_api_server_instance.api().add_resource.assert_called_with(mock_resource, self.fake_path)

    def test_provider_checks_if_instance_exists(self):
        mock_rest_api_server_instance_1 = Mock()
        mock_rest_api_server_instance_2 = Mock()

        register_rest_api_server(mock_rest_api_server_instance_1)
        register_rest_api_server(mock_rest_api_server_instance_2)

        expected_rest_api_server_instance = get_rest_api_server()

        self.assertEqual(expected_rest_api_server_instance, mock_rest_api_server_instance_1)
