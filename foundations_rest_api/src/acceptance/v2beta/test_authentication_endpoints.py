"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2019
"""
import os

import foundations
from foundations_spec import Spec, let
from foundations_rest_api.global_state import app_manager
from acceptance.api_acceptance_test_case_base import APIAcceptanceTestCaseBase

from unittest import skip

class TestAuthenticationEndpoints(Spec, APIAcceptanceTestCaseBase):
    url = '/api/v2beta/auth'
    sorting_columns = []
    filtering_columns = []

    @let
    def test_client(self):
        return app_manager.app().test_client()

    def test_get_route(self):
        data = super().test_get_route()
        print('DATA =======> ', data)
    
