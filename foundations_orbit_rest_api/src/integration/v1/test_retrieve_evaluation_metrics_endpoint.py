"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

from foundations_spec import *

from foundations_orbit_rest_api.global_state import app_manager

class TestRetrieveEvaluationMetricsEndpoint(Spec):
    client = app_manager.app().test_client()
    url = '/api/v1/projects/test_project/metrics'

    @let
    def redis(self):
        from foundations_contrib.global_state import redis_connection
        return redis_connection

    @set_up
    def set_up(self):
        self.redis.flushall()

    @tear_down
    def tear_down(self):
        import os
        os.environ.pop('MODEL_NAME')
        os.environ.pop('PROJECT_NAME')

    def _get_from_route(self):
        import json

        response = self.client.get(self.url)
        response_data = response.data.decode()
        return json.loads(response_data)

    def test_retrieve_evaluation_metrics_gets_stored_metrics_from_redis(self):
        import os
        from foundations_orbit import track_production_metrics

        os.environ['PROJECT_NAME'] = 'test_project'

        os.environ['MODEL_NAME'] = 'this_job'

        track_production_metrics('MSE', {
            '2019-02-01': 1.077,
            '2019-03-01': 1.074,
            '2019-04-01': 1.09,
            '2019-05-01': 1.086
        })

        track_production_metrics('Customer Response (%)', {
            '2029-02-02': 17.56,
            '2029-03-02': 17.57,
            '2029-04-02': 17.53,
            '2029-05-02': 17.43
        })

        os.environ['MODEL_NAME'] = 'that_job'

        track_production_metrics('MSE', {
            '2019-02-01': 2.077,
            '2019-03-01': 2.074,
            '2019-04-01': 2.09,
            '2019-05-01': 2.086
        })

        track_production_metrics('Customer Response (%)', {
            '2029-02-02': 27.56,
            '2029-03-02': 27.57,
            '2029-04-02': 27.53,
            '2029-05-02': 27.43
        })

        expected_data = [
            {
                'title': {'text': 'Customer Response (%) over time'},
                'yAxis': {'title': {'text': 'Customer Response (%)'}},
                'xAxis': {
                    'categories': ['2029-02-02', '2029-03-02', '2029-04-02', '2029-05-02']
                },
                'series': [
                    {
                        'data': [27.56, 27.57, 27.53, 27.43],
                        'name': 'that_job'
                    },
                    {
                        'data': [17.56, 17.57, 17.53, 17.43],
                        'name': 'this_job'
                    }
                ]
            },
            {
                'title': {'text': 'MSE over time'},
                'yAxis': {'title': {'text': 'MSE'}},
                'xAxis': {
                    'categories': ['2019-02-01', '2019-03-01', '2019-04-01', '2019-05-01']
                },
                'series': [
                    {
                        'data': [2.077, 2.074, 2.09, 2.086],
                        'name': 'that_job'
                    },
                    {
                        'data': [1.077, 1.074, 1.09, 1.086],
                        'name': 'this_job'
                    }
                ]
            }
        ]

        data = self._get_from_route()
        self.assertEqual(expected_data, data)