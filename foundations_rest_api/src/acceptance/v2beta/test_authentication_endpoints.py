"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2019
"""

from foundations_spec import Spec, let, set_up

from unittest import skip

@skip('Not implemented yet')
class TestAuthenticationEndpoints(Spec):

    URL = '/api/v2beta/auth/{action}'

    
    def client(self):
        from foundations_rest_api.global_state import app_manager
        return app_manager.app().test_client()

    def test_login(self):
        resp = self.client().get(self.URL.format(action='login'))
