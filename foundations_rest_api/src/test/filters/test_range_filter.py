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
