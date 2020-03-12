
from foundations_spec import Spec, let_now, set_up, Mock, let
from mock import patch

class TestAuthenticationController(Spec):
    @let_now
    def auth_client(self):
        constructor = self.patch(
            "foundations_authentication.authentication_client.AuthenticationClient",
            autospec=True,
        )
        return constructor('conf', 'redirect')

    @let
    def auth_controller(self):
        from foundations_core_rest_api_components.v1.controllers.authentication_controller import (
            AuthenticationController,
        )

        return AuthenticationController()

    def test_login_without_code_redirects_to_login_page(self):
        from foundations_core_rest_api_components.v1.controllers.authentication_controller import (
            AuthenticationController,
        )
        from foundations_rest_api.global_state import app_manager

        with app_manager.app().test_request_context():
            resp = self.auth_controller.get("login")
            self.assertIn(
                "AuthenticationClient().authentication_url()", resp.headers["Location"]
            )

    def test_login_with_code_exchanges_code_for_token(self):
        from foundations_rest_api.global_state import app_manager

        with app_manager.app().test_request_context(query_string="code=code"):
            self.auth_controller.get("login")
            self.auth_client.token_using_auth_code.assert_called_once_with(code="code")

    def test_login_with_code_returns_redirect_to_frontend(self):
        from foundations_rest_api.global_state import app_manager

        with app_manager.app().test_request_context(query_string="code=code"):
            resp = self.auth_controller.get("login")
            self.assertIn("http://localhost:3000/projects", resp.headers["Location"])

    def test_cli_login(self):
        from foundations_rest_api.global_state import app_manager
        import base64

        username = self.faker.word()
        password = self.faker.word()
        code = base64.b64encode(f"{username}:{password}".encode()).decode()

        headers = {"Authorization": f"Basic {code}"}

        with app_manager.app().test_request_context(headers=headers):
            self.auth_controller.get("cli_login")
            self.auth_client.token_using_username_password.assert_called_once_with(
                username, password
            )

    def test_logout_uses_client_logout(self):
        from foundations_rest_api.global_state import app_manager

        headers = {"Authorization": "bearer token"}

        with app_manager.app().test_request_context(headers=headers):
            self.auth_controller.get("logout")
            self.auth_client.logout.assert_called_once_with("token")

    @patch(
        "foundations_authentication.utils.verify_token"
    )
    def test_verify_calls_verify_token_with_token_and_client_jwks_issuer(self, verify):

        self.auth_client.json_web_key_set = None
        self.auth_client.issuer = "value"

        from foundations_rest_api.global_state import app_manager

        headers = {"Authorization": "bearer token"}

        with app_manager.app().test_request_context(headers=headers):
            self.auth_controller.get("verify")
            verify.assert_called_once_with(
                "token", self.auth_client.json_web_key_set, self.auth_client.issuer
            )
