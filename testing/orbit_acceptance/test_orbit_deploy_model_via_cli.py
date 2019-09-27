"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import foundations
import time
import subprocess
import requests
import foundations_contrib
from foundations_spec import *
from typing import List
from orbit_acceptance.mixins.contrib_path_mixin import ContribPathMixin

class TestOrbitDeployModelViaCli(Spec, ContribPathMixin):

    port = 31998
    max_time_out_in_sec = 60

    @set_up_class
    def set_up_class(self):
        from acceptance.cleanup import cleanup
        cleanup()

        subprocess.run(['./integration/resources/fixtures/test_server/spin_up.sh'], cwd=self.resolve_f9s_contrib(), stdout=subprocess.PIPE)

    @tear_down_class
    def tear_down_class(self):
        subprocess.run(['./integration/resources/fixtures/test_server/tear_down.sh'], cwd=self.resolve_f9s_contrib(), stdout=subprocess.PIPE)

    @set_up
    def set_up(self):
        self.config_file_path = './orbit_acceptance/fixtures/config/local.config.yaml'
        self._generate_yaml_config_file()

        self.base_url = f'http://{self._get_scheduler_ip()}:{self.port}/projects/{self.mock_project_name}/{self.mock_user_provided_model_name}/'

    @tear_down
    def tear_down(self):
        try:
            self._perform_tear_down_for_model_package(self.mock_project_name, self.mock_user_provided_model_name)
        except:
            print('Unable to remove model pacakge. Probably terminated in the test')

    @staticmethod
    def _is_running_on_jenkins():
        import os
        return os.environ.get('RUNNING_ON_CI', 'FALSE') == 'TRUE'

    @let
    def mock_project_name(self):
        return self.faker.word().lower()

    @let
    def mock_user_provided_model_name(self):
        return self.faker.word().lower()

    @let
    def project_directory(self):
        return './project_code/'

    def test_can_successfully_run_model_serve(self):
        try:
            self._deploy_default_job()

            result = self._check_if_endpoint_available()
            self.assertIsNotNone(result)
        except KeyboardInterrupt:
            self.fail('Interrupted by user')

    def test_can_successfully_stop_model_serve(self):
        try:
            import time
            # ensure deployed
            self._deploy_default_job()
            self.assertIsNotNone(self._check_if_endpoint_available())

            # stop and ensure that its unavailable
            self._stop_job(self.mock_project_name, self.mock_user_provided_model_name)
            self._wait_for_server_to_be_unavailable()
            self.assertIsNone(self._check_if_endpoint_available())
        except KeyboardInterrupt:
            self.fail('Interrupted by user')

    def test_can_retrieve_the_entrypoints_of_deployed_model_from_rest_api(self):
        import redis
        import foundations_contrib.global_state as global_state

        old_redis = global_state.redis_connection
        global_state.redis_connection = redis.Redis.from_url(self._get_redis_ip())

        try:
            from foundations_orbit_rest_api.v1.models.model import Model

            self._deploy_default_job()

            expected_entrypoint = {
                'predict': {'module': 'src.main', 'function': 'predict'},
                'recalibrate': {'module': 'src.main', 'function': 'train'},
                'evaluate': {'module': 'src.main', 'function': 'evaluate'}
            }

            models_promise = Model.all(project_name=self.mock_project_name)

            models = models_promise.evaluate()
            for model in models:
                if model.model_name == self.mock_user_provided_model_name():
                    self.assertEqual(expected_entrypoint, model.entrypoints)
                    return
            
            self.fail('Failed to find entrypoint (model name not found)')
        except KeyboardInterrupt:
            self.fail('Interrupted by user')
        finally:
            global_state.redis = old_redis

    def _deploy_default_job(self):
        self._deploy_job(self.mock_project_name, self.mock_user_provided_model_name)
        self._wait_for_server_to_be_available()

    def test_can_successfully_resume_model_serve(self):
        try:
            import time
            # ensure deployed
            self._deploy_default_job()
            self.assertIsNotNone(self._check_if_endpoint_available())

            # stop and ensure that its unavailable
            self._stop_job(self.mock_project_name, self.mock_user_provided_model_name)
            self._wait_for_server_to_be_unavailable()
            self._wait_for_deployment_pod_to_delete(f'foundations-model-package-{self.mock_project_name}-{self.mock_user_provided_model_name}')
            self.assertIsNone(self._check_if_endpoint_available())

            self._deploy_job(self.mock_project_name, self.mock_user_provided_model_name)
            self._wait_for_server_to_be_available()
            self.assertIsNotNone(self._check_if_endpoint_available())
        except KeyboardInterrupt:
            self.fail('Interrupted by user')

    def _deploy_job(self, project_name, model_name):
        import subprocess

        command_to_run = [
            'python', '-m', 
            'foundations',
            'orbit',
            'serve', 
            'start',
            '--project_name={}'.format(project_name),
            '--model_name={}'.format(model_name),
            '--project_directory={}'.format(self.project_directory)
        ]

        process_result = subprocess.run(command_to_run, cwd='./orbit_acceptance/fixtures/', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self._check_if_process_successful(process_result)

    def _stop_job(self, project_name, model_name):
        import subprocess

        command_to_run = [
            'python', '-m', 
            'foundations',
            'orbit',
            'serve', 
            'stop',
            '--project_name={}'.format(project_name),
            '--model_name={}'.format(model_name),
        ]

        process_result = subprocess.run(command_to_run, cwd='./orbit_acceptance/fixtures/', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self._check_if_process_successful(process_result)

    def _get_scheduler_ip(self):
        import os

        if 'FOUNDATIONS_SCHEDULER_HOST' not in os.environ:
            raise RuntimeError('please set FOUNDATIONS_SCHEDULER_HOST env var')

        return os.environ['FOUNDATIONS_SCHEDULER_HOST']

    def _get_redis_ip(self):
        import os

        if not self._is_running_on_jenkins():
            return f'redis://{self._get_scheduler_ip()}:6379'

        return os.environ['FOUNDATIONS_SCHEDULER_ACCEPTANCE_REDIS_PROXY']

    def _wait_for_server_to_be_available(self):
        import time

        start_time = time.time()
        while time.time() - start_time < self.max_time_out_in_sec:
            try:
                requests.get(self.base_url, timeout=0.1).json()
                return
            except Exception as e:
                time.sleep(1)
        self.fail('server never started')

    def _wait_for_server_to_be_unavailable(self):
        import time

        start_time = time.time()
        while time.time() - start_time < 6:
            try:
                requests.get(self.base_url,  timeout=0.01).json()
                time.sleep(1)
            except:
                return
        self.fail('server failed to stop')

    def _check_if_error_exists(self, cli_deploy_process):
        return cli_deploy_process.returncode != 0

    def _check_if_process_successful(self, cli_deploy_process):
        if self._check_if_error_exists(cli_deploy_process):
            raise AssertionError(f'deploy failed:\nstdout:\n{cli_deploy_process.stdout.decode()}\nstderr:\n{cli_deploy_process.stderr.decode()}')

    def _check_if_unsuccessful(self, cli_deploy_process):
        if not self._check_if_error_exists(cli_deploy_process):
            raise AssertionError('deploy succeeded when it should have failed')

    def _check_if_endpoint_available(self):
        end_point_url = f'{self.base_url}predict'
        try:
            result = requests.post(end_point_url, json={'a': 20, 'b': 30}).json()
            return result
        except Exception as e:
            return None

    def _generate_yaml_config_file(self):
        import yaml

        config_yaml = yaml.dump({
            'job_deployment_env': 'scheduler_plugin', 
            'results_config': {
                'archive_end_point': '/archive',
                'redis_end_point': self._get_redis_ip(),
                'artifact_path': 'artifacts'
            },
            'cache_config': {
                'end_point': '/cache'
            },
            'ssh_config': {
                'host': self._get_scheduler_ip(),
                'port': 31222,
                'code_path': '/jobs',
                'result_path': '/jobs',
                'key_path': '~/.ssh/id_foundations_scheduler',
                'user': 'job-uploader'
            },
            'obfuscate_foundations': False,
            'enable_stages': False
        })
        with open(self.config_file_path, 'w+') as file:
            file.write(config_yaml)

    def _wait_for_deployment_pod_to_delete(self, deployment):
        import subprocess

        import time

        start_time = time.time()
        while time.time() - start_time < 60:
            if self._deployment_pods(deployment) == []:
                return
            time.sleep(2)

        self.fail('deployment pod failed to stop')

    def _deployment_pods(self, deployment):
        import subprocess
        import yaml
        import shlex

        process = subprocess.run(shlex.split(f'kubectl -n foundations-scheduler-test get pods -l app={deployment} -o yaml'), stdout=subprocess.PIPE)
        yaml_output = yaml.load(process.stdout.decode())
        return yaml_output['items']

    def _perform_tear_down_for_model_package(self, project_name, model_name):
        import subprocess
        import shlex
        subprocess.run(shlex.split(f'kubectl -n foundations-scheduler-test delete deployment foundations-model-package-{project_name}-{model_name}-deployment'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(shlex.split(f'kubectl -n foundations-scheduler-test delete svc foundations-model-package-{project_name}-{model_name}-service'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # subprocess.run(shlex.split('kubectl -n foundations-scheduler-test delete configmap model-package-submission-config'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)