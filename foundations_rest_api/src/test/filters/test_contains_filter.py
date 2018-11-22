"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""
import unittest
from mock import patch
from foundations_rest_api.filters.contains_filter import ContainsFilter

class TestContainsFilter(unittest.TestCase):

    class MockJobInfo(object):

        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    def test_user_contains(self):
        params = {
            'user_contains': 'oven'
        }

        job_users = ['mozart', 'beethoven', 'tchaikovsky']

        result = [self.MockJobInfo(user=job_user) for job_user in job_users]

        contain_filter = ContainsFilter()
        new_result = contain_filter(result, params)

        self.assertEqual(len(new_result), 1)

        new_result_users = [job.user for job in new_result]
        expected_new_result_user = ['beethoven']
        self.assertEqual(expected_new_result_user, new_result_users)

    def test_status_contains(self):
        params = {
            'status_contains': 'u'
        }

        job_statuses = ['RUNNING', 'COMPLETED', 'FAILED', 'COMPLETED', 'RUNNING']

        result = [self.MockJobInfo(job_id=index+1, status=status) for index, status in enumerate(job_statuses)]

        contain_filter = ContainsFilter()
        new_result = contain_filter(result, params)

        self.assertEqual(len(new_result), 2)

        new_result_ids = [job.job_id for job in new_result]
        expected_new_result_ids = [1, 5]
        self.assertEqual(expected_new_result_ids, new_result_ids)

    def test_start_time_contains(self):
        from datetime import datetime

        params = {
            'start_time_contains': '15'
        }

        jobs_start_times = [
            datetime(2018, 8, 1, 10, 30, 0, 0, None),
            datetime(2018, 9, 30, 1, 0, 0, 0, None),
            datetime(2018, 10, 10, 15, 30, 0, 0, None),
            datetime(2018, 11, 1, 21, 15, 0, 0, None),
            datetime(2018, 12, 1, 10, 30, 0, 0, None),
        ]

        result = [self.MockJobInfo(start_time=start_time.isoformat()) for start_time in jobs_start_times]

        contain_filter = ContainsFilter()
        new_result = contain_filter(result, params)

        self.assertEqual(len(new_result), 2)

        new_result_start_times = [job.start_time for job in new_result]
        expected_new_result_start_times = [start_time.isoformat() for start_time in jobs_start_times[2:4]]
        self.assertEqual(expected_new_result_start_times, new_result_start_times)
