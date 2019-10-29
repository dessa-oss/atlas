import json
import os
import webbrowser

from keycloak import KeycloakOpenID

from typing import Callable


class AuthenticationClient:
    """Currently a wrapper for the KeycloakOpenID class"""

    def __init__(self, conf: str, redirect_url: str):
        self.client = keycloak_client(conf)
        self._redirect_url = redirect_url

    def authentication_url(self) -> str:
        return self.client.auth_url(self._redirect_url)

    def browser_login(self) -> None:
        webbrowser.open(self.authentication_url())


def keycloak_client(conf: str) -> KeycloakOpenID:
    with open(conf) as config_file:
        config = json.load(config_file)
        return KeycloakOpenID(
            server_url=config["auth-server-url"],
            realm_name=config["realm"],
            client_id=config["resource"],
            client_secret_key=config["credentials"]["secret"],
        )
