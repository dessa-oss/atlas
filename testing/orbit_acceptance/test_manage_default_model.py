"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


from foundations_spec import *
import requests
import subprocess
import foundations_contrib
from orbit_acceptance.mixins.contrib_path_mixin import ContribPathMixin
from faker import Faker

@skip('Not using K8s anymore')
class TestManageDefaultModel(Spec, ContribPathMixin):

    api_port = 8080
    
    port = 31998
    max_time_out_in_sec = 30

    faker = Faker()

    mock_model_name = faker.word().lower()
    mock_second_model_name = faker.word().lower()
    mock_project_name = faker.word().lower()

    @set_up_class
    def set_up_class(klass):
        from acceptance.cleanup import cleanup
        cleanup()

        subprocess.run(['./integration/resources/fixtures/test_server/spin_up.sh'], cwd=klass.resolve_f9s_contrib(), stdout=subprocess.PIPE)
        klass._flask_process = subprocess.Popen(f'python launch_rest_api.py {klass._get_redis_ip()} {klass.api_port} {klass._get_scheduler_ip()}'.split(), cwd='./orbit_acceptance/fixtures/rest_api/', stdout=subprocess.PIPE)
        
    
    @tear_down_class
    def tear_down_class(klass):
        if klass._flask_process is not None:
            klass._flask_process.terminate()
        subprocess.run(['./integration/resources/fixtures/test_server/tear_down.sh', klass.mock_project_name], cwd=klass.resolve_f9s_contrib(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @set_up
    def set_up(self):
        self.config_file_path = './orbit_acceptance/fixtures/config/local.config.yaml'
        self._generate_yaml_config_file()

    @tear_down
    def tear_down(self):
        self._perform_tear_down_for_model_package(self.mock_project_name, self.mock_model_name)
        self._perform_tear_down_for_model_package(self.mock_project_name, self.mock_second_model_name)

    @let
    def project_directory(self):
        return './project_code/'

    @let
    def base_url(self):
        return f'http://{self._get_scheduler_ip()}:{self.port}'

    @let
    def project_base_url(self):
        return f'{self.base_url}/projects/{self.mock_project_name}'

    @let
    def api_project_base_url(self):
        return f'http://{self._get_scheduler_ip()}:{self.api_port}/api/v1/projects/{self.mock_project_name}'

    def test_switch_default_model(self):
        try:
            self._deploy_job(self.mock_project_name, self.mock_model_name)
            self._wait_for_server_to_be_available(self.mock_model_name)
            
            self._deploy_job(self.mock_project_name, self.mock_second_model_name)
            self._wait_for_server_to_be_available(self.mock_second_model_name)
            
            response = requests.put(f'{self.api_project_base_url}', json={'default_model': self.mock_second_model_name})
            self.assertEqual(response.status_code, 200)

            expected_default_model = self._get_expected_default_model()
            self.assertEqual(self.mock_second_model_name, expected_default_model['model_name'])

        except KeyboardInterrupt:
            self.fail('Interrupted by user')

    def test_first_deployed_model_is_default(self):
        try:
            self._deploy_job(self.mock_project_name, self.mock_model_name)
            self._wait_for_server_to_be_available(self.mock_model_name)

            models = self._retrieve_model_listing_from_api()
            for model in models:
                if model['model_name'] == self.mock_model_name:
                    expected_default_model = model

            self.assertEqual(self.mock_model_name, expected_default_model['model_name'])
            self.assertEqual(True, expected_default_model['default'])

        except KeyboardInterrupt:
            self.fail('Interrupted by user')

    def _retrieve_model_listing_from_api(self):
        results = requests.get(f'{self.api_project_base_url}/model_listing').json()
        models = results['models']
        return models


    def _get_expected_default_model(self):
        models = self._retrieve_model_listing_from_api()
        for model in models:
            if model['default']:
                return model
    
    @staticmethod
    def _is_running_on_jenkins():
        import os
        return os.environ.get('RUNNING_ON_CI', 'FALSE') == 'TRUE'

    @staticmethod
    def _get_scheduler_ip():
        import os

        if 'FOUNDATIONS_SCHEDULER_HOST' not in os.environ:
            raise RuntimeError('please set FOUNDATIONS_SCHEDULER_HOST env var')

        return os.environ['FOUNDATIONS_SCHEDULER_HOST']

    @classmethod
    def _get_redis_ip(klass):
        import os

        if not klass._is_running_on_jenkins():
            return f'redis://{klass._get_scheduler_ip()}:6379'
        
        return os.environ['FOUNDATIONS_SCHEDULER_ACCEPTANCE_REDIS_PROXY']


    def _deploy_job(self, project_name, model_name):
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

    def _check_if_process_successful(self, cli_deploy_process):
        if self._check_if_error_exists(cli_deploy_process):
            raise AssertionError(f'deploy failed:\nstdout:\n{cli_deploy_process.stdout.decode()}\nstderr:\n{cli_deploy_process.stderr.decode()}')

    def _check_if_error_exists(self, cli_deploy_process):
        return cli_deploy_process.returncode != 0

    def _wait_for_server_to_be_available(self, model_name):
        import time

        start_time = time.time()
        while time.time() - start_time < self.max_time_out_in_sec:
            try:
                url = f'{self.project_base_url}/{model_name}/'
                requests.get(url, timeout=0.1).json()
                return
            except Exception as e:
                time.sleep(1)
        self.fail('server never started')

    

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

    def _wait_for_server_to_be_unavailable(self, project_name, model_name):
        import time
        base_url = f'http://{self._get_scheduler_ip()}:{self.port}/projects/{project_name}/{model_name}/'

        start_time = time.time()
        while time.time() - start_time < 6:
            try:
                requests.get(base_url,  timeout=0.01).json()
                time.sleep(1)
            except:
                return
        self.fail('server failed to stop')

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

        self._stop_job(project_name, model_name)
        subprocess.run(shlex.split(f'kubectl -n foundations-scheduler-test delete ingress foundations-model-package-{project_name}-ingress'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self._wait_for_server_to_be_unavailable(project_name, model_name)
        self._wait_for_deployment_pod_to_delete(f'foundations-model-package-{project_name}-{model_name}')
