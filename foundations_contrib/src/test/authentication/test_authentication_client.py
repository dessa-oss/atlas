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
)

from mock import mock_open, patch, Mock


class TestAuthenticationClient(Spec):

    conf = "test/authentication/fixtures/auth_config.json"
    redirect_url = "http://some_outher_url:0000"
    mock_keycloak_instance = let_mock()

    @set_up
    def set_up(self):
        self.mock_keycloak_class = self.patch(
            "foundations_contrib.authentication.authentication_client.KeycloakOpenID",
            Mock(),
        )
        with open(self.conf) as conf:
            with patch("builtins.open", mock_open(read_data=conf.read())):
                self.auth_client = AuthenticationClient(self.conf, self.redirect_url)
                self.mock_keycloak = self.auth_client.client

    def test_keycloak_client_creates_a_keycloak_open_id_instance(self):
        from foundations_contrib.authentication.authentication_client import (
            keycloak_client,
        )

        self.mock_keycloak_class = self.patch(
            "foundations_contrib.authentication.authentication_client.KeycloakOpenID",
            ConditionalReturn(),
        )
        self.mock_keycloak_class.return_when(
            "KeycloakInstance",
            server_url="http://some_host:8080/auth/",
            realm_name="some_realm",
            client_id="some_resource",
            client_secret_key="some_secret",
        )
        client = keycloak_client(self.conf)
        self.assertEqual(client, "KeycloakInstance")

    def test_authentication_url_calls_keycloak_auth_url_with_the_redirect(self):
        self.auth_client.authentication_url()
        self.mock_keycloak.auth_url.assert_called_once_with(self.redirect_url)

