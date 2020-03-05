
import json
from typing import Type, Union, Dict
import webbrowser

from jose import jwt

from keycloak import KeycloakOpenID


class AuthenticationClient:
    """A facade for the some authentication implementation, currently keycloak."""

    issuer = None
    json_web_key_set: dict = {}

    def __init__(self, conf: Union[str, dict], redirect_url: str):
        """
        :param conf: Client configuration. Can be a path to a json file.
        :type conf: Union[str, dict]
        :param redirect_url: The url that the authentication server will redirect
            to after a successful login.
        :type redirect_url: str
        """

        self.config = self._get_config_from_file(conf) if isinstance(conf, str) else conf
        self._redirect_url = redirect_url
        self._client = keycloak_client(self.config)
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
        """[summary]
        
        :param username: [description]
        :type username: str
        :param password: [description]
        :type password: str
        :return: [description]
        :rtype: dict
        """
        return self._client.token(username=username, password=password)

    def users_info(self, auth_token: str) -> Dict[str, str]:
        import requests
        
        users_response = requests.get(
            f"{self.config['auth-server-url']}/admin/realms/Atlas/users",
            headers={"Authorization": f"Bearer {auth_token}"},
        ).json()
        return {info["id"]: info["username"] for info in users_response}

    def decode_jwt(self, auth_token: str) -> dict:
        unverified_header = jwt.get_unverified_header(auth_token)
        rsa_key = self._jwt_rsa_key(unverified_header)
        payload = jwt.decode(
            auth_token, rsa_key, algorithms=["RS256"], audience="account", issuer=self.issuer,
        )
        return payload

    def _jwt_rsa_key(self, unverified_header) -> Dict[str, str]:
        rsa_key: Dict[str, str] = {}
        for key in self.json_web_key_set["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
        return rsa_key

    @staticmethod
    def _get_config_from_file(fname: str) -> dict:
        with open(fname) as config_file:
            return json.load(config_file)


def keycloak_client(config: dict) -> KeycloakOpenID:
    creds = config.get("credentials", None)
    secret_key = creds["secret"] if creds else None
    return KeycloakOpenID(
        server_url=config["auth-server-url"] + "/",
        realm_name=config["realm"],
        client_id=config["resource"],
        client_secret_key=secret_key,
    )
