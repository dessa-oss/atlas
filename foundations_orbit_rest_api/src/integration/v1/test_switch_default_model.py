"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

from foundations_spec import *
from foundations_orbit_rest_api.global_state import app_manager

@skip('not implemented')
class TestSwitchDefaultModel(Spec):
    client = app_manager.app().test_client()
    base_url = '/api/v1/projects/'

    @let
    def redis(self):
        from foundations_contrib.global_state import redis_connection
        return redis_connection

    @let 
    def project_name(self):
        return 'test_project'

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

    @tear_down
    def tear_down(self):
        import os

    def test_put_request_changes_default_model(self):
        # create at least two models (manually)
        self._create_project('test_project')

        self._create_model_information('model', self.model_information)
        self._create_model_information('again_model', self.model_again_information)

        # perform the put request with the details of the change
        request_body = {'default_model': 'again_model'}
        self._put_to_route(request_body)

        # check with redis that change was completed successfully
        models = self._get_from_route()
        again_model = models[0]
        again_model_default = again_model['default']
        model = models[1]
        model_default = model['default']
        
        self.assertEqual(True, again_model_default)
        self.assertEqual(False, model_default)

    def _create_project(self, project_name):
        import time
        self.redis.execute_command('ZADD', 'projects', 'NX', time.time(), project_name)

    def _create_model_information(self, model_name, model_information):
        import pickle

        hash_map_key = 'projects:test_project:model_listing'
        serialized_model_information = pickle.dumps(model_information)
        self.redis.hmset(hash_map_key, {model_name: serialized_model_information})

    def _put_to_route(self, body):
        import json

        response = self.client.put(self.project_url, json=body)
        response_data = response.data.decode()
        return json.loads(response_data)

    def _get_from_route(self):
        import json

        url = f'{self.project_url}/model_listing'

        response = self.client.get(url)
        response_data = response.data.decode()
        return json.loads(response_data)