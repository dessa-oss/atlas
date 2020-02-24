
import base64

from flask import abort, redirect, request
from flask_restful import Resource
from foundations_core_rest_api_components.config.configs import ATLAS
from werkzeug.wrappers import Response


class AuthenticationController(Resource):
    """Controller for authentication related endpoints.

    This controller overloads the get method with actions related to
    authentication. To add endpoints, define methods that perform some action
    and the the endpoint api/v2beta/auth/<method_name> (without '_') will call 
    that method.
    """

    client = None

    def __init__(self):
        from foundations_authentication.authentication_client import (
            AuthenticationClient,
        )

        self.client = AuthenticationClient(ATLAS, redirect_url="/api/v2beta/auth/login")

    def get(self, action: str) -> Response:
        return getattr(self, "_" + action, lambda: abort(404))()

    def _login(self) -> Response:
        """Login to Atlas.

        This endpoint works by checking for an authorization code that comes from
        the authentication server. If that code is not present, then we redirect
        to the authentication server's own login page. The authentication sever
        then redirects back here with the code so that we can obtain a token.
        
        :return: The identity token with a location to redirect.
        :rtype: Response
        
        """
        code = request.args.get("code", None)
        if code:
            token = self.client.token_using_auth_code(code=code)
            print(token)
            return Response(
                response=token,
                status=303,
                headers={"Location": "http://localhost:3000/projects"},
            )

        return redirect(self.client.authentication_url())

    def _cli_login(self) -> Response:
        from foundations_core_rest_api_components.exceptions import AuthError
        from foundations_authentication.utils import get_creds_from_header

        try:
            creds = get_creds_from_header()
            username, password = base64.b64decode(creds.encode()).decode().split(":")
            return self.client.token_using_username_password(username, password)
        except Exception as error:
            raise AuthError(str(error), 401)

    def _logout(self) -> Response:
        """Logout of Atlas.

        :return: Just a successful response, no content.
        :rtype: Response

        """
        from foundations_authentication.utils import get_token_from_header

        self.client.logout(get_token_from_header())
        return Response(status=200)

    def _verify(self) -> Response:
        """Verify a JSON web token.

        verify_token will raise a 401 error if verification fails. Token information otherwise.
        
        :return: A dictionary containing token information.
        :rtype: dict

        """
        from foundations_authentication.utils import get_token_from_header
        from foundations_authentication.utils import verify_token

        token = get_token_from_header()
        jwks = self.client.json_web_key_set
        issuer = self.client.issuer
        return verify_token(token, jwks, issuer)
