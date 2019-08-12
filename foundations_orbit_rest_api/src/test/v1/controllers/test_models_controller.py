"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

from foundations_spec import *

from foundations_orbit_rest_api.v1.controllers.models_controller import ModelsController

class TestModelsController(Spec):

    @let
    def model_name(self):
        return self.faker.word()

    @let
    def is_default(self):
        return self.faker.boolean()

    @let
    def activated_status(self):
        if self.faker.boolean():
            return 'activated'
        return 'deactivated'

    @let
    def created_by(self):
        return self.faker.first_name()

    @let
    def created_at(self):
        return str(self.faker.date_time_this_year())

    @let
    def description(self):
        return self.faker.sentence()

    @let
    def entrypoints(self):
        return self.faker.pydict()

    @let
    def validation_metrics(self):
        return self.faker.pydict()

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def model_information(self):
        return {
            'status': self.activated_status,
            'default': self.is_default,
            'created_by': self.created_by,
            'created_at': self.created_at,
            'description': self.description,
            'entrypoints': self.entrypoints,
            'validation_metrics': self.validation_metrics
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
        import fakeredis

        self._redis = self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())
        self._create_model_information(self.project_name, 'model', self.model_information)
        self._create_model_information(self.project_name, 'another_model', self.model_again_information)

    def test_index_returns_payload_for_models_in_redis(self):
        controller = ModelsController()
        controller.params = {'project_name': self.project_name}

        expected_results = {'name': self.project_name}

        expected_model = {'model_name': 'model'}
        expected_model.update(self.model_information)

        expected_another_model = {'model_name': 'another_model'}
        expected_another_model.update(self.model_again_information)

        expected_results['models'] = [expected_another_model, expected_model]

        self.assertEqual(expected_results, controller.index().as_json())

    def test_index_returns_resource_with_resource_name_models(self):
        controller = ModelsController()
        controller.params = {'project_name': self.project_name}

        result = controller.index()

        self.assertEqual('Models', result.resource_name())

    def _create_model_information(self, project_name, model_name, model_information):
        import pickle

        hash_map_key = f'projects:{self.project_name}:model_listing'
        serialized_model_information = pickle.dumps(model_information)
        self._redis.hmset(hash_map_key, {model_name: serialized_model_information})