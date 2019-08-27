"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
import foundations

import threading

class TestCanDeployModelServer(Spec):

    @staticmethod
    def _is_running_on_jenkins():
        import os
        return os.environ.get('RUNNING_ON_CI', 'FALSE') == 'TRUE'

    @set_up_class
    def set_up_class(klass):
        import os
        import subprocess

        if not klass._is_running_on_jenkins():
            return_code = subprocess.call(['bash', '-c', 'cd src && ./build.sh'])

            if return_code != 0:
                raise AssertionError('docker build for model package failed :(')

    @set_up
    def set_up(self):
        from foundations_contrib.global_state import config_manager, redis_connection

        self._proxy_process = None
        self.deployment = None

        if self._is_running_on_jenkins():
            config_manager.config()['redis_url'] = self._get_redis_url()

        self.redis_connection = redis_connection
        self.redis_connection.flushall()

    def _set_up_in_test(self, job_directory):
        import subprocess

        self._generate_yaml_config_file(job_directory)

        self._deploy_job(job_directory)
        self.deployment.wait_for_deployment_to_complete()

        self._deploy_model_package('test-model-package', self.job_id)
        self._proxy_process = subprocess.Popen(['bash', '-c', 'kubectl -n foundations-scheduler-test port-forward service/foundations-model-package-test-model-package 5000:80'])

        self._wait_for_server('test-model-package')

    @tear_down
    def tear_down(self):
        from foundations_contrib.global_state import config_manager

        if self._proxy_process is not None:
            self._proxy_process.terminate()

        self._tear_down_model_package('test-model-package', self.job_id)

        config_manager.reset()

    @let
    def job_id(self):
        return self.deployment.job_name()

    def test_can_deploy_server(self):
        self._set_up_in_test('model-server')

        result = self._try_post_to_root_endpoint()
        predict_result = self._try_post_to_predict_endpoint()

        self.assertEqual({'a': 2, 'b': 4}, result)
        self.assertEqual({'a': 21, 'b': 32}, predict_result)

        self.assertEqual('1', self.redis_connection.get(f'models:{self.job_id}:served').decode())

    def test_can_hit_evaluate_endpoint(self):
        import time
        import pickle
        import os

        self._set_up_in_test('model-server-with-evaluate')

        self._try_post_to_evaluate_endpoint('october')
        time.sleep(5)
        self._try_post_to_evaluate_endpoint('january')
        time.sleep(5)

        production_metrics_from_redis = self.redis_connection.hgetall(f'models:{self.job_id}:production_metrics')
        production_metrics = {metric_name.decode(): pickle.loads(serialized_metrics) for metric_name, serialized_metrics in production_metrics_from_redis.items()}
        production_metrics['MSE'].sort(key=lambda entry: entry[0])

        expected_production_metrics = {
            'roc_auc': [('october', 66), ('january', 66)],
            'MSE': [('january', 1), ('january_again', 2), ('october', 1), ('october_again', 2)]
        }

        self.assertEqual(expected_production_metrics, production_metrics)

    def _generate_yaml_config_file(self, job_directory):
        import yaml

        config_path = f'integration/fixtures/{job_directory}/config/scheduler.config.yaml'
        config_yaml = yaml.dump({
            'log_level': 'DEBUG',
            'job_deployment_env': 'scheduler_plugin', 
            'results_config': {
                'archive_end_point': '/archive',
                'redis_end_point': self._get_redis_url(),
                'artifact_path': 'artifacts',
                'artifact_path': '.'
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
        with open(config_path, 'w+') as file:
            file.write(config_yaml)

    def _wait_for_model_package_pod(self, model_name):
        import time

        current_time = time.time()

        while self._model_package_pod_status(model_name) != 'Running':
            if time.time() - current_time > 30:
                raise AssertionError('model package pod took too long to come up (> 30 sec)')

            time.sleep(3)

    def _model_package_pod_status(self, model_name):
        import subprocess

        process = subprocess.run(['kubectl', '-n', 'foundations-scheduler-test', 'get', 'pod', '-l', f'app=foundations-model-package-{model_name}', '-o', 'go-template={{(index .items 0).status.phase}}'], stdout=subprocess.PIPE)
        return process.stdout.decode().rstrip('\n')

    def _wait_for_server(self, model_name):
        import subprocess
        import requests
        import time

        start_time = time.time()

        while time.time() - start_time < 15:
            try:
                requests.get('http://localhost:5000')
                return
            except:
                time.sleep(0.200)


        process = subprocess.run(['kubectl', '-n', 'foundations-scheduler-test', 'logs', '-l', f'app=foundations-model-package-{model_name}'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        process_logs = process.stdout.decode().rstrip('\n')
        self.fail(f'server never started:\n{process_logs}')

    def _try_post_to_root_endpoint(self):
        return self._try_post('/', {'a': 1, 'b': 2})

    def _try_post_to_predict_endpoint(self):
        return self._try_post('/predict', {'a': 20, 'b': 30})

    def _try_post_to_evaluate_endpoint(self, eval_period):
        response = self._try_post('/evaluate', {'eval_period': eval_period})

        if response is None:
            self.fail('post to /evaluate failed :(')

    def _try_post(self, endpoint, dict_payload):
        import requests

        try:
            return requests.post(f'http://localhost:5000{endpoint}', json=dict_payload).json()
        except:
            return None

    def _get_scheduler_ip(self):
        import os

        if 'FOUNDATIONS_SCHEDULER_HOST' not in os.environ:
            raise RuntimeError('please set FOUNDATIONS_SCHEDULER_HOST env variable')

        return os.environ['FOUNDATIONS_SCHEDULER_HOST']

    def _get_redis_url(self):
        import os

        if self._is_running_on_jenkins():
            return os.environ['FOUNDATIONS_SCHEDULER_ACCEPTANCE_REDIS_URL']
        else:
            return f'redis://{self._get_scheduler_ip()}:6379'
        
    def _deploy_job(self, job_directory):
        import foundations

        if self.deployment is None:
            foundations.set_job_resources(num_gpus=0)
            self.deployment = foundations.deploy(project_name='test', env='scheduler', entrypoint='project_code.driver', job_directory=f'integration/fixtures/{job_directory}', params=None)
        return self.deployment

    def _deploy_model_package(self, model_name, job_id):
        self._perform_action_for_model_package(model_name, job_id, 'create')
        self._wait_for_model_package_pod(model_name)

    def _tear_down_model_package(self, model_name, job_id):
        self._perform_action_for_model_package(model_name, job_id, 'delete')
        self._wait_for_serving_pod_to_die(model_name)

    def _perform_action_for_model_package(self, model_name, job_id, action):
        import os.path as path
        import subprocess

        yaml_template_path = path.realpath('../foundations_contrib/src/foundations_contrib/resources/model_serving/kubernetes-deployment.envsubst.yaml')
        command_to_run = f'job_id={job_id} model_name={model_name} envsubst < {yaml_template_path} | kubectl {action} -f -'
        subprocess.call(['bash', '-c', command_to_run])

    def _wait_for_serving_pod_to_die(self, model_name):
        import time

        current_time = time.time()

        while self._pod_exists(model_name):
            if time.time() - current_time > 60:
                raise AssertionError('model package pod took too long to go down (> 60 sec)')

            time.sleep(3)

    def _pod_exists(self, model_name):
        import subprocess
        import yaml

        process = subprocess.run(['bash', '-c', f'kubectl -n foundations-scheduler-test get pod -l app=foundations-model-package-{model_name} -o yaml'], stdout=subprocess.PIPE)
        pod_list_payload = yaml.load(process.stdout)
        return pod_list_payload['items'] != []