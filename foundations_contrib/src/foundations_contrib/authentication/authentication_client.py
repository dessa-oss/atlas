"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

import webbrowser
import json

from typing import Type, Union
from keycloak import KeycloakOpenID


class AuthenticationClient:
    """A facade for the some authentication implementation, currently keycloak."""

    def __init__(self, conf: Union[str, dict], redirect_url: str):
        """
        :param conf: Client configuration. Can be a path to a json file.
        :type conf: Union[str, dict]
        :param redirect_url: The url that the authentication server will redirect
            to after a successful login.
        :type redirect_url: str
        """

        config = self._get_config_from_file(conf) if isinstance(conf, str) else conf
        self._redirect_url = redirect_url
        self._client = keycloak_client(config)
        self.issuer = self._client.well_know()["issuer"]
        self.json_web_key_set = self._client.certs()

    def authentication_url(self) -> str:
        """The URL of the authentication server that is used to authenticate.

        :return: The request url including params.
        :rtype: str
        """

        return self._client.auth_url(self._redirect_url)

    def browser_login(self) -> None:
        """Open a browser window to login.

        :rtype: None
        """

        webbrowser.open(self.authentication_url())

    def logout(self, refresh_token: str) -> None:
        """Logout the user.
        
        :param refresh_token: The refresh token provided by the last authentication
            payload.
        :type refresh_token: str
        """

        self._client.logout(refresh_token)

    def token_using_auth_code(self, code: str) -> dict:
        """Obtain a token using an authorization code from the auth server.

        An authorization code is obtained from the auth server after a successful
        login.

        :param code: The authorization code.
        :type code: str
        :return: A dictionary containing the token, refresh token, and other info.
        :rtype: dict
        """

        return self._client.token(
            code=code,
            grant_type=["authorization_code"],
            redirect_uri=self._redirect_url,
        )

    def token_using_username_password(self, username: str, password: str) -> dict:
        return self._client.token(username=username, password=password)

    def user_info(self, token: str) -> dict:
        """Obtain the user info in the auth server associated with some token.

        :param token: The identity token.
        :type token: str
        :return: JSON formatted payload containing user info.
        :rtype: dict
        """

        return self._client.userinfo(token)

    @staticmethod
    def _get_config_from_file(fname: str) -> dict:
        with open(fname) as config_file:
            return json.load(config_file)


def keycloak_client(config: dict) -> Type[KeycloakOpenID]:
    creds = config.get("credentials", None)
    secret_key = creds["secret"] if creds else None
    return KeycloakOpenID(
        server_url=config["auth-server-url"] + "/",
        realm_name=config["realm"],
        client_id=config["resource"],
        client_secret_key=secret_key,
    )


# Here for development purposes

# from foundations_contrib.authentication.configs import ATLAS

# client = AuthenticationClient(ATLAS, redirect_url="/api/v2beta/auth")
