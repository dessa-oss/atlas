"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

from foundations_spec import Spec
from mock import patch

class TestUserInfoController(Spec):

    @patch(
        "foundations_contrib.authentication.authentication_client.AuthenticationClient",
        autospec=True,
    )
    def test_user_info_controller_uses_auth_client_to_get_info(self, mock_contructor):
        from foundations_rest_api.v2beta.controllers.user_info_controller import (
            UserInfoController,
        )
        from foundations_rest_api.global_state import app_manager

        headers = [("Authorization", "bearer token")]

        with app_manager.app().test_request_context(headers=headers):
            auth_client = mock_contructor("conf", "redirect_url")
            UserInfoController().index()
        #     auth_client.user_info.assert_called_once_with("token")
