"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
import foundations

class TestCanDeployModelServer(Spec):

    @set_up
    def set_up(self):
        import yaml

        config_path = 'integration/fixtures/model-server/config/local.config.yaml'
        config_yaml = yaml.dump({
            'job_deployment_env': 'local', 
            'results_config': {
                'artifact_path': '.',
                'redis_end_point': f'redis://{self._get_current_ip()}:6379',
            },
            'cache_config': {},
            'obfuscate_foundations': False,
            'enable_stages': False,
        })
        with open(config_path, 'w+') as file:
            file.write(config_yaml)

        # ensure deployment set
        self.deployment

    @tear_down
    def tear_down(self):
        import subprocess

        subprocess.call(['docker', 'stop', self.integration_test_container_name])
        subprocess.call(['docker', 'rm', self.integration_test_container_name])

    @let
    def integration_test_container_name(self):
        return 'foundations-integration-test-model-server'

    @let
    def deployment(self):
        import foundations
        return foundations.deploy(project_name='test', env='local', entrypoint='project_code.driver', job_directory='integration/fixtures/model-server', params=None)

    @let
    def job_id(self):
        return self.deployment.job_name()

    @let
    def foundations_job_data_path(self):
        import os.path
        return os.path.expanduser('~/.foundations/job_data')

    def test_can_deploy_server(self):
        import subprocess
        from foundations_contrib.global_state import redis_connection

        subprocess.call(['bash', '-c', 'cd src && ./build.sh'])
        docker_process_return_code = subprocess.call([
            'docker', 
            'run',
            '-p', '31333:80',
            '-d',
            '--name', self.integration_test_container_name, 
            '-v', f'{self.foundations_job_data_path}:/archive', 
            '-e', f'JOB_ID={self.job_id}', 
            'docker.shehanigans.net/foundations-model-package'
        ])

        if docker_process_return_code != 0:
            self.fail('docker process for model package failed')

        self._wait_for_server()
        result = self._try_post()

        self.assertEqual({'a': 2, 'b': 4}, result)
        self.assertEqual('1', redis_connection.get(f'models:{self.job_id}:served').decode())

    def _wait_for_server(self):
        import subprocess
        import requests
        import time

        start_time = time.time()

        while time.time() - start_time < 15:
            try:
                requests.get('http://localhost:31333')
                return
            except:
                time.sleep(0.200)

        container_logs_process = subprocess.run(['docker', 'logs', self.integration_test_container_name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        container_logs = container_logs_process.stdout.decode()

        self.fail(f'server never started:\n{container_logs}')

    def _try_post(self):
        import requests

        try:
            return requests.post('http://localhost:31333', json={'a': 1, 'b': 2}).json()
        except:
            return None

    def _get_current_ip(self):
        from foundations_spec.extensions import get_network_address
        return get_network_address('enp3s0')
