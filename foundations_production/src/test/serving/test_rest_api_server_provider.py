"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""
import unittest
from mock import patch, Mock

from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers import let, let_patch_mock

class TestRestAPIServerProvider(Spec):

    def test_get_rest_api_server_returns_placeholder_if_server_is_not_running(self):
        from foundations_production.serving.rest_api_server_provider import get_rest_api_server, register_rest_api_server
        from foundations_production.serving.rest_api_server_provider import _RestAPIServerProvider

        register_rest_api_server(None)

        rest_api_server_like_object = get_rest_api_server()
        self.assertIsInstance(rest_api_server_like_object, _RestAPIServerProvider)

    def test_get_rest_api_server_returns_the_server_if_server_is_running(self):
        from foundations_production.serving.rest_api_server_provider import get_rest_api_server, register_rest_api_server
        from foundations_production.serving.rest_api_server import RestAPIServer

        rest_api_server_instance = RestAPIServer()
        register_rest_api_server(rest_api_server_instance)

        rest_api_server_like_object = get_rest_api_server()
        self.assertEqual(rest_api_server_like_object, rest_api_server_instance)