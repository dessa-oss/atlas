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

    def test_retrieve_evaluation_metrics_gets_stored_metrics_from_redis_python_data_types(self):
        import os
        from foundations_orbit import track_production_metrics

        os.environ['PROJECT_NAME'] = 'test_project'

        os.environ['MODEL_NAME'] = 'this_job'

        track_production_metrics('MSE', {
            '2019-02-01': int(1),
            '2019-03-01': int(2),
            '2019-04-01': int(3),
            '2019-05-01': int(4)
        })

        track_production_metrics('Customer Response (%)', {
            '2029-02-02': float(17.56),
            '2029-03-02': float(17.57),
            '2029-04-02': float(17.53),
            '2029-05-02': float(17.43)
        })

        os.environ['MODEL_NAME'] = 'that_job'

        track_production_metrics('MSE', {
            '2019-02-01': int(5),
            '2019-03-01': int(6),
            '2019-04-01': int(7),
            '2019-05-01': int(8)
        })

        track_production_metrics('Customer Response (%)', {
            '2029-02-02': float(27.56),
            '2029-03-02': float(27.57),
            '2029-04-02': float(27.53),
            '2029-05-02': float(27.43)
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
                        'data': [5, 6, 7, 8],
                        'name': 'that_job'
                    },
                    {
                        'data': [1, 2, 3, 4],
                        'name': 'this_job'
                    }
                ]
            }
        ]

        data = self._get_from_route()
        self._sort_series_entries(data)

        self.assertEqual(expected_data, data)

    @skip('not implemented')
    def test_retrieve_evaluation_metrics_gets_stored_metrics_from_redis_numpy_data_types(self):
        import os
        import numpy
        from foundations_orbit import track_production_metrics

        os.environ['PROJECT_NAME'] = 'test_project'

        os.environ['MODEL_NAME'] = 'this_job'

        track_production_metrics('MSE', {
            '2019-02-01': numpy.int8(1),
            '2019-03-01': numpy.int16(2),
            '2019-04-01': numpy.int32(3),
            '2019-05-01': numpy.int64(4)
        })

        track_production_metrics('Customer Response (%)', {
            '2029-02-02': numpy.float16(17.56),
            '2029-03-02': numpy.float16(17.57),
            '2029-04-02': numpy.float32(17.53),
            '2029-05-02': numpy.float64(17.43)
        })

        os.environ['MODEL_NAME'] = 'that_job'

        track_production_metrics('MSE', {
            '2019-02-01': numpy.int8(5),
            '2019-03-01': numpy.int16(6),
            '2019-04-01': numpy.int32(7),
            '2019-05-01': numpy.int64(8)
        })

        track_production_metrics('Customer Response (%)', {
            '2029-02-02': numpy.float16(27.56),
            '2029-03-02': numpy.float16(27.57),
            '2029-04-02': numpy.float32(27.53),
            '2029-05-02': numpy.float64(27.43)
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
                        'data': [5, 6, 7, 8],
                        'name': 'that_job'
                    },
                    {
                        'data': [1, 2, 3, 4],
                        'name': 'this_job'
                    }
                ]
            }
        ]

        data = self._get_from_route()
        self._sort_series_entries(data)

        self.assertEqual(expected_data, data)

    def _sort_series_entries(self, data_from_route):
        for metric_set in data_from_route:
            metric_set['series'].sort(key=lambda series_entry: series_entry['name'])