from foundations_spec import Spec, let_mock, let, let_patch_mock, set_up

from foundations_contrib.authentication.authentication_client import AuthenticationClient

from mock import Mock

class TestAuthenticationClient(Spec):

    conf = "fixtures/auth_config.json"
    redirect_url = "http://some_outher_url:0000"
    mock_keycloak_builder = let_patch_mock(
        "foundations_contrib.authentication.authentication_client.keycloak_client"
    )

    @set_up
    def set_up(self):
        self.mock_keycloak_builder.return_value = Mock()
        self.auth_client = AuthenticationClient(self.conf, self.redirect_url)
        self.mock_keycloak = self.auth_client.client

    def test_authentication_url_calls_keycloak_auth_url_with_the_redirect(self):
        self.auth_client.authentication_url()
        self.mock_keycloak.auth_url.assert_called_once_with(self.redirect_url)
