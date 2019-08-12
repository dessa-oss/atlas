"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 12 2018
"""
import unittest
from mock import patch
from foundations_core_rest_api_components.filters.null_filter import NullFilter


class TestNullFilter(unittest.TestCase):

    class MockJobInfo(object):

        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    def test_start_time_is_null(self):
        from datetime import datetime

        params = {
            'start_time_isnull': 'true',
        }

        jobs_start_times = [
            datetime(2018, 8, 1, 10, 30, 0, 0, None),
            None,
            datetime(2018, 10, 10, 15, 30, 0, 0, None),
            None,
            datetime(2018, 12, 1, 10, 30, 0, 0, None),
        ]

        result = [self.MockJobInfo(job_id=index+1, start_time=start_time.isoformat() if start_time else None)
                  for index, start_time in enumerate(jobs_start_times)]

        null_filter = NullFilter()
        new_result = null_filter(result, params)

        self.assertEqual(len(new_result), 2)

        new_result_ids = [job.job_id for job in new_result]
        expected_new_result_ids = [2, 4]
        self.assertEqual(expected_new_result_ids, new_result_ids)

    def test_start_time_is_not_null(self):
        from datetime import datetime

        params = {
            'start_time_isnull': 'false',
        }

        jobs_start_times = [
            datetime(2018, 8, 1, 10, 30, 0, 0, None),
            None,
            datetime(2018, 10, 10, 15, 30, 0, 0, None),
            None,
            datetime(2018, 12, 1, 10, 30, 0, 0, None),
        ]

        result = [self.MockJobInfo(job_id=index+1, start_time=start_time.isoformat() if start_time else None)
                  for index, start_time in enumerate(jobs_start_times)]

        null_filter = NullFilter()
        new_result = null_filter(result, params)

        self.assertEqual(len(new_result), 3)

        new_result_ids = [job.job_id for job in new_result]
        expected_new_result_ids = [1, 3, 5]
        self.assertEqual(expected_new_result_ids, new_result_ids)

    def test_start_time_bad_filter_value(self):
        from datetime import datetime

        params = {
            'start_time_isnull': 'random',
        }

        jobs_start_times = [
            datetime(2018, 8, 1, 10, 30, 0, 0, None),
            None,
            datetime(2018, 10, 10, 15, 30, 0, 0, None),
            None,
            datetime(2018, 12, 1, 10, 30, 0, 0, None),
        ]

        result = [self.MockJobInfo(job_id=index+1, start_time=start_time.isoformat() if start_time else None)
                  for index, start_time in enumerate(jobs_start_times)]

        null_filter = NullFilter()
        new_result = null_filter(result, params)

        self.assertEqual(len(new_result), 5)

        new_result_ids = [job.job_id for job in new_result]
        expected_new_result_ids = [1, 2, 3, 4, 5]
        self.assertEqual(expected_new_result_ids, new_result_ids)

    def test_input_parameters_argument_is_null(self):
        params = {
            'argument1_isnull': 'true',
        }

        input_parameters_list = [
            [{'name': 'argument0', 'type': 'string', 'value': 'red leave'},
             {'name': 'argument1', 'type': 'number', 'value': '3.14'}],
            [{'name': 'argument0', 'type': 'string', 'value': 'green grass'},
             {'name': 'argument1', 'type': 'number', 'value': None}],
            [{'name': 'argument0', 'type': 'string', 'value': 'more stuff'},
             {'name': 'argument1', 'type': 'number', 'value': float('nan')}]
        ]
        result = [self.MockJobInfo(job_id=index+1, input_params=input_parameters)
                  for index, input_parameters in enumerate(input_parameters_list)]

        null_filter = NullFilter()
        new_result = null_filter(result, params)

        self.assertEqual(len(new_result), 2)

        new_result_job_ids = [job.job_id for job in new_result]
        expected_new_result_ids = [2, 3]
        self.assertEqual(expected_new_result_ids, new_result_job_ids)

    def test_input_parameters_argument_is_not_null(self):
        params = {
            'argument1_isnull': 'false',
        }

        input_parameters_list = [
            [{'name': 'argument0', 'type': 'string', 'value': 'red leave'},
             {'name': 'argument1', 'type': 'number', 'value': '3.14'}],
            [{'name': 'argument0', 'type': 'string', 'value': 'green grass'},
             {'name': 'argument1', 'type': 'number', 'value': None}],
            [{'name': 'argument0', 'type': 'string', 'value': 'more stuff'},
             {'name': 'argument1', 'type': 'number', 'value': float('nan')}]
        ]
        result = [self.MockJobInfo(job_id=index+1, input_params=input_parameters)
                  for index, input_parameters in enumerate(input_parameters_list)]

        null_filter = NullFilter()
        new_result = null_filter(result, params)

        self.assertEqual(len(new_result), 1)

        new_result_job_ids = [job.job_id for job in new_result]
        expected_new_result_ids = [1]
        self.assertEqual(expected_new_result_ids, new_result_job_ids)

    def test_output_metrics_is_null(self):
        params = {
            'metric1_isnull': 'true',
        }

        output_metrics_list = [
            [{'name': 'metric0', 'type': 'string', 'value': 'more stuff'},
             {'name': 'metric1', 'type': 'string', 'value': float('nan')}],
            [{'name': 'metric0', 'type': 'string', 'value': 'red leave'},
             {'name': 'metric1', 'type': 'string', 'value': 'vague'}],
            [{'name': 'metric0', 'type': 'string', 'value': 'green grass'},
             {'name': 'metric1', 'type': 'string', 'value': None}]
        ]
        result = [self.MockJobInfo(job_id=index+1, output_metrics=output_metrics)
                  for index, output_metrics in enumerate(output_metrics_list)]

        null_filter = NullFilter()
        new_result = null_filter(result, params)

        self.assertEqual(len(new_result), 2)

        new_result_job_ids = [job.job_id for job in new_result]
        expected_new_result_ids = [1, 3]
        self.assertEqual(expected_new_result_ids, new_result_job_ids)

    def test_output_metrics_is_not_null(self):
        params = {
            'metric1_isnull': 'false',
        }

        output_metrics_list = [
            [{'name': 'metric0', 'type': 'string', 'value': 'more stuff'},
             {'name': 'metric1', 'type': 'string', 'value': float('nan')}],
            [{'name': 'metric0', 'type': 'string', 'value': 'red leave'},
             {'name': 'metric1', 'type': 'string', 'value': 'vague'}],
            [{'name': 'metric0', 'type': 'string', 'value': 'green grass'},
             {'name': 'metric1', 'type': 'string', 'value': None}]
        ]
        result = [self.MockJobInfo(job_id=index+1, output_metrics=output_metrics)
                  for index, output_metrics in enumerate(output_metrics_list)]

        null_filter = NullFilter()
        new_result = null_filter(result, params)

        self.assertEqual(len(new_result), 1)

        new_result_job_ids = [job.job_id for job in new_result]
        expected_new_result_ids = [2]
        self.assertEqual(expected_new_result_ids, new_result_job_ids)
