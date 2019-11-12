"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 06 2018
"""

import base64

from flask import abort, redirect, request
from flask_restful import Resource

from werkzeug.wrappers import Response

from foundations_contrib.authentication.authentication_client import (
    AuthenticationClient,
)
from foundations_contrib.authentication.configs import ATLAS
from foundations_contrib.authentication.utils import (
    get_token_from_header,
    verify_token,
    get_creds_from_header,
)
from foundations_core_rest_api_components.global_state import app_manager

API = app_manager.api()


class AuthenticationController(Resource):
    """Controller for authentication related endpoints.

    This controller overloads the get method with actions related to
    authentication. To add endpoints, define methods that perform some action
    and the the endpoint api/v2beta/auth/<method_name> (without '_') will call 
    that method.
    """

    client = None

    def __init__(self):
        self.client = AuthenticationClient(ATLAS, redirect_url="/api/v2beta/auth/login")

    def get(self, action: str) -> Response:
        return getattr(self, "_" + action, lambda: abort(404))()

    def _login(self) -> Response:
        """Login to Atlas/Orbit.

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
        creds = get_creds_from_header()
        username, password = base64.b64decode(creds.encode()).decode().split(":")
        try:
            return self.client.token_using_username_password(username, password)
        except Exception as error:
            raise AuthError(str(error), 401)

    def _logout(self) -> Response:
        """Logout of Atlas/Orbit.
        
        :return: The login page of the authentication server.
        :rtype: Response

        """
        self.client.logout(get_token_from_header())
        return redirect(self.client.authentication_url())

    def _verify(self) -> None:
        """Verify a JSON web token.

        verify_token will raise a 401 error if verification fails. None otherwise.
        
        :return: None
        :rtype: None

        """
        token = get_token_from_header()
        jwks = self.client.json_web_key_set
        issuer = self.client.issuer
        verify_token(token, jwks, issuer)


API.add_resource(AuthenticationController, "/api/v2beta/auth/<string:action>")
