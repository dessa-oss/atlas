"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_orbit_rest_api.v1.models.model import Model

class TestModel(Spec):

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

    @set_up
    def set_up(self):
        import fakeredis
        self._redis = self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())

    @tear_down
    def tear_down(self):
        self._redis.flushall()

    def _create_model_information(self, project_name, model_name, model_information):
        import pickle

        hash_map_key = f'projects:{self.project_name}:model_listing'
        serialized_model_information = pickle.dumps(model_information)
        self._redis.hmset(hash_map_key, {model_name: serialized_model_information})

    def test_has_model_name(self):
        model = Model(model_name=self.model_name)
        self.assertEqual(self.model_name, model.model_name)

    def test_has_default_status(self):
        model = Model(default=self.is_default)
        self.assertEqual(self.is_default, model.default)

    def test_has_activated_status(self):
        model = Model(status=self.activated_status)
        self.assertEqual(self.activated_status, model.status)

    def test_has_created_by(self):
        model = Model(created_by=self.created_by)
        self.assertEqual(self.created_by, model.created_by)
    
    def test_has_created_at(self):
        model = Model(created_at=self.created_at)
        self.assertEqual(self.created_at, model.created_at)

    def test_has_description(self):
        model = Model(description=self.description)
        self.assertEqual(self.description, model.description)

    def test_has_entrypoints(self):
        model = Model(entrypoints=self.entrypoints)
        self.assertEqual(self.entrypoints, model.entrypoints)

    def test_has_validation_metrics(self):
        model = Model(validation_metrics=self.validation_metrics)
        self.assertEqual(self.validation_metrics, model.validation_metrics)

    def test_get_all_for_project_returns_empty_list_when_nothing_in_redis(self):
        self.assertEqual({'name': self.project_name, 'models': []}, Model.all(project_name=self.project_name).evaluate())

    def test_get_all_for_project_returns_model_when_in_redis(self):
        self._create_model_information(self.project_name, self.model_name, self.model_information)
        
        expected_information = {'model_name': self.model_name}
        expected_information.update(self.model_information)

        model = Model(**expected_information)

        self.assertEqual({'name': self.project_name, 'models': [model]}, Model.all(project_name=self.project_name).evaluate())