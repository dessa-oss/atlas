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

        return path.realpath("../foundations_authentication/src/")

    def keycloak_is_available(self) -> bool:
        try:
            requests.get(
                f"http://{self.auth_server_host}:8080/auth/"
            ).raise_for_status()
            return True
        except requests.ConnectionError:
            return False
        except requests.HTTPError as err:
            self.fail(err)

    def rest_api_is_available(self) -> bool:
        try:
            requests.get(
                f"http://localhost:37722/api/v2beta/projects"
            ).raise_for_status()
            return True
        except requests.ConnectionError:
            return False
        except requests.HTTPError as err:
            log_file = f"{os.getenv('FOUNDATIONS_HOME', '~/.foundations')}/logs/atlas_rest_api.log"
            with open(log_file) as logs:
                msg = "\n".join([str(err), "REST_API_LOGS:", logs.read()])
            self.fail(msg)

    def start_and_wait_for_keycloak(self) -> None:
        full_path = os.path.join(
            self.resolve_f9s_auth(), "foundations_authentication"
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

    def start_and_wait_for_rest_api(self) -> None:
        import subprocess

        subprocess.run(
            "export REDIS_HOST=localhost && export FOUNDATIONS_SCHEDULER_URL=localhost && cd ../devops && python startup_atlas_api.py 37722 &",
            shell=True,
        )

        def rest_api_is_ready() -> bool:
            try:
                res = requests.get("http://localhost:37722/api/v2beta/projects")
            except requests.exceptions.ConnectionError:
                return False
            if res.status_code == 200:
                return True
            else:
                return False

        wait_for_condition(
            rest_api_is_ready,
            5,
            fail_hook=lambda: self.fail("Atlas REST API failed to start"),
        )

    def test_cli_login(self):
        if not self.keycloak_is_available():
            if self.running_on_ci:
                self.fail("Keycloak is unavailable in our cluster.")
            self.start_and_wait_for_keycloak()

        if not self.rest_api_is_available():
            if self.running_on_ci:
                self.fail("Atlas REST API is unavailable in our cluster.")
            self.start_and_wait_for_rest_api()

        with self.assert_does_not_raise():
            result = subprocess.run(
                "python -m foundations login http://localhost:5558 -u test -p test",
                stdout=subprocess.PIPE,
                shell=True,
                check=True,
            )
            self.assertEqual(result.stdout.decode().strip(), "Login Succeeded!")
