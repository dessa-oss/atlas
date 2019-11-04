import json
from foundations_spec import (
    Spec,
    let_mock,
    let,
    let_patch_mock,
    set_up,
    ConditionalReturn,
)

from foundations_contrib.authentication.authentication_client import (
    AuthenticationClient,
    keycloak_client,
)

from mock import mock_open, patch, Mock


class TestAuthenticationClient(Spec):

    redirect_url = "http://some_outher_url:0000"
    conf_file = "test/authentication/fixtures/auth_config.json"

    @set_up
    def set_up(self):
        self.patch(
            "foundations_contrib.authentication.authentication_client.KeycloakOpenID",
            Mock(),
        )
        with open(self.conf_file) as conf:
            config = json.load(conf)
            self.auth_client = AuthenticationClient(config, self.redirect_url)
            self.mock_keycloak = self.auth_client.client

    def test_keycloak_client_uses_a_dict_to_create_a_keycloak_open_id_instance(self):
        self.mock_keycloak_class = self.patch(
            "foundations_contrib.authentication.authentication_client.KeycloakOpenID",
            ConditionalReturn(),
        )
        # These values should match the auth_config in the fixtures
        self.mock_keycloak_class.return_when(
            "KeycloakInstance",
            server_url="http://some_host:8080/auth/",
            realm_name="some_realm",
            client_id="some_resource",
            client_secret_key="some_secret",
        )
        with open(self.conf_file) as conf:
            config = json.load(conf)
        client = keycloak_client(config)
        self.assertEqual(client, "KeycloakInstance")

    def test_can_initalize_auth_client_with_file_path(self):
        with open(self.conf_file) as conf:
            with patch("builtins.open", mock_open(read_data=conf.read())):
                client = AuthenticationClient(self.conf_file, self.redirect_url)
        self.assertIsInstance(client, AuthenticationClient)

    def test_authentication_url_calls_keycloak_auth_url_with_the_redirect(self):
        self.auth_client.authentication_url()
        self.mock_keycloak.auth_url.assert_called_once_with(self.redirect_url)

    def test_browser_login_opens_window_to_authentication_url(self):
        with patch("webbrowser.open") as mock_browser:
            self.auth_client.browser_login()
            mock_browser.assert_called_once_with(self.auth_client.authentication_url())

    # def test_token_using_auth_code(self):
    #     auth_code = self.faker.word()
    #     self.auth_client.token_using_auth_code(auth_code)
