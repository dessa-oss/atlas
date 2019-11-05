import json
import os
import webbrowser

from keycloak import KeycloakOpenID

from typing import Callable, Dict, Type, Union, Any


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
        self.client = keycloak_client(config)
        self._redirect_url = redirect_url

    def authentication_url(self) -> str:
        """The URL of the authentication server that is used to authenticate.
        
        :return: The request url including params.
        :rtype: str
        """

        return self.client.auth_url(self._redirect_url)

    def browser_login(self) -> None:
        """Open a browser window to login.

        :rtype: None
        """

        webbrowser.open(self.authentication_url())

    def token_using_auth_code(self, code: str) -> dict:
        """Obtain a token using an authorization code from the auth server.

        An authorization code is obtained from the auth server after a successful
        login.

        :param code: The authorization code.
        :type code: str
        :return: [description]
        :rtype: dict
        """

        return self.client.token(
            code=code,
            grant_type=["authorization_code"],
            redirect_uri=self._redirect_url,
        )

    def token_using_username_password(self, username: str, password: str) -> dict:
        return self.client.token(username=username, password=password)

    def json_web_key_set(self) -> dict:
        """The JSWKS needed to verify a json web token.

        :return: The set of public keys issued by the auth server.
        :rtype: dict
        """
        return self.client.certs()

    def well_known(self) -> dict:
        """Metadata associated with the auth server

        :return: A dictionary containing useful information about the server.
        :rtype: dict
        """

        return self.client.well_know()

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
auth_config = {
    "realm": "Atlas",
    "auth-server-url": "http://localhost:8080/auth",
    "ssl-required": "external",
    "resource": "foundations",
    "confidential-port": 0,
}
client = AuthenticationClient(auth_config, redirect_url="/api/v2beta/auth")
