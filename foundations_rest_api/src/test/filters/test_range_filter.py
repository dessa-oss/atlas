"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""
import unittest
from mock import patch
from foundations_rest_api.filters.range_filter import RangeFilter


class TestRangeFilter(unittest.TestCase):

    class MockJobInfo(object):

        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    def test_start_time_range(self):
        from datetime import datetime

        params = {
            'start_time_starts': datetime(2018, 9, 1, 10, 30, 0, 0, None).isoformat(),
            'start_time_ends': datetime(2018, 11, 21, 16, 52, 0, 0, None).isoformat()
        }

        jobs_start_times = [
            datetime(2018, 8, 1, 10, 30, 0, 0, None),
            datetime(2018, 9, 30, 1, 0, 0, 0, None),
            datetime(2018, 10, 10, 15, 30, 0, 0, None),
            datetime(2018, 11, 1, 21, 15, 0, 0, None),
            datetime(2018, 12, 1, 10, 30, 0, 0, None),
        ]

        result = [self.MockJobInfo(start_time=start_time.isoformat()) for start_time in jobs_start_times]

        range_filter = RangeFilter()
        new_result = range_filter(result, params)

        self.assertEqual(len(new_result), 3)

        new_result_start_times = [job.start_time for job in new_result]
        expected_new_result_start_times = [start_time.isoformat() for start_time in jobs_start_times[1:4]]
        self.assertEqual(expected_new_result_start_times, new_result_start_times)

    def test_user_range(self):
        params = {
            'user_starts': 'beethoven',
            'user_ends': 'tchaikovsky'
        }

        job_users = ['bach', 'mozart', 'beethoven', 'tchaikovsky', 'verdi']

        result = [self.MockJobInfo(user=job_user) for job_user in job_users]

        range_filter = RangeFilter()
        new_result = range_filter(result, params)

        self.assertEqual(len(new_result), 3)

        new_result_users = [job.user for job in new_result]
        expected_new_result_user = ['mozart', 'beethoven', 'tchaikovsky']
        self.assertEqual(expected_new_result_user, new_result_users)

    def test_status_range(self):
        params = {
            'status_starts': 'failed',
            'status_ends': 'queued',
        }

        job_statuses = ['RUNNING', 'COMPLETED', 'FAILED', 'COMPLETED', 'RUNNING', 'FAILED', 'QUEUED']

        result = [self.MockJobInfo(job_id=index+1, status=status) for index, status in enumerate(job_statuses)]

        range_filter = RangeFilter()
        new_result = range_filter(result, params)

        self.assertEqual(len(new_result), 3)

        new_result_ids = [job.job_id for job in new_result]
        expected_new_result_ids = [3, 6, 7]
        self.assertEqual(expected_new_result_ids, new_result_ids)

    def test_input_parameters_range(self):
        params = {
            'argument1_starts': '2',
            'argument1_ends': '6',
        }

        input_parameters_list = [
            [{'name': 'argument0', 'type': 'string', 'value': 'red leave'},
             {'name': 'argument1', 'type': 'number', 'value': '3.14'}],
            [{'name': 'argument0', 'type': 'string', 'value': 'green grass'},
             {'name': 'argument1', 'type': 'number', 'value': '9.8'}],
            [{'name': 'argument0', 'type': 'string', 'value': 'more stuff'},
             {'name': 'argument1', 'type': 'number', 'value': '5'}]
        ]
        result = [self.MockJobInfo(job_id=index+1, input_params=input_parameters)
                  for index, input_parameters in enumerate(input_parameters_list)]

        range_filter = RangeFilter()
        new_result = range_filter(result, params)

        self.assertEqual(len(new_result), 2)

        new_result_job_ids = [job.job_id for job in new_result]
        expected_new_result_ids = [1, 3]
        self.assertEqual(expected_new_result_ids, new_result_job_ids)

    def test_output_metrics_range(self):
        params = {
            'metric1_starts': 'ad',
            'metric1_ends': 'tao',
        }

        output_metrics_list = [
            [{'name': 'metric0', 'type': 'string', 'value': 'more stuff'},
             {'name': 'metric1', 'type': 'string', 'value': 'bohemian'}],
            [{'name': 'metric0', 'type': 'string', 'value': 'red leave'},
             {'name': 'metric1', 'type': 'string', 'value': 'vague'}],
            [{'name': 'metric0', 'type': 'string', 'value': 'green grass'},
             {'name': 'metric1', 'type': 'string', 'value': 'rapsody'}]
        ]
        result = [self.MockJobInfo(job_id=index+1, output_metrics=output_metrics)
                  for index, output_metrics in enumerate(output_metrics_list)]

        range_filter = RangeFilter()
        new_result = range_filter(result, params)

        self.assertEqual(len(new_result), 2)

        new_result_job_ids = [job.job_id for job in new_result]
        expected_new_result_ids = [1, 3]
        self.assertEqual(expected_new_result_ids, new_result_job_ids)
