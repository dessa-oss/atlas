"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
import time
import subprocess
import foundations_contrib
from foundations_spec import *
from typing import List

class TestOrbitDeployModelViaCli(Spec):

    @set_up_class
    def set_up(self):
        from acceptance.cleanup import cleanup
        cleanup()

        _run_command(['./integration/resources/fixtures/test_server/spin_up.sh'], foundations_contrib.root() / '..')
    
    @tear_down_class
    def tear_down(self):
        _run_command(['./integration/resources/fixtures/test_server/tear_down.sh'], foundations_contrib.root() / '..')

    @let
    def mock_project_name(self):
        return self.faker.word().lower()

    @let
    def mock_user_provided_model_name(self):
        return self.faker.word().lower()

    @let
    def project_directory(self):
        return './project_code/'

    def _deploy_job(self, model_name):
        import subprocess

        # manually load the configuration file (hoping that it will trigger the configuration of the bucket)
        from foundations_contrib.global_state import config_manager

        config_manager.reset()
        config_manager.add_simple_config_path('./orbit_acceptance/fixtures/config/local.config.yaml')

        command_to_run = [
            'python', '-m', 
            'foundations',
            'orbit',
            'serve', 
            'start',
            '--project_name={}'.format(self.mock_project_name),
            '--model_name={}'.format(model_name),
            '--project_directory={}'.format(self.project_directory),
            '--env=local'
        ]

        return subprocess.run(command_to_run, cwd='./orbit_acceptance/fixtures/')

    def __check_if_error_exists(self, cli_deploy_process):
        return cli_deploy_process.returncode != 0 or len(cli_deploy_process.stderr) > 1

    def _check_if_successful(self, cli_deploy_process):
        if self.__check_if_error_exists(cli_deploy_process):
            raise AssertionError('deploy failed:\nstdout:\n{}\nstderr:\n{}'.format(cli_deploy_process.stdout, cli_deploy_process.stderr))
    
    def _check_if_unsuccessful(self, cli_deploy_process):
        if not self.__check_if_error_exists(cli_deploy_process):
            raise AssertionError('deploy succeeded when it should have failed')
    
    def test_can_successfully_run_model_serve(self):
        cli_deploy_process = self._deploy_job(self.mock_user_provided_model_name)
        self._check_if_successful(cli_deploy_process)

    @skip
    def test_will_fail_if_run_same_model_in_project_twice(self):
        self._deploy_job(self.mock_user_provided_model_name)
        cli_deploy_process = self._deploy_job(self.mock_user_provided_model_name)
        self._check_if_unsuccessful(cli_deploy_process)


def _run_command(command: List[str], cwd: str=None) -> subprocess.CompletedProcess:
    result = subprocess.run(command, cwd=cwd)
    # try:
    #     result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10, check=True, cwd=cwd)
    # except subprocess.TimeoutExpired as error:
    #     raise Exception(error.stderr.decode())
    # except subprocess.CalledProcessError as error:
    #     raise Exception(error.stderr.decode())
    # return result