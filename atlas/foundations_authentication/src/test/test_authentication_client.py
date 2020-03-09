import json
from foundations_spec import Spec, set_up, ConditionalReturn, let_now

from foundations_authentication.authentication_client import (
    AuthenticationClient,
    keycloak_client,
)

from mock import mock_open, patch, Mock


class TestAuthenticationClient(Spec):

    redirect_url = "http://some_outher_url:0000"
    conf_file = "test/fixtures/auth_config.json"

    @let_now
    def requests_get(self):
        return self.patch("requests.get")

    @set_up
    def set_up(self):
        self.patch(
            "foundations_authentication.authentication_client.KeycloakOpenID",
            autospec=True,
            spec_set=True,
        )
        self.config = load_config(self.conf_file)
        self.auth_client = AuthenticationClient(self.config, self.redirect_url)
        self.mock_auth_backend = self.auth_client._client

    def test_keycloak_client_uses_a_dict_to_create_a_keycloak_open_id_instance(self):
        self.mock_auth_backend_class = self.patch(
            "foundations_authentication.authentication_client.KeycloakOpenID",
            ConditionalReturn(),
        )
        # These values should match the auth_config in the fixtures
        self.mock_auth_backend_class.return_when(
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

    def test_can_initialize_auth_client_with_file_path(self):
        with open(self.conf_file) as conf:
            with patch("builtins.open", mock_open(read_data=conf.read())):
                client = AuthenticationClient(self.conf_file, self.redirect_url)
        self.assertIsInstance(client, AuthenticationClient)

    def test_authentication_url_calls_keycloak_auth_url_with_the_redirect(self):
        self.auth_client.authentication_url()
        self.mock_auth_backend.auth_url.assert_called_once_with(self.redirect_url)

    def test_browser_login_opens_window_to_authentication_url(self):
        with patch("webbrowser.open") as mock_browser:
            self.auth_client.browser_login()
            mock_browser.assert_called_once_with(self.auth_client.authentication_url())

    def test_logout_delegates_to_keycloak_logout(self):
        refresh_token = self.faker.word()
        self.auth_client.logout(refresh_token)
        self.mock_auth_backend.logout.assert_called_once_with(refresh_token)

    def test_token_using_username_password_delegates_to_keycloak_token(self):
        user = self.faker.word()
        password = self.faker.word()
        self.auth_client.token_using_username_password(user, password)
        self.mock_auth_backend.token.assert_called_once_with(
            username=user, password=password
        )

    def test_token_using_auth_code_delegates_to_keycloak_token(self):
        auth_code = self.faker.word()
        self.auth_client.token_using_auth_code(auth_code)
        self.mock_auth_backend.token.assert_called_once_with(
            code=auth_code,
            grant_type=["authorization_code"],
            redirect_uri=self.redirect_url,
        )

    def test_issuer_is_set_as_attribute(self):
        with self.assert_does_not_raise():
            self.auth_client.issuer

    def test_json_web_key_set_is_set_as_attribute(self):
        with self.assert_does_not_raise():
            self.auth_client.json_web_key_set

    def test_users_info_triggers_get_request(self):
        auth_token = self.faker.word()
        users = self.auth_client.users_info(auth_token)
        url = f"{self.config['auth-server-url']}/admin/realms/Atlas/users"
        headers = {"Authorization": f"Bearer {auth_token}"}
        self.requests_get.assert_called_once_with(url, headers=headers)

    def test_users_info_transforms_user_list_to_map_of_users_based_on_id(self):
        response = [
            {"id": "some_id", "username": "some_username"},
            {"id": "another_id", "username": "another_username"},
        ]
        mock_json = Mock()
        mock_json.json.return_value = response
        self.requests_get.return_value = mock_json
        
        auth_token = self.faker.word()
        users = self.auth_client.users_info(auth_token)
        expected = {"some_id": "some_username", "another_id": "another_username"}
        self.assertEqual(expected, users)

    @patch('foundations_authentication.authentication_client.jwt')
    def test_decode_jwt(self, jwt):
        auth_token = self.faker.word()
        issuer = self.faker.word()
        self.auth_client.issuer = issuer
        self.auth_client.decode_jwt(auth_token)
        jwt.get_unverified_header.assert_called_once_with(auth_token)
        jwt.decode.assert_called_once_with(auth_token, {}, algorithms=['RS256'], audience='account',issuer=issuer)
        
        

def load_config(conf_file: str) -> dict:
    with open(conf_file) as conf:
        return json.load(conf)
