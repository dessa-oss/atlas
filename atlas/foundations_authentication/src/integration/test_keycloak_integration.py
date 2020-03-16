import json
from foundations_spec import Spec, set_up, ConditionalReturn, let_now, set_up_class

from foundations_authentication.authentication_client import (
    AuthenticationClient,
    keycloak_client,
)
import subprocess
from foundations_contrib.utils import wait_for_condition

import requests
from typing import Callable
import os

class TestKeycloakIntegration(Spec):

    redirect_url = "some_redirect"
    conf_file = "integration/fixtures/atlas_client.json"
    user = "test"
    auth_server_host = 'keycloak-headless.ci-pipeline.svc.cluster.local' if os.environ.get('RUNNING_ON_CI', False) == 'TRUE' else 'localhost'

    @set_up_class
    def set_up_class(cls):
        if not os.environ.get('RUNNING_ON_CI', False):
            def condition() -> bool:
                try:
                    res = requests.get(f"http://localhost:8080/auth/")
                except requests.exceptions.ConnectionError:
                    return False
                if res.status_code == 200:
                    return True
                return False

            wait_for_condition(condition, 60)

    @set_up
    def set_up(self):
        self.config = load_json(self.conf_file)
        self.realm = self.config["realm"]
        self.auth_url = f'http://{self.auth_server_host}:8080/auth'
        self.config['auth-server-url'] = self.auth_url
        self.client_name = self.config["resource"]
        self.auth_client = AuthenticationClient(self.config, self.redirect_url)

    def test_authentication_url_returns_correct_url(self):
        url = self.auth_client.authentication_url()
        expected = (f"{self.auth_url}/realms/{self.realm}/protocol/openid-connect/"
                    f"auth?client_id={self.client_name}&response_type=code"
                    f"&redirect_uri={self.redirect_url}")
        self.assertEqual(expected, url)

    def test_token_using_username_password_returns_an_access_token(self):
        token = self._get_token_using_test_username_and_password()
        self.assertIn("access_token", token)

    def test_users_info_returns_map_of_user_ids_to_usernames(self):
        token = self._get_token_using_test_username_and_password()
        users = self.auth_client.users_info(token["access_token"])
        self.assertIn(self.user, users.values())

    def _get_token_using_test_username_and_password(self):
        user = self.user
        password = self.user
        return self.auth_client.token_using_username_password(user, password)


def load_json(json_file: str) -> dict:
    with open(json_file) as jsonfile:
        return json.load(jsonfile)
