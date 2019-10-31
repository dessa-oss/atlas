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

from flask import redirect, jsonify

conf = {
    "realm": "Atlas",
    "auth-server-url": "http://localhost:8080/auth/",
    "ssl-required": "external",
    "resource": "flask",
    "credentials": {"secret": "b52bd653-2b4f-449a-a129-fb1a6a188bf9"},
    "confidential-port": 0,
}

client = AuthenticationClient(
    conf, redirect_url="/api/v2beta/auth"
)


@api_resource("/api/v2beta/auth")
class AuthenticationController:
    def index(self):
        code = self.params.get("code", None)
        if code:
            token = client.token_using_auth_code(code=code)
            return Response("Authentication", LazyResult(lambda: token))
        else:
            # TODO: Fix our custom Response class to handle redirects.
            client.browser_login()
            return Response("Authentication", LazyResult(lambda: ""))
