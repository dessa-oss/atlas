"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2019
"""

from foundations_spec import Spec, let_now, set_up
from mock import patch


class TestAuthenticationController(Spec):
    @patch(
        "foundations_contrib.authentication.authentication_client.AuthenticationClient",
        autospec=True,
    )
    def test_login_without_code_redirects_to_login_page(self, mock_constructor):
        from foundations_rest_api.v2beta.controllers.authentication_controller import (
            AuthenticationController,
        )
        from foundations_rest_api.global_state import app_manager

        with app_manager.app().test_request_context():
            resp = AuthenticationController().get("login")
            self.assertIn(
                "AuthenticationClient().authentication_url()", resp.headers["Location"]
            )

    @patch(
        "foundations_contrib.authentication.authentication_client.AuthenticationClient",
        autospec=True,
    )
    def test_login_with_code_exchanges_code_for_token(self, mock_constructor):
        from foundations_rest_api.v2beta.controllers.authentication_controller import (
            AuthenticationController,
        )
        from foundations_rest_api.global_state import app_manager

        with app_manager.app().test_request_context(query_string="code=code"):
            auth_client = mock_constructor("conf", "redirect_url")
            AuthenticationController().get("login")
            auth_client.token_using_auth_code.assert_called_once_with("code")

    @patch(
        "foundations_contrib.authentication.authentication_client.AuthenticationClient",
        autospec=True,
    )
    def test_login_with_code_returns_redirect_to_frontend(self, mock_constructor):
        from foundations_rest_api.v2beta.controllers.authentication_controller import (
            AuthenticationController,
        )
        from foundations_rest_api.global_state import app_manager

        with app_manager.app().test_request_context(query_string="code=code"):
            auth_client = mock_constructor("conf", "redirect_url")
            resp = AuthenticationController().get("login")
            self.assertIn("http://localhost:3000/projects", resp.headers["Location"])

    @patch(
        "foundations_contrib.authentication.authentication_client.AuthenticationClient",
        autospec=True,
    )
    def test_cli_login(self, mock_constructor):
        from foundations_rest_api.v2beta.controllers.authentication_controller import (
            AuthenticationController,
        )
        from foundations_rest_api.global_state import app_manager

        with app_manager.app().test_request_context(query_string="code=code"):


    @patch(
        "foundations_contrib.authentication.authentication_client.AuthenticationClient",
        autospec=True,
    )
    def test_logout_uses_client_logout(self, mock_constructor):
        from foundations_rest_api.v2beta.controllers.authentication_controller import (
            AuthenticationController,
        )
        from foundations_rest_api.global_state import app_manager

        headers = {"Authorization": "bearer token"}
        # headers = {}
        with app_manager.app().test_request_context(headers=headers):
            auth_client = mock_constructor("conf", "redirect_url")
            AuthenticationController().get("logout")
            auth_client.logout.assert_called_once_with("token")

    @patch(
        "foundations_contrib.authentication.authentication_client.AuthenticationClient",
        autospec=True,
    )
    def test_logout_redirect_to_login_page(self, _):
        from foundations_rest_api.v2beta.controllers.authentication_controller import (
            AuthenticationController,
        )
        from foundations_rest_api.global_state import app_manager

        headers = {'Authorization': 'bearer token'}

        with app_manager.app().test_request_context(headers=headers):
            resp = AuthenticationController().get("logout")
            self.assertIn(
                "AuthenticationClient().authentication_url()", resp.headers["Location"]
            )

    # @patch(
    #     "foundations_rest_api.v2beta.controllers.authentication_controller.verify_token",
    #     autospec=True
    # )
    @patch(
        "foundations_contrib.authentication.authentication_client.AuthenticationClient",
        autospec=True,
    )
    def test_verify_calls_verify_token_with_token_and_client_jwks_issuer(self, mock_constructor):
        from foundations_rest_api.v2beta.controllers.authentication_controller import (
            AuthenticationController,
        )
        from foundations_rest_api.global_state import app_manager

        headers = {"Authorization": "bearer token"}

        with app_manager.app().test_request_context(headers=headers):
            mock_constructor.return_value.json_web_key_set = 'foo'
            AuthenticationController().get("verify")
            mock_verify.assert_called_once_with("token")