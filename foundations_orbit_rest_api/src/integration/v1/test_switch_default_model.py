"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""
import json
import foundations_contrib
from foundations_spec import *
from foundations_orbit_rest_api.global_state import app_manager
from foundations_spec.extensions import run_process

class TestSwitchDefaultModel(Spec):
    client = app_manager.app().test_client()
    base_url = '/api/v1/projects'
    project_name = 'test-project'
    
    @set_up_class
    def set_up_class(self):
        run_process(['./integration/resources/fixtures/test_server/spin_up.sh'], foundations_contrib.root() / '..')

    @tear_down_class
    def tear_down_class(self):
        run_process(['./integration/resources/fixtures/test_server/tear_down.sh'], foundations_contrib.root() / '..')
        run_process(f'./remove_deployment.sh {self.project_name} model'.split(), foundations_contrib.root() / 'resources/model_serving/orbit')
        run_process(f'./remove_deployment.sh {self.project_name} again-model'.split(), foundations_contrib.root() / 'resources/model_serving/orbit')

    @let
    def redis(self):
        from foundations_contrib.global_state import redis_connection
        return redis_connection

    @let
    def first_model_name(self):
        return self.faker.word()

    @let
    def second_model_name(self):
        return self.faker.word()

    @let
    def project_url(self):
        return f'{self.base_url}/{self.project_name}'

    @let
    def namespace(self):
        return 'foundations-scheduler-test'

    @let
    def redis(self):
        from foundations_contrib.global_state import redis_connection
        return redis_connection

    @let
    def model_information(self):
        return {
            'status': 'activated',
            'default': True,
            'created_by': 'Alan',
            'created_at': '2020-09-22T12:42:31Z',
            'description': 'this is a model...',
            'entrypoints': {
                'inference': {'module': 'src.main', 'function': 'predict'},
                'recalibrate': {'module': 'src.main', 'function': 'train'},
                'evaluation': {'module': 'src.main', 'function': 'eval'}
            },
            'validation_metrics': {
                'roc-auc': 0.7,
                'accuracy': 0.9
            }
        }

    @let
    def model_again_information(self):
        return {
            'status': 'deactivated',
            'default': False,
            'created_by': 'Sam',
            'created_at': '2019-01-22T12:42:31Z',
            'description': None,
            'entrypoints': {
                'inference': {'module': 'dev.main', 'function': 'predict_this'},
                'recalibrate': {'module': 'dev.main', 'function': 'train_that'},
                'evaluation': {'module': 'dev.main', 'function': 'eval_me'}
            },
            'validation_metrics': {
                'accuracy': 0.6,
                'mse': 77
            }
        }

    @set_up
    def set_up(self):
        self.redis.flushall()

    def test_put_request_changes_default_model(self):
        self._create_two_models_and_change_default()

        # check with redis that change was completed successfully
        response = self._get_from_route()
        models = response['models']
        for model in models:
            if model['model_name'] == 'model':
                first_model_default = model['default']
            if model['model_name'] == 'again-model':
                again_model_default = model['default']

        self.assertEqual(True, again_model_default)
        self.assertEqual(False, first_model_default)

    def test_put_request_change_default_model_in_the_ingress(self):
        import yaml, json
        

        self._create_two_models_and_change_default()

        ingress_resource = yaml.load(run_process(f'kubectl get ingress model-service-selection -n {self.namespace} -o yaml'.split(), '.'))
        ingress_configuration = ingress_resource['metadata']['annotations']['kubectl.kubernetes.io/last-applied-configuration'].strip('\n')
        ingress_resource = json.loads(ingress_configuration)
        ingress_resource_paths = ingress_resource['spec']['rules'][0]['http']['paths']

        for route in ingress_resource_paths:
            if route['path'] == f'/projects/{self.project_name}/(.*)':
                self.assertEqual(route['backend']['serviceName'], f'foundations-model-package-{self.project_name}-again-model-service')
                return

        self.fail()

    def _create_project(self, project_name):
        import time
        self.redis.execute_command('ZADD', 'projects', 'NX', time.time(), project_name)

    def _create_model_information(self, project_name, model_name, model_information):
        import pickle

        hash_map_key = f'projects:{project_name}:model_listing'
        serialized_model_information = pickle.dumps(model_information)
        self.redis.hmset(hash_map_key, {model_name: serialized_model_information})
        
        self._deploy_model(project_name, model_name)

    def _deploy_model(self, project_name, model_name):
        run_process(f'./integration/resources/fixtures/test_server/setup_test_server.sh {self.namespace} {project_name} {model_name}'.split(), foundations_contrib.root() / '..')

    def _put_to_route(self, body):
        response = self.client.put(self.project_url, data=body) # TODO NEED TO GET JSON=BODY TO WORK AS WELL
        response_data = response.data.decode()
        return json.loads(response_data)

    def _get_from_route(self):
        url = f'{self.project_url}/model_listing'
        response = self.client.get(url)
        response_data = response.data.decode()
        return json.loads(response_data)
    
    def _create_two_models_and_change_default(self):
        self._create_project(self.project_name)

        self._create_model_information(self.project_name, 'model', self.model_information)
        self._create_model_information(self.project_name, 'again-model', self.model_again_information)

        request_body = {'default_model': 'again-model'}
        self._put_to_route(request_body)