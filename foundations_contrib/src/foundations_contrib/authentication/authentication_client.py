import json
import os
import webbrowser

from keycloak import KeycloakOpenID

from typing import Callable, Dict, Type, Union, Any


class AuthenticationClient:
    """Currently a wrapper for the KeycloakOpenID class"""

    def __init__(self, conf: Union[str, dict], redirect_url: str):
        config = self._get_config_from_file(conf) if isinstance(conf, str) else conf
        self.client = keycloak_client(config)
        self._redirect_url = redirect_url

    def authentication_url(self) -> str:
        return self.client.auth_url(self._redirect_url)

    def browser_login(self) -> None:
        webbrowser.open(self.authentication_url())

    def token_using_auth_code(self, code) -> Dict[str, str]:
        return self.client.token(
            code=code,
            grant_type=["authorization_code"],
            redirect_uri=self._redirect_url,
        )

    @staticmethod
    def _get_config_from_file(fname: str) -> dict:
        with open(fname) as config_file:
            return json.load(config_file)


def keycloak_client(config: dict) -> Type[KeycloakOpenID]:
    return KeycloakOpenID(
        server_url=config["auth-server-url"],
        realm_name=config["realm"],
        client_id=config["resource"],
        client_secret_key=config["credentials"]["secret"],
    )

