"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import time
import yaml
import subprocess
import os.path as path

class DeployModelMixin(object):

    sleep_time = 2
    max_sleep_time = 60
    port = 5000

    def _set_up_environment(self):
        from foundations_contrib.global_state import config_manager, redis_connection

        self._proxy_process = None
        self.deployment = None

        if self._is_running_on_jenkins():
            config_manager.config()['redis_url'] = self._get_proxy_url()

        self.redis_connection = redis_connection

    def _apply_environment_yaml(self):
        yaml_template_path = path.realpath('../../foundations_contrib/src/foundations_contrib/resources/model_serving/model-serving-environment.yaml')
        command_to_run = f'kubectl apply -f {yaml_template_path}'
        subprocess.call(['bash', '-c', command_to_run])

    def _tear_down_environment(self, project_name, models):
        from foundations_contrib.global_state import config_manager

        self._tear_down_proxy()

        for model in models:
            self._tear_down_model_package(project_name, model, self.job_id)

        config_manager.reset()

    def _tear_down_proxy(self):
        if self._proxy_process is not None:
            self._proxy_process.terminate()

    def _set_up_in_test(self, job_directory):
        self._generate_yaml_config_file(job_directory)

        self._deploy_job(job_directory)
        self.deployment.wait_for_deployment_to_complete()
        self._spin_up_model_package_and_proxy(self.project_name, self.model_name)
        
    def _spin_up_model_package_and_proxy(self, project_name, model_name):
        self._deploy_model_package(project_name, model_name, self.job_id)
        self._proxy_process = subprocess.Popen(['bash', '-c', f'kubectl -n foundations-scheduler-test port-forward service/foundations-model-package-{self.project_name}-{self.model_name}-service {self.port}:80'])

        self._wait_for_server(self.project_name, self.model_name)

    def _deploy_job(self, job_directory):
        import foundations

        if self.deployment is None:
            foundations.set_job_resources(num_gpus=0)
            self.deployment = foundations.submit(project_name=self.project_name, entrypoint='project_code/driver.py', job_dir=f'integration/fixtures/{job_directory}', params=None)
        return self.deployment

    def _deploy_model_package(self, project_name, model_name, job_id):
        self._peform_action_for_creating_config_map('apply')
        self._perform_action_for_model_package(project_name, model_name, job_id, 'create')
        self._wait_for_model_package_pod(project_name, model_name)

    def _tear_down_model_package(self, project_name, model_name, job_id):
        self._perform_action_for_model_package(project_name, model_name, job_id, 'delete')
        # self._peform_action_for_creating_config_map('delete')
        self._wait_for_serving_pod_to_die(project_name, model_name)

    def _peform_action_for_creating_config_map(self, action):
        yaml_template_path = path.realpath('../../foundations_contrib/src/foundations_contrib/resources/model_serving/submission_config.yaml')
        command_to_run = f'FOUNDATIONS_SCHEDULER_HOST={self._get_scheduler_ip()} envsubst < {yaml_template_path} | kubectl {action} -f -'
        subprocess.call(['bash', '-c', command_to_run])

    def _perform_action_for_model_package(self, project_name, model_name, job_id, action):
        yaml_template_path = path.realpath('../../foundations_contrib/src/foundations_contrib/resources/model_serving/kubernetes-deployment.envsubst.yaml')
        command_to_run = f'foundations_version={self._image_version()} job_id={job_id} model_name={model_name} project_name={project_name} namespace=foundations-scheduler-test envsubst < {yaml_template_path} | kubectl {action} -f -'
        subprocess.call(['bash', '-c', command_to_run])

    def _force_delete_pod(self, project_name, model_name):
        command_to_run = f'kubectl -n foundations-scheduler-test delete pod --force -l app=foundations-model-package-{project_name}-{model_name}'
        subprocess.call(['bash', '-c', command_to_run])

    def _wait_for_model_package_pod(self, project_name, model_name):
        current_time = time.time()

        while self._model_package_pod_status(project_name, model_name) != "'Running'":
            if time.time() - current_time > self.max_sleep_time:
                raise AssertionError(f'model package pod took too long to come up (> 60 sec), Last Status: {self._model_package_pod_status(project_name, model_name)}')

            time.sleep(self.sleep_time)
    
    def _model_package_pod_status(self, project_name, model_name):
        command_to_run = ['kubectl', '-n', 'foundations-scheduler-test', 'get', 'pod', '-l', f'app=foundations-model-package-{project_name}-{model_name}', '-o', 'go-template=\'{{(index .items 0).status.phase}}\'']
        process = subprocess.run(command_to_run, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        if process.returncode != 0:
            return 'does not exist'
        return process.stdout.decode().rstrip('\n')

    def _wait_for_serving_pod_to_die(self, project_name, model_name):
        current_time = time.time()

        while self._pod_exists(project_name, model_name):
            if time.time() - current_time > self.max_sleep_time:
                self._force_delete_pod(project_name, model_name)
                break

            time.sleep(self.sleep_time)

    def _pod_exists(self, project_name, model_name):
        process = subprocess.run(['bash', '-c', f'kubectl -n foundations-scheduler-test get pod -l app=foundations-model-package-{project_name}-{model_name} -o yaml'], stdout=subprocess.PIPE)
        pod_list_payload = yaml.load(process.stdout)
        return pod_list_payload['items'] != []

    def _wait_for_server(self, project_name, model_name):
        import subprocess
        import requests
        import time

        start_time = time.time()

        while time.time() - start_time < self.max_sleep_time:
            try:
                requests.get(f'http://localhost:{self.port}')
                return
            except:
                time.sleep(self.sleep_time)

        process = subprocess.run(['kubectl', '-n', 'foundations-scheduler-test', 'logs', '-l', f'app=foundations-model-package-{project_name}-{model_name}'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        process_logs = process.stdout.decode().rstrip('\n')
        self.fail(f'server never started:\n{process_logs}')

    def _generate_yaml_config_file(self, job_directory, config_file='scheduler'):
        config_path = f'integration/fixtures/{job_directory}/config/{config_file}.config.yaml'
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

    def _get_proxy_url(self):
        import os

        if 'FOUNDATIONS_SCHEDULER_ACCEPTANCE_REDIS_PROXY' not in os.environ:
            raise RuntimeError('please set FOUNDATIONS_SCHEDULER_ACCEPTANCE_REDIS_PROXY env variable')

        return os.environ['FOUNDATIONS_SCHEDULER_ACCEPTANCE_REDIS_PROXY']

    def _image_version(self):
        import foundations_internal.versioning
        return foundations_internal.versioning.__version__.replace('+', '_')