"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from scheduler_acceptance.mixins.metrics_fetcher import MetricsFetcher
from scheduler_acceptance.mixins.node_aware_mixin import NodeAwareMixin

class TestCliDeployment(Spec, MetricsFetcher, NodeAwareMixin):
    
    @let
    def cli_config(self):
        import os

        scheduler_host = os.environ.get('FOUNDATIONS_SCHEDULER_HOST', None)

        if scheduler_host is None:
            print("Please set the FOUNDATIONS_SCHEDULER_HOST environment variable to your LAN ip!")
            exit(1)

        if os.environ.get('RUNNING_ON_CI', 'FALSE') == 'TRUE':
            ssh_config_host = scheduler_host
            redis_url = os.environ.get('FOUNDATIONS_SCHEDULER_ACCEPTANCE_REDIS_URL', 'redis://{}:6379'.format(scheduler_host))
        else:
            from foundations_spec.extensions import get_network_address

            ssh_config_host = 'localhost'
            docker_address = get_network_address('docker0')
            redis_url = 'redis://{}:6379'.format(docker_address)

        return {
            'job_deployment_env': 'scheduler_plugin',
            'results_config': {
                'archive_end_point': '/archive',
                'artifacts_path': 'results',
                'redis_end_point': redis_url
            },
            'cache_config': {
                'end_point': '/cache'
            },
            'ssh_config': {
                'user': 'job-uploader',
                'host': ssh_config_host,
                'code_path': '/jobs',
                'result_path': '/jobs',
                'key_path': '~/.ssh/id_foundations_scheduler',
                'port': 31222
            },
            'log_level': 'INFO',
            'obfuscate_foundations': False
        }

    @let
    def yaml_cli_config(self):
        import yaml
        return yaml.dump(self.cli_config)
    
    @set_up
    def set_up(self):
        import shutil
        import os
        import os.path
        import uuid

        from scheduler_acceptance.cleanup import cleanup

        cleanup()

        shutil.rmtree("test-cli-init", ignore_errors=True)
        if os.path.isfile('~/.foundations/job_data/projects/my-foundations-project.tracker'):
            os.remove('~/.foundations/job_data/projects/my-foundations-project.tracker')

        self._env_name = str(uuid.uuid4())
        self._config_file_name = os.path.expanduser('~/.foundations/config/{}.config.yaml'.format(self._env_name))
        self._write_config_to_path(self._config_file_name)

    @set_up_class
    def set_up_class(klass):
        from foundations_scheduler_core.kubernetes_api_wrapper import KubernetesApiWrapper

        klass._core_api = KubernetesApiWrapper().core_api()

    @tear_down
    def tear_down(self):
        import os
        import os.path

        if os.path.isfile(self._config_file_name):
            os.remove(self._config_file_name)

    def test_cli_can_deploy_job_created_by_init(self):
        import subprocess

        subprocess.call(["python", "-m", "foundations", "init", "test-cli-init"])

        self._write_config_to_path('test-cli-init/config/scheduler.config.yaml')

        driver_deploy_result = subprocess.run(["/bin/bash", "-c", "cd test-cli-init && python -m foundations deploy --entrypoint=project_code/driver.py --env=scheduler"], stderr=subprocess.PIPE)
        self._assert_deployment_was_successful(driver_deploy_result)

    def test_cli_can_deploy_stageless_job_with_resources_set(self):
        import subprocess

        process = subprocess.run(['/bin/bash', '-c', 'cd scheduler_acceptance/fixtures/logging_resources_set && python -m foundations deploy --project-name=this-project --entrypoint=stages.py --env={} --num-gpus=0 --ram=3'.format(self._env_name)], stdout=subprocess.PIPE)
        job_id = self._job_id_from_logs(process)

        self._wait_for_job_to_complete(job_id)

        self.assertEqual(0, self._get_logged_metric('this-project', job_id, 'gpus'))
        self.assertEqual(3.0, self._get_logged_metric('this-project', job_id, 'memory'))

    def test_cli_can_deploy_stageless_job_with_resources_default(self):
        import subprocess

        process = subprocess.run(['/bin/bash', '-c', 'cd scheduler_acceptance/fixtures/logging_resources_default && python -m foundations deploy --project-name=this-project --entrypoint=stages.py --env={}'.format(self._env_name)], stdout=subprocess.PIPE)
        job_id = self._job_id_from_logs(process)

        self._wait_for_job_to_complete(job_id)

        node_name = self._get_node_for_job(job_id)
        memory_capacity = self._get_memory_capacity_for_node(node_name)

        ram_available_to_job = self._get_logged_metric('this-project', job_id, 'memory')
        ram_error = abs(memory_capacity - ram_available_to_job) / memory_capacity

        self.assertEqual(1, self._get_logged_metric('this-project', job_id, 'gpus'))
        self.assertLess(ram_error, 0.01)

    def test_deploy_does_not_print_crypto_warning(self):
        import subprocess

        process = subprocess.run(['/bin/bash', '-c', 'cd scheduler_acceptance/fixtures/logging_resources_set && python -m foundations deploy --project-name=this-project --entrypoint=stages.py --env={} --num-gpus=0 --ram=3'.format(self._env_name)], stderr=subprocess.PIPE)
        self.assertNotIn('CryptographyDeprecationWarning', process.stderr.decode())

    @skip('not implemented')
    def test_deploy_streams_to_console(self):
        import time
        from subprocess import PIPE, Popen

        process = Popen(['/bin/bash', '-c', 'cd scheduler_acceptance/fixtures/streaming_test && python -m foundations deploy --env={} --num-gpus=0 --ram=3'.format(self._env_name)], stdout=PIPE, encoding='ascii')
        process_stdout = process.stdout

        self._wait_for_job_to_start(process_stdout)

        time.sleep(8)
        process.terminate()

        rest_of_output = process_stdout.read().split('\n')
        rest_of_output = list(map(int, rest_of_output))

        self.assertEqual(1, rest_of_output[0])
        self.assertGreaterEqual(14, rest_of_output[-1])
        self.assertLessEqual(20, rest_of_output[-1])

        for index in range(len(rest_of_output) - 1):
            self.assertEqual(rest_of_output[index] + 1, rest_of_output[index + 1])

    def _job_id_from_logs(self, driver_deploy_completed_process):
        import re

        logs_parsing_regex = re.compile("Job '(.*)' deployed")
        logs = self._driver_stdout(driver_deploy_completed_process)
        return logs_parsing_regex.findall(logs)[0]

    def _driver_stdout(self, driver_deploy_completed_process):
        return driver_deploy_completed_process.stdout.decode()

    def _assert_deployment_was_successful(self, driver_deploy_result):
        if driver_deploy_result.returncode != 0:
            error_message = 'Driver deployment failed:\n{}'.format(driver_deploy_result.stderr.decode())
            raise AssertionError(error_message)

    def _write_config_to_path(self, path):
        with open(path, 'w+') as file:
            file.write(self.yaml_cli_config)

    def _wait_for_job_to_complete(self, job_id):
        self._wait_for_statuses(job_id, ['Pending', 'Running'], 'job did not finish')

    def _wait_for_job_to_start(self, job_process_stdout_stream):
        for line in job_process_stdout_stream:
            if line == 'JOB_STARTED_MARKER':
                return

        raise AssertionError('either job never started or job output never started streaming')

    def _wait_for_statuses(self, job_id, statuses, error_message):
        import time

        time_elapsed = 0
        timeout = 60

        while self._job_status(job_id) in statuses:
            if time_elapsed >= timeout:
                raise AssertionError(error_message)

            time_elapsed += 5
            time.sleep(5)

    def _job_status(self, job_id):
        from foundations_scheduler.pod_fetcher import get_latest_for_job

        pod = get_latest_for_job(self._core_api, job_id)

        if pod is None:
            return 'Pending'
        else:
            return pod.status.phase