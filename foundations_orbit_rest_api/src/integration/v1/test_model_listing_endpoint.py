"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

from foundations_spec import *

from foundations_orbit_rest_api.global_state import app_manager

@skip('not implemented')
class TestModelListingEndpoint(Spec):
    client = app_manager.app().test_client()
    url = '/api/v1/projects/test_project/model_listing'

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

        self._create_project('test_project')

        self._create_model_information('model', self.model_information)
        self._create_model_information('model_again', self.model_again_information)

    def _create_project(self, project_name):
        import time
        self.redis.execute_command('ZADD', 'projects', 'NX', time.time(), project_name)

    def _create_model_information(self, model_name, model_information):
        import pickle

        hash_map_key = 'projects:test_project:model_listing'
        serialized_model_information = pickle.dumps(model_information)
        self.redis.hmset(hash_map_key, {model_name: serialized_model_information})

    def _get_from_route(self):
        import json

        response = self.client.get(self.url)
        response_data = response.data.decode()
        return json.loads(response_data)

    def test_get_model_listing(self):
        data = self._get_from_route()

        self.assertEqual('test_project', data['name'])

        models = data['models']
        model_again = models[0]
        model = models[1]

        self.assertEqual('model_again', model_again['model_name'])
        self._assert_is_subset(self.model_again_information, model_again)

        self.assertEqual('model', model['model_name'])
        self._assert_is_subset(self.model_information, model)

    def _assert_is_subset(self, subset, superset):
        for key in subset:
            self.assertEqual(subset[key], superset[key])

    def _assert_project_in(self, project_name, projects):
        for project in projects:
            if project['name'] == project_name:
                return

        raise AssertionError(f'no project with name \'{project_name}\' exists in {projects}')