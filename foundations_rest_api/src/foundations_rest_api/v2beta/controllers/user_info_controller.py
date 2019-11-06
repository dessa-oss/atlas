"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 06 2018
"""

from foundations_rest_api.utils.api_resource import api_resource
from foundations_core_rest_api_components.response import Response
from foundations_core_rest_api_components.lazy_result import LazyResult

from foundations_contrib.authentication.authentication_client import (
    AuthenticationClient,
)
from foundations_contrib.authentication.utils import get_token_from_header
from foundations_contrib.authentication.configs import ATLAS


@api_resource("/api/v2beta/auth/userinfo")
class UserInfoController:
    client = AuthenticationClient(ATLAS, redirect_url="/api/v2beta/auth")

    def index(self):
        token = get_token_from_header()
        info = self.client.user_info(token)
        return Response("UserInfo", LazyResult(lambda: info))
