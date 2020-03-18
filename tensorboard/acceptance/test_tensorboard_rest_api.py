import os
from subprocess import PIPE

import requests

from foundations_spec import Spec, set_up_class, tear_down_class
from foundations_contrib.utils import run_command, cd, wait_for_condition
from dotenv import load_dotenv

load_dotenv()
TB_API_PORT = os.getenv("TB_API_PORT")
SERVICE_NAME = "tb_api"


class TestTensorboardRestAPI(Spec):

    tag = "latest"

    @set_up_class
    def set_up(cls):
        run_command(f"docker-compose up -d --force-recreate {SERVICE_NAME}")
        run_command(
            f"docker-compose logs -f > .foundations/logs/{SERVICE_NAME}.log 2>&1 &"
        )
        wait_for_condition(
            cls.service_is_ready,
            timeout=10,
            fail_hook=lambda: Spec().fail("Tensorboard API failed to start."),
        )

    @staticmethod
    def service_is_ready():
        try:
            container_logs = run_command(
                f"docker-compose logs {SERVICE_NAME}"
            ).stdout.decode()
            assert f"* Running on http://0.0.0.0:5000/" in container_logs
        except AssertionError:
            return False
        else:
            return True

    @tear_down_class
    def tear_down_class(cls):
        run_command(f"docker-compose stop {SERVICE_NAME}")
        run_command(f"docker-compose rm -f {SERVICE_NAME}")

    def test_tensorboard_rest_api_creates_symbolic_links_in_logdir_to_archive(self):
        test_file_content = "this is a test"

        self._create_test_file_in_mounted_archive(test_file_content)
        self._hit_the_create_sym_links_endpoint()

        cat_linked_file = (
            f"docker-compose exec {SERVICE_NAME} cat /logs/test_job/test.txt"
        )
        linked_file_content = run_command(cat_linked_file).stdout.decode().strip()

        self.assertEqual(test_file_content, linked_file_content)

    @staticmethod
    def _create_test_file_in_mounted_archive(test_file_content):
        sync_dir = (
            f".foundations/job_data/archive/test_job/synced_directories/__tensorboard__"
        )
        os.makedirs(sync_dir, exist_ok=True)
        with open(f"{sync_dir}/test.txt", "w") as test_file:
            test_file.write(test_file_content)

    @staticmethod
    def _hit_the_create_sym_links_endpoint():
        payload_from_frontend = {
            "tensorboard_locations": [
                {
                    "job_id": "test_job",
                    "synced_directory": f"archive/test_job/synced_directories/__tensorboard__",
                }
            ]
        }
        try:
            _make_request(
                "POST",
                f"http://localhost:{TB_API_PORT}/create_sym_links",
                json=payload_from_frontend,
            )
        except requests.HTTPError as e:
            msg = f"HTTP Error -> {e.response.text}"
            raise AssertionError(msg)


def _make_request(method: str, url: str, **kwargs) -> requests.Response:
    """Make a request. Raises an exception if unsuccessful."""
    res = requests.request(method, url, **kwargs)
    try:
        res.raise_for_status()
    except requests.HTTPError as exc:
        raise exc
    return res
