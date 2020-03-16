
from foundations_spec import *
from foundations_contrib.utils import foundations_home
import os
import os.path
from os.path import expanduser, join


class TestSubmitWithAuth(Spec):
    @set_up
    def set_up(self):
        credential_filepath = expanduser(join(foundations_home(), "credentials.yaml"))
        if os.path.exists(credential_filepath):
            os.remove(credential_filepath)

    def test_submit_through_cli_fails_if_not_authenticated(self):
        import subprocess

        result = subprocess.run(
            "python -m foundations submit scheduler auth_acceptance/fixtures foundations_job.py",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        output = result.stdout.decode().strip() or result.stderr.decode().strip()
        self.assertIn("Token is not valid", output)
