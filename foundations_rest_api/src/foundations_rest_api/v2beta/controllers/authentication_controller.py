"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 06 2018
"""
import os.path
import subprocess as sp
import webbrowser

from foundations_rest_api.utils.api_resource import api_resource
from foundations_core_rest_api_components.response import Response
from foundations_core_rest_api_components.lazy_result import LazyResult

from foundations_contrib.authentication.authentication_client import (
    AuthenticationClient,
)
from foundations_contrib.authentication.configs import ATLAS

# from flask import redirect, jsonify


@api_resource("/api/v2beta/auth")
class AuthenticationController:
    client = AuthenticationClient(ATLAS, redirect_url="/api/v2beta/auth")

    def index(self):
        code = self.params.get("code", None)
        if code:
            token = self.client.token_using_auth_code(code=code)
            return Response("Authentication", LazyResult(lambda: token))
        else:
            # TODO: Fix our custom Response class to handle redirects.
            self.client.browser_login()
            return Response("Authentication", LazyResult(lambda: ""))
