"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
import time
import subprocess
import requests
import foundations_contrib
from foundations_spec import *
from typing import List
from foundations import config_manager

class TestOrbitDeployModelViaCli(Spec):

    port = 31998
    max_time_out_in_sec = 60

    @set_up_class
    def set_up_class(self):
        from acceptance.cleanup import cleanup
        cleanup()
        config_manager['log_level'] = 'INFO'
        
        _run_command(['./integration/resources/fixtures/test_server/spin_up.sh'], foundations_contrib.root() / '..')
    
    @tear_down_class
    def tear_down_class(self):
        pass
        _run_command(['./integration/resources/fixtures/test_server/tear_down.sh'], foundations_contrib.root() / '..')

    @set_up
    def set_up(self):
        self.base_url = f'http://{self._get_scheduler_ip()}:{self.port}/{self.mock_project_name}/{self.mock_user_provided_model_name}'

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

        # process_result = subprocess.run(command_to_run, cwd='./orbit_acceptance/fixtures/', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process_result = subprocess.run(command_to_run, cwd='./orbit_acceptance/fixtures/')
        self._check_if_process_successful(process_result)

    def _get_scheduler_ip(self):
        import os

        if 'FOUNDATIONS_SCHEDULER_HOST' not in os.environ:
            raise RuntimeError('please set FOUNDATIONS_SCHEDULER_HOST env var')

        return os.environ['FOUNDATIONS_SCHEDULER_HOST']

    def _wait_for_server(self):
        import time

        start_time = time.time()

        while time.time() - start_time < self.max_time_out_in_sec:
            try:
                requests.get(self.base_url)
                return
            except:
                time.sleep(0.200)

        self.fail(f'server never started')

    def _check_if_error_exists(self, cli_deploy_process):
        # return cli_deploy_process.returncode != 0 or (cli_deploy_process is not None and len(cli_deploy_process.stderr) > 1)
        return cli_deploy_process.returncode != 0

    def _check_if_process_successful(self, cli_deploy_process):
        if self._check_if_error_exists(cli_deploy_process):
            raise AssertionError('deploy failed:\nstdout:\n{}\nstderr:\n{}'.format(cli_deploy_process.stdout, cli_deploy_process.stderr))
    
    def _check_if_unsuccessful(self, cli_deploy_process):
        if not self._check_if_error_exists(cli_deploy_process):
            raise AssertionError('deploy succeeded when it should have failed')
    
    def _check_if_endpoint_available(self):
        end_point_url = f'{self.base_url}/predict'
        try:
            return requests.post(end_point_url, json={'a': 20, 'b': 30}).json()
        except:
            return None

    def test_can_successfully_run_model_serve(self):
        self._deploy_job(self.mock_user_provided_model_name)

        self._wait_for_server()

        result = self._check_if_endpoint_available()
        self.assertIsNotNone(result)

    # def test_will_fail_if_run_same_model_in_project_twice(self):
    #     self._deploy_job(self.mock_user_provided_model_name)
    #     cli_deploy_process = self._deploy_job(self.mock_user_provided_model_name)
    #     self._check_if_unsuccessful(cli_deploy_process)


def _run_command(command: List[str], cwd: str=None) -> subprocess.CompletedProcess:
    result = subprocess.run(command, cwd=cwd)
    # try:
    #     result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10, check=True, cwd=cwd)
    # except subprocess.TimeoutExpired as error:
    #     raise Exception(error.stderr.decode())
    # except subprocess.CalledProcessError as error:
    #     raise Exception(error.stderr.decode())
    # return result