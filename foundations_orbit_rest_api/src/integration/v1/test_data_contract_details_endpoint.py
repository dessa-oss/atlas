"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

from foundations_spec import *

from foundations_orbit_rest_api.global_state import app_manager

class TestDataContractDetailsEndpoint(Spec):
    client = app_manager.app().test_client()
    url = '/api/v1/contracts'

    @let
    def redis(self):
        from foundations_contrib.global_state import redis_connection
        return redis_connection
    
    @let
    def data_contract_uuid(self):
        return self.faker.uuid4()

    @let
    def data_contract_details(self):
        return {
            self.faker.word(): self.faker.random.random()
        }

    @set_up
    def set_up(self):
        self.redis.flushall()

    def _get_data_from_response(self, response):
        import json

        response_data = response.data.decode()
        return json.loads(response_data)

    def test_data_contract_details_returns_400_if_uuid_does_not_exist(self):
        expected_response_data = {
            'uuid': self.data_contract_uuid,
            'error': 'UUID does not exist'
        }

        response = self.client.get(f'{self.url}/{self.data_contract_uuid}')
        self.assertEqual(400, response.status_code)
        self.assertEqual(expected_response_data, self._get_data_from_response(response))
    
    def test_data_contract_details_returns_correct_details_if_uuid_exists(self):
        self.redis.set(f'contracts:{self.id}:info', str(self.data_contract_details))
        
        response = self.client.get(f'{self.url}/{self.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(self.data_contract_details), self._get_data_from_response(response))