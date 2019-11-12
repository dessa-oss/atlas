"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2019
"""

from foundations_spec import *

from foundations_orbit_rest_api.v1.controllers import DataContractDetailsController

class TestDataContractDetailsController(Spec):

    @let
    def data_contract_uuid(self):
        return self.faker.uuid4()

    @let
    def data_contract_info(self):
        return str({self.faker.word: self.faker.pydict()})

    @let
    def controller(self):
        return DataContractDetailsController()

    @let_now
    def redis_connection(self):
        import fakeredis
        return self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())

    def test_post_returns_404_if_uuid_not_in_redis(self):
        self.controller.params = {'uuid': self.data_contract_uuid}
        response = self.controller.index()
        self.assertEqual(400, response.status())

    def test_post_returns_error_dictionary_if_uuid_not_in_redis(self):
        self.controller.params = {'uuid': self.data_contract_uuid}
        response = self.controller.index()

        expected_error = {
            'uuid': self.data_contract_uuid,
            'error': 'UUID does not exist'
        }
        self.assertEqual(expected_error, response.as_json())

    def test_post_returns_report_if_report_in_redis(self):
        self.maxDiff = None
        self._register_info(self.data_contract_uuid)
        self.controller.params = {'uuid': self.data_contract_uuid}
        response = self.controller.index()

        self.assertEqual(200, response.status())
        self.assertEqual(self.data_contract_info, str(response.evaluate()))

    @staticmethod
    def _key_to_write(uuid):
        return f'contracts:{uuid}:info'

    def _register_info(self, uuid):
        import pickle

        key_to_write = self._key_to_write(uuid)
        
        self.redis_connection.set(f'{key_to_write}', self.data_contract_info)