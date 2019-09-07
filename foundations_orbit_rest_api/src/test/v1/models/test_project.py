"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestProject(Spec):

    mock_ingress_update_default_model = let_patch_mock('foundations_contrib.resources.model_serving.orbit.ingress_modifier.update_default_model_for_project')

    @let
    def model_name(self):
        return self.faker.word()

    @let
    def is_default(self):
        return False

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

    def _create_model_information(self, project_name, model_name, model_information):
        import pickle

        hash_map_key = f'projects:{self.project_name}:model_listing'
        serialized_model_information = pickle.dumps(model_information)
        self._redis.hmset(hash_map_key, {model_name: serialized_model_information})

    def test_set_default_model_request_change_to_ingress(self):
        self._call_set_default_model()
        self.mock_ingress_update_default_model.assert_called_with(self.project_name, self.model_name)

    def test_set_default_model_updates_info_in_redis(self):
        import pickle

        self._create_model_information(self.project_name, self.model_name, self.model_information)
        self._call_set_default_model()

        hash_map_key = f'projects:{self.project_name}:model_listing'
        model_listings = self._redis.hgetall(hash_map_key)
        decoded_results = {key.decode(): value for key, value in model_listings.items()}

        self.assertTrue(self.model_name in decoded_results)

        model_details = decoded_results[self.model_name]
        deserialized_model = pickle.loads(model_details)
        model_default_state = deserialized_model['default']

        self.assertEqual(True, model_default_state)

    def _call_set_default_model(self):
        from foundations_orbit_rest_api.v1.models.project import Project
        Project.set_default_model(self.project_name, self.model_name)