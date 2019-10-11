"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

from foundations_spec import *

from foundations_orbit_rest_api.global_state import app_manager

class TestRetrieveValidationReportEndpoint(Spec):
    client = app_manager.app().test_client()
    url = '/api/v1/projects/test_project/validation_results'

    @let
    def redis(self):
        from foundations_contrib.global_state import redis_connection
        return redis_connection

    @set_up
    def set_up(self):
        self.redis.flushall()

    def _post_response_from_route(self, data):
        return self.client.post(self.url, json=data)

    def _post_data_from_response(self, response):
        import json

        response_data = response.data.decode()
        return json.loads(response_data)

    def _post_status_code_from_response(self, response):
        return response.status_code

    def test_retrieve_validation_report_gives_a_404_if_not_exists(self):
        post_data = {
            'inference_period': '2019-05-01',
            'monitor_package': 'model_abcdefg',
            'data_contract': 'data_contract_1'
        }

        expected_response_data = {
            'inference_period': '2019-05-01',
            'monitor_package': 'model_abcdefg',
            'data_contract': 'data_contract_1',
            'error': 'does not exist'
        }

        response = self._post_response_from_route(data=post_data)

        self.assertEqual(404, self._post_status_code_from_response(response))
        self.assertEqual(expected_response_data, self._post_data_from_response(response))

    def test_retrieve_validation_report_returns_report_if_exists_in_redis(self):
        import pickle

        post_data = {
            'inference_period': '2019-05-01',
            'monitor_package': 'model_abcdefg',
            'data_contract': 'data_contract_1'
        }

        expected_response_data = {
            'schema_check': True,
            'schema_information': {
                'rows': 10
            }
        }

        self.redis.hset(f'projects:test_project:monitors:model_abcdefg:validation:data_contract_1', '2019-05-01', pickle.dumps(expected_response_data))

        response = self._post_response_from_route(data=post_data)

        self.assertEqual(200, self._post_status_code_from_response(response))
        self.assertEqual(expected_response_data, self._post_data_from_response(response))