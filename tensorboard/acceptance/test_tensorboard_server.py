import os
import re

from foundations_spec import Spec, set_up_class, tear_down_class
from foundations_contrib.utils import run_command, cd, wait_for_condition
from dotenv import load_dotenv

load_dotenv()
SERVICE_NAME = "tb_server"
TB_SERVER_PORT = os.getenv("TB_SERVER_PORT")


class TestTensorboardServer(Spec):
    @set_up_class
    def set_up_class(cls):
        run_command(f"docker-compose up -d --force-recreate {SERVICE_NAME}")
        run_command(
            f"docker-compose logs -f > .foundations/logs/{SERVICE_NAME}.log 2>&1 &"
        )
        wait_for_condition(
            cls.service_is_ready,
            timeout=5,
            fail_hook=lambda: Spec().fail("Tensorboard Server failed to start"),
        )

    @staticmethod
    def service_is_ready():
        try:
            run_command(f"curl localhost:{TB_SERVER_PORT}", quiet=True)
            return True
        except:
            return False

    @tear_down_class
    def tear_down_class(cls):
        run_command(f"docker-compose stop {SERVICE_NAME}")
        run_command(f"docker-compose rm -f {SERVICE_NAME}")

    def test_starts_tensorboard_server(self):
        container_logs = run_command(
            f"docker-compose logs {SERVICE_NAME}"
        ).stdout.decode()
        expected_message = re.compile(
            r"TensorBoard [0-9.]+ at http:\/\/[0-9a-f]{12}:6006\/ \(Press CTRL\+C to quit\)"
        )
        try:
            self.assertIsNotNone(expected_message.search(container_logs))
        except AssertionError:
            msg = "\n".join(
                [
                    f"Expected regex {expected_message.pattern} was not found in the container logs.",
                    "Container logs:",
                    container_logs,
                ]
            )
            self.fail(msg)
