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
        os.environ.pop('MONITOR_NAME')
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

        os.environ['MONITOR_NAME'] = 'this_job'

        track_production_metrics('MSE', {
            '2019-02-01 12:13:14': int(1),
            '2019-03-01 13:14:15': int(2),
            '2019-04-01 14:15:16': int(3),
            '2019-05-01 15:16:17': int(4)
        })

        track_production_metrics('Customer Response (%)', {
            '2029-02-02 16:17:18': float(17.56),
            '2029-03-02 18:19:20': float(17.57),
            '2029-04-02 19:20:21': float(17.53),
            '2029-05-02 20:21:22': float(17.43)
        })

        os.environ['MONITOR_NAME'] = 'that_job'

        track_production_metrics('MSE', {
            '2019-02-01 12:13:14': int(5),
            '2019-03-01 13:14:15': int(6),
            '2019-04-01 14:15:16': int(7),
            '2019-05-01 15:16:17': int(8)
        })

        track_production_metrics('Customer Response (%)', {
            '2029-02-02 16:17:18': float(27.56),
            '2029-03-02 18:19:20': float(27.57),
            '2029-04-02 19:20:21': float(27.53),
            '2029-05-02 20:21:22': float(27.43)
        })

        expected_data = [
            {
                'title': {'text': 'Customer Response (%) over time'},
                'yAxis': {'title': {'text': 'Customer Response (%)'}},
                'xAxis': {
                    'type': 'datetime'
                },
                'series': [
                    {
                        'data': [[_convert_date_string_to_timestamp('2029-02-02 16:17:18'), 27.56], [_convert_date_string_to_timestamp('2029-03-02 18:19:20'), 27.57], [_convert_date_string_to_timestamp('2029-04-02 19:20:21'), 27.53], [_convert_date_string_to_timestamp('2029-05-02 20:21:22'), 27.43]],
                        'name': 'that_job'
                    },
                    {
                        'data': [[_convert_date_string_to_timestamp('2029-02-02 16:17:18'), 17.56], [_convert_date_string_to_timestamp('2029-03-02 18:19:20'), 17.57], [_convert_date_string_to_timestamp('2029-04-02 19:20:21'), 17.53], [_convert_date_string_to_timestamp('2029-05-02 20:21:22'), 17.43]],
                        'name': 'this_job'
                    }
                ]
            },
            {
                'title': {'text': 'MSE over time'},
                'yAxis': {'title': {'text': 'MSE'}},
                'xAxis': {
                    'type': 'datetime'
                },
                'series': [
                    {
                        'data': [[_convert_date_string_to_timestamp('2019-02-01 12:13:14'), 5], [_convert_date_string_to_timestamp('2019-03-01 13:14:15'), 6], [_convert_date_string_to_timestamp('2019-04-01 14:15:16'), 7], [_convert_date_string_to_timestamp('2019-05-01 15:16:17'), 8]],
                        'name': 'that_job'
                    },
                    {
                        'data': [[_convert_date_string_to_timestamp('2019-02-01 12:13:14'), 1], [_convert_date_string_to_timestamp('2019-03-01 13:14:15'), 2], [_convert_date_string_to_timestamp('2019-04-01 14:15:16'), 3], [_convert_date_string_to_timestamp('2019-05-01 15:16:17'), 4]],
                        'name': 'this_job'
                    }
                ]
            }
        ]

        data = self._get_from_route()
        self._sort_series_entries(data)

        self.assertEqual(expected_data, data)

    def test_retrieve_evaluation_metrics_gets_stored_metrics_from_redis_numpy_data_types(self):
        import os
        import numpy
        from foundations_orbit import track_production_metrics

        os.environ['PROJECT_NAME'] = 'test_project'

        os.environ['MONITOR_NAME'] = 'this_job'

        track_production_metrics('MSE', {
            '2019-02-01 12:13:14': numpy.int8(1),
            '2019-03-01 13:14:15': numpy.int16(2),
            '2019-04-01 14:15:16': numpy.int32(3),
            '2019-05-01 15:16:17': numpy.int64(4)
        })

        track_production_metrics('Customer Response (%)', {
            '2029-02-02 16:17:18': numpy.float16(17.56),
            '2029-03-02 18:19:20': numpy.float16(17.57),
            '2029-04-02 19:20:21': numpy.float32(17.53),
            '2029-05-02 20:21:22': numpy.float64(17.43)
        })

        os.environ['MONITOR_NAME'] = 'that_job'

        track_production_metrics('MSE', {
            '2019-02-01 12:13:14': numpy.int8(5),
            '2019-03-01 13:14:15': numpy.int16(6),
            '2019-04-01 14:15:16': numpy.int32(7),
            '2019-05-01 15:16:17': numpy.int64(8)
        })

        track_production_metrics('Customer Response (%)', {
            '2029-02-02 16:17:18': numpy.float16(27.56),
            '2029-03-02 18:19:20': numpy.float16(27.57),
            '2029-04-02 19:20:21': numpy.float32(27.53),
            '2029-05-02 20:21:22': numpy.float64(27.43)
        })

        expected_data = [
            {
                'title': {'text': 'Customer Response (%) over time'},
                'yAxis': {'title': {'text': 'Customer Response (%)'}},
                'xAxis': {
                    'type': 'datetime'
                },
                'series': [
                    {
                        'data': [
                            [_convert_date_string_to_timestamp('2029-02-02 16:17:18'),_cast_to_float_like_and_then_back(27.56,numpy.float16)],
                            [_convert_date_string_to_timestamp('2029-03-02 18:19:20'), _cast_to_float_like_and_then_back(27.57, numpy.float16)],
                            [_convert_date_string_to_timestamp('2029-04-02 19:20:21'), _cast_to_float_like_and_then_back(27.53, numpy.float32)],
                            [_convert_date_string_to_timestamp('2029-05-02 20:21:22'), _cast_to_float_like_and_then_back(27.43, numpy.float64)]
                        ],
                        'name': 'that_job'
                    },
                    {
                        'data': [
                            [_convert_date_string_to_timestamp('2029-02-02 16:17:18'), _cast_to_float_like_and_then_back(17.56, numpy.float16)],
                            [_convert_date_string_to_timestamp('2029-03-02 18:19:20'), _cast_to_float_like_and_then_back(17.57, numpy.float16)],
                            [_convert_date_string_to_timestamp('2029-04-02 19:20:21'), _cast_to_float_like_and_then_back(17.53, numpy.float32)],
                            [_convert_date_string_to_timestamp('2029-05-02 20:21:22'), _cast_to_float_like_and_then_back(17.43, numpy.float64)]
                        ],
                        'name': 'this_job'
                    }
                ]
            },
            {
                'title': {'text': 'MSE over time'},
                'yAxis': {'title': {'text': 'MSE'}},
                'xAxis': {
                    'type': 'datetime'
                },
                'series': [
                    {
                        'data': [[_convert_date_string_to_timestamp('2019-02-01 12:13:14'), 5], [_convert_date_string_to_timestamp('2019-03-01 13:14:15'), 6], [_convert_date_string_to_timestamp('2019-04-01 14:15:16'), 7], [_convert_date_string_to_timestamp('2019-05-01 15:16:17'), 8]],
                        'name': 'that_job'
                    },
                    {
                        'data': [[_convert_date_string_to_timestamp('2019-02-01 12:13:14'), 1], [_convert_date_string_to_timestamp('2019-03-01 13:14:15'), 2], [_convert_date_string_to_timestamp('2019-04-01 14:15:16'), 3], [_convert_date_string_to_timestamp('2019-05-01 15:16:17'), 4]],
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

def _cast_to_float_like_and_then_back(value, float_like_class):
    return float(float_like_class(value))

def _convert_date_string_to_timestamp(date_string):
    from datetime import datetime
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").timestamp() * 1000