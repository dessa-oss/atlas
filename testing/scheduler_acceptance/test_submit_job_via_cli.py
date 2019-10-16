"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from scheduler_acceptance.mixins.job_deploy_function_test_scaffold import JobDeployFunctionTestScaffold

import foundations
from contextlib import contextmanager

class TestSubmitJobViaCLI(Spec, JobDeployFunctionTestScaffold):

    @let
    def submission_environment(self):
        return 'scheduler_with_remote_redis'

    @let
    def base_config_path(self):
        return f'foundations_home/config/submission/scheduler.config.yaml'

    @let
    def config_path(self):
        return f'foundations_home/config/submission/{self.submission_environment}.config.yaml'

    def _log_level(self):
        return 'INFO'

    @set_up
    def set_up(self):
        self._set_up()

    @tear_down
    def tear_down(self):
        self._tear_down()

    def test_submit_job_with_all_arguments_specified_submits_job(self):
        self._test_submit_job_with_all_arguments_specified_submits_job()

    def test_submit_job_with_no_arguments_specified_submits_job_with_defaults(self):
        self._test_submit_job_with_no_arguments_specified_submits_job_with_defaults()

    def _submit_job_with_defaults(self):
        cli_submit_process = self._run_process(['python', '-m', 'foundations', 'submit'])
        self._check_if_successful(cli_submit_process)
        return cli_submit_process

    def _submit_job(self, **kwargs):
        import json
        import os
        import os.path as path

        job_directory = kwargs['job_directory']

        params_file_path = path.join(job_directory, 'foundations_job_parameters.json')

        with open(params_file_path, 'w') as params_file:
            json.dump(kwargs['params'], params_file)

        command_to_run = [
            'python', '-m', 'foundations', 'submit',
            '--job-directory={}'.format(job_directory),
            '--entrypoint={}'.format(kwargs['entrypoint']),
            '--project-name={}'.format(kwargs['project_name'])
        ]

        cli_submit_process = self._run_process(command_to_run)
        os.remove(params_file_path)
        self._check_if_successful(cli_submit_process)
        return cli_submit_process

    def _job_id_from_logs(self, driver_submit_completed_process):
        import re

        logs_parsing_regex = re.compile("Job '(.*)' deployed.")
        logs = self._driver_stdout(driver_submit_completed_process)
        return logs_parsing_regex.findall(logs)[0]

    def _driver_stdout(self, driver_submit_completed_process):
        return driver_submit_completed_process.stdout.decode()

    def _uuid(self, driver_process):
        return self._job_id_from_logs(driver_process)

    def _check_if_successful(self, driver_process):
        if driver_process.returncode != 0:
            raise AssertionError(f'submit failed:\nstdout:\n{driver_process.stdout.decode()}\nstderr:\n{driver_process.stderr.decode()}')
                