"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

from foundations_spec import *

from foundations_orbit_rest_api.global_state import app_manager

class TestRetrieveValidationReportListingEndpoint(Spec):
    client = app_manager.app().test_client()
    url = '/api/v1/projects/test_project/validation_report_list'

    @let
    def redis(self):
        from foundations_contrib.global_state import redis_connection
        return redis_connection

    @set_up
    def set_up(self):
        self.redis.flushall()

    def _get_from_route(self):
        import json

        response = self.client.get(self.url)
        response_data = response.data.decode()
        return json.loads(response_data)

    @skip
    def test_retrieve_validation_report_listing_gets_stored_metrics_from_redis(self):
        expected_data = [
            {
                'inference_period': '2019-02-01',
                'model_package': 'model_one',
                'data_contract': 'data_contract_1'
            },
            {
                'inference_period': '2019-02-01',
                'model_package': 'model_one',
                'data_contract': 'data_contract_2'
            },
            {
                'inference_period': '2019-02-05',
                'model_package': 'model_one',
                'data_contract': 'data_contract_1'
            },
            {
                'inference_period': '2019-02-05',
                'model_package': 'model_one',
                'data_contract': 'data_contract_2'
            },
            {
                'inference_period': '2019-02-02',
                'model_package': 'model_two',
                'data_contract': 'data_contract_1'
            },
            {
                'inference_period': '2019-02-02',
                'model_package': 'model_two',
                'data_contract': 'data_contract_2'
            }
        ]

        for listing_entry in expected_data:
            contract_name = listing_entry['data_contract']
            inference_period = listing_entry['inference_period']
            model_name = listing_entry['model_package']
            self.redis.hmset(f'projects:test_project:models:{model_name}:validation:{contract_name}', {inference_period: 'dummy'})

        data = self._get_from_route()
        self._sort_series_entries(data)

        self.assertEqual(expected_data, data)

    def _sort_series_entries(self, data_from_route):
        for metric_set in data_from_route:
            metric_set['series'].sort(key=lambda series_entry: series_entry['name'])