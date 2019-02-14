"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 02 2019
"""

from foundations_internal.testing.helpers import set_up
from foundations_internal.testing.helpers.spec import Spec

class TestCLIInit(Spec):

    @set_up
    def set_up(self):
        import shutil

        shutil.rmtree("test-cli-init", ignore_errors=True)

    def test_cli_can_deploy_job_created_by_init(self):
        import subprocess

        subprocess.call(["python", "-m", "foundations", "init", "test-cli-init"])
        driver_deploy_exit_code = subprocess.call(["/bin/bash", "-c", "cd test-cli-init && python -m foundations deploy project_code/driver.py --env local"])

        self.assertEqual(driver_deploy_exit_code, 0)

    def test_cli_can_run_job_with_default_configuration(self):
        import subprocess

        subprocess.call(["python", "-m", "foundations", "init", "test-cli-init"])
        driver_deploy_exit_code = subprocess.call(["/bin/bash", "-c", "cd test-cli-init/project_code && python driver.py"])

        self.assertEqual(driver_deploy_exit_code, 0)
