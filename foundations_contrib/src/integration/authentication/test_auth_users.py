"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2019
"""

from foundations_spec import *

class TestAuthUsers(Spec):
    
    def test_can_pull_users_from_keycloack_using_authclient(self):
        import foundations_contrib
        from foundations_contrib.authentication.authentication_client import AuthenticationClient
        import json
        from pprint import pprint
        
        with open(f'{foundations_contrib.root()}/../integration/fixtures/config/auth/foundations_keycloak_conf.json') as file:
            config = json.load(file)
        
        auth_client = AuthenticationClient(config, redirect_url="/api/v2beta/auth/login")
        token_response = auth_client.token_using_username_password('test', 'test')
        token = token_response['access_token']
        users = auth_client.users_info(token)
        self.assertTrue(len(users.keys()) > 0)