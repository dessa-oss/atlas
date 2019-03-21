"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 02 2019
"""

from foundations_spec.helpers import set_up
from foundations_spec.helpers.spec import Spec

class TestCLIInit(Spec):

    @set_up
    def set_up(self):
        import shutil
        import os
        import os.path

        shutil.rmtree("test-cli-init", ignore_errors=True)
        if os.path.isfile('~/.foundations/job_data/projects/my-foundations-project.tracker'):
            os.remove('~/.foundations/job_data/projects/my-foundations-project.tracker')

    def test_cli_can_deploy_job_created_by_init(self):
        import subprocess

        subprocess.call(["python", "-m", "foundations", "init", "test-cli-init"])
        driver_deploy_exit_code = subprocess.call(["/bin/bash", "-c", "cd test-cli-init && python -m foundations deploy project_code/driver.py --env local"])

        self.assertEqual(driver_deploy_exit_code, 0)

    def test_cli_can_execute_results_created_by_init(self):
        import subprocess

        subprocess.call(["python", "-m", "foundations", "init", "test-cli-init"])
        driver_deploy_exit_code = subprocess.call(["/bin/bash", "-c", "cd test-cli-init && python -m foundations deploy post_processing/results.py --env local"])

        self.assertEqual(driver_deploy_exit_code, 0)

    def test_cli_deployment_with_default_configuration_can_produce_results(self):
        import subprocess
        import re

        subprocess.call(["python", "-m", "foundations", "init", "test-cli-init"])
        driver_deploy_output = subprocess.check_output(["/bin/bash", "-c", "cd test-cli-init && python -m foundations deploy project_code/driver.py --env local"])

        job_id = re.search("Job\s+'([^']+)'\s+deployed", driver_deploy_output.decode(), re.MULTILINE)[1]

        self._assert_file_exists('{}.tracker'.format(job_id))
        self._assert_job_file_exists(job_id, 'job_source/{}.tgz'.format(job_id))
        self._assert_job_file_exists(job_id, 'miscellaneous/stage_listing')
        self._assert_job_file_exists(job_id, 'miscellaneous/stages/158903c052e1917e04b4de080ebb9ff636b37566/stage_context')
        self._assert_job_file_exists(job_id, 'miscellaneous/stages/global/stage_context')
        self._assert_job_file_exists(job_id, 'provenance')
        self._assert_job_file_exists(job_id, 'stage_contexts/158903c052e1917e04b4de080ebb9ff636b37566/stage_log')
        self._assert_job_file_exists(job_id, 'stage_contexts/global/stage_log')

    def _assert_job_file_exists(self, job_id, relative_path):
        from os.path import join

        path = join(job_id, relative_path)
        self._assert_file_exists(path)

    def _assert_file_exists(self, relative_path):
        from os.path import exists
        from os.path import join
        from os.path import expanduser

        foundations_root = expanduser('~/.foundations/job_data/archive')
        path = join(foundations_root, relative_path)
        if not exists(path):
            raise AssertionError('Expected file, `{}` to exist'.format(path))
