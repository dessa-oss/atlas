"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from acceptance.mixins.job_deploy_function_test_scaffold import JobDeployFunctionTestScaffold

import foundations
from contextlib import contextmanager

class TestDeployJobViaCLI(Spec, JobDeployFunctionTestScaffold):

    def _log_level(self):
        return 'INFO'

    @set_up
    def set_up(self):
        self._set_up()

    @tear_down
    def tear_down(self):
        self._tear_down()

    @contextmanager
    def _change_config(self, key, value):
        from foundations_contrib.global_state import config_manager

        config = config_manager.config()
        has_previous = key in config
        if has_previous:
            previous = config[key]

        try:
            config[key] = value
            yield
        finally:
            if has_previous:
                config[key] = previous
            else:
                del config[key]

    def test_deploy_job_with_all_arguments_specified_deploys_job(self):
        self._test_deploy_job_with_all_arguments_specified_deploys_job()

    def test_deploy_job_with_no_arguments_specified_deploys_job_with_defaults(self):
        self._test_deploy_job_with_no_arguments_specified_deploys_job_with_defaults()

    def _deploy_job_with_defaults(self):
        cli_deploy_process = self._run_process(['python', '-m', 'foundations', 'deploy'])
        self._check_if_successful(cli_deploy_process)
        return cli_deploy_process

    def _deploy_job(self, **kwargs):
        import json
        import os
        import os.path as path

        job_directory = kwargs['job_directory']

        params_file_path = path.join(job_directory, 'foundations_job_parameters.json')

        with open(params_file_path, 'w') as params_file:
            json.dump(kwargs['params'], params_file)

        command_to_run = [
            'python', '-m', 'foundations', 'deploy',
            '--job-directory={}'.format(job_directory),
            '--env={}'.format(kwargs['env']),
            '--entrypoint={}'.format(kwargs['entrypoint']),
            '--project-name={}'.format(kwargs['project_name'])
        ]

        cli_deploy_process = self._run_process(command_to_run)
        os.remove(params_file_path)
        self._check_if_successful(cli_deploy_process)
        return cli_deploy_process

    def _job_id_from_logs(self, driver_deploy_completed_process):
        import re

        logs_parsing_regex = re.compile("Job '(.*)' deployed")
        logs = self._driver_stdout(driver_deploy_completed_process)
        return logs_parsing_regex.findall(logs)[0]

    def _driver_stdout(self, driver_deploy_completed_process):
        return driver_deploy_completed_process.stdout.decode()

    def _uuid(self, driver_process):
        return self._job_id_from_logs(driver_process)

    def _check_if_successful(self, driver_process):
        if driver_process.returncode != 0:
            raise AssertionError(f'deploy failed:\nstdout:\n{driver_process.stdout.decode()}\nstderr:\n{driver_process.stderr.decode()}')
                