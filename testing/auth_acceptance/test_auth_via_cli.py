"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2019
"""
import subprocess
import requests
import os
import time

from foundations_spec import *
from foundations_contrib.utils import wait_for_condition


class TestAuthViaClient(Spec):

    max_time_out_in_sec = 60
    ci_keycloak_host = "keycloak-headless.ci-pipeline.svc.cluster.local"
    running_on_ci = os.getenv("RUNNING_ON_CI")
    auth_server_host = ci_keycloak_host if running_on_ci else "localhost"

    @staticmethod
    def resolve_f9s_auth():
        import os.path as path

        return path.realpath("../foundations_contrib/src/")

    def keycloak_is_available(self) -> bool:
        try:
            requests.get(
                f"http://{self.auth_server_host}:8080/auth/"
            ).raise_for_status()
            return True
        except requests.ConnectionError:
            return False

    def start_and_wait_for_keycloak(self) -> None:
        full_path = os.path.join(
            self.resolve_f9s_auth(), "foundations_contrib/authentication"
        )
        subprocess.run(["bash", "launch.sh"], cwd=full_path, stdout=subprocess.PIPE)

        def keycloak_is_ready() -> bool:
            try:
                res = requests.get(f"http://{self.auth_server_host}:8080/auth/")
            except requests.exceptions.ConnectionError:
                return False
            if res.status_code == 200:
                return True
            return False

        wait_for_condition(
            keycloak_is_ready,
            60,
            fail_hook=lambda: self.fail("keycloak failed to start"),
        )

    def test_cli_login(self):
        if not self.keycloak_is_available():
            if self.running_on_ci:
                self.fail("Keycloack is unavailable in our cluster.")
            self.start_and_wait_for_keycloak()

        with self.assert_does_not_raise():
            result = subprocess.run(
                "foundations login http://localhost:5558 -u test -p test",
                stdout=subprocess.PIPE,
                shell=True,
                check=True,
            )
            self.assertEqual(result.stdout.decode().strip(), "Login Succeeded!")

