"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 02 2019
"""

from foundations_spec import *

class TestCLIInit(Spec):

    @let
    def job_root(self):
        from foundations_contrib.utils import foundations_home
        from os.path import expanduser

        return expanduser(foundations_home() + '/job_data')

    @let
    def redis(self):
        from foundations_contrib.global_state import redis_connection
        return redis_connection

    @set_up
    def set_up(self):
        import shutil
        import os
        import os.path

        shutil.rmtree("test-cli-init", ignore_errors=True)
        if os.path.isfile(self.job_root + '/projects/my-foundations-project.tracker'):
            os.remove(self.job_root + '/projects/my-foundations-project.tracker')

    def test_cli_can_deploy_job_created_by_init(self):
        import subprocess

        subprocess.call(["python", "-m", "foundations", "init", "test-cli-init"])
        driver_deploy_exit_code = subprocess.call(["/bin/bash", "-c", "cd test-cli-init && python project_code/driver.py"])

        self.assertEqual(driver_deploy_exit_code, 0)

    def test_cli_deployment_with_default_configuration_can_produce_results(self):
        import subprocess
        import re

        subprocess.call(["python", "-m", "foundations", "init", "test-cli-init"])
        self._append_redis_job_id_log_to_driver_file()
        driver_deploy_output = subprocess.check_output(["/bin/bash", "-c", "cd test-cli-init && python project_code/driver.py"])
        job_id = self.redis.get('foundations_testing_job_id').decode()

        self._assert_job_file_exists(job_id, 'miscellaneous/job_artifact_listing.pkl')

    def _append_redis_job_id_log_to_driver_file(self):
        self.redis.delete('foundations_testing_job_id')
        with open('test-cli-init/project_code/driver.py', 'a') as file:
            file.write(
                '\nfrom foundations_contrib.global_state import redis_connection, current_foundations_context\n'
                'redis_connection.set("foundations_testing_job_id", current_foundations_context().pipeline_context().job_id)\n'
            )
        
    def _assert_job_file_exists(self, job_id, relative_path):
        from os.path import join

        path = join(job_id, relative_path)
        self._assert_file_exists(path)

    def _assert_file_exists(self, relative_path):
        from os.path import exists
        from os.path import join
        from os.path import expanduser

        foundations_root = expanduser(self.job_root + '/archive')
        path = join(foundations_root, relative_path)
        if not exists(path):
            raise AssertionError('Expected file, `{}` to exist'.format(path))
