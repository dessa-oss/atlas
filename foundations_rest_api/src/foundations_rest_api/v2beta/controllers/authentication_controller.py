"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 06 2018
"""

from foundations_rest_api.utils.api_resource import api_resource
from foundations_core_rest_api_components.lazy_result import LazyResult

from foundations_contrib.authentication.authentication_client import (
    AuthenticationClient,
)
from foundations_contrib.authentication.configs import ATLAS
from foundations_core_rest_api_components.global_state import app_manager

API = app_manager.api()

from flask import abort, redirect, request
from flask_restful import Resource, reqparse

from foundations_contrib.authentication.utils import get_token_from_header, verify_token


class AuthenticationController(Resource):
    client = AuthenticationClient(ATLAS, redirect_url="/api/v2beta/auth/login")

    def get(self, action):
        result = getattr(self, '_' + action, lambda: abort(404))()
        return result

    def _login(self):
        code = request.args.get("code", None)
        if code:
            return self.client.token_using_auth_code(code=code)
        
        return redirect(self.client.authentication_url())

    def _logout(self):
        refresh_token = get_token_from_header()
        self.client.logout(refresh_token)
        return redirect(self.client.authentication_url())

    def _verify(self):
        token = get_token_from_header()
        jwks = self.client.json_web_key_set
        issuer = self.client.issuer
        return verify_token(token, jwks, issuer)
        # return 200

API.add_resource(AuthenticationController, "/api/v2beta/auth/<string:action>")
