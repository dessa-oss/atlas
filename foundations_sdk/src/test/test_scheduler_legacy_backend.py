"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

import unittest
from mock import patch

from foundations.scheduler_legacy_backend import LegacyBackend
from foundations.scheduler_job_information import JobInformation

class MockBucketStatScanner(object):
    def __init__(self, path):
        self._path = path

    def scan(self):
        return MockBucketStatScanner.dirs[self._path]

class MockClock(object):
    def __init__(self, time_to_show=0):
        self._time = time_to_show
    
    def time(self):
        return self._time

class TestSchedulerLegacyBackend(unittest.TestCase):

    def setUp(self):
        MockBucketStatScanner.dirs = {}

    def _create_buckets(self, jobs_bucket_name, archives_bucket_name, results_bucket_name):
        MockBucketStatScanner.dirs[jobs_bucket_name] = []
        MockBucketStatScanner.dirs[archives_bucket_name] = []
        MockBucketStatScanner.dirs[results_bucket_name] = []

    def _add_to_bucket(self, bucket_name, entry):
        MockBucketStatScanner.dirs[bucket_name].append(entry)

    def test_get_queued_jobs_no_jobs(self):
        self._create_buckets('jobs', 'archives', 'results')
        backend = LegacyBackend(MockClock(), MockBucketStatScanner, 'jobs', 'archives', 'results')
        
        queued_jobs = list(backend.get_paginated(None, None, status="QUEUED"))
        self.assertEqual(queued_jobs, [])

    def test_get_queued_jobs_one_job(self):
        self._create_buckets('jobs', 'archives', 'results')
        self._add_to_bucket('jobs', {'owner': 'me', 'last_modified': 22, 'filename': 'this_file.tgz'})
        backend = LegacyBackend(MockClock(55), MockBucketStatScanner, 'jobs', 'archives', 'results')
        
        queued_jobs = list(backend.get_paginated(None, None, status="QUEUED"))
        self.assertEqual(queued_jobs, [JobInformation('this_file.tgz', 22, 33, "QUEUED", "me")])

    def test_get_queued_jobs_returns_non_list_iterable(self):
        self._create_buckets('jobs', 'archives', 'results')
        backend = LegacyBackend(MockClock(), MockBucketStatScanner, 'jobs', 'archives', 'results')
        
        queued_jobs = backend.get_paginated(None, None, status="QUEUED")
        self.assertTrue(hasattr(queued_jobs, "__iter__") and not isinstance(queued_jobs, list))

    def test_get_queued_jobs_one_job_different_job_different_time(self):
        self._create_buckets('jobs', 'archives', 'results')
        self._add_to_bucket('jobs', {'owner': 'you', 'last_modified': 23, 'filename': 'that_file.tgz'})
        backend = LegacyBackend(MockClock(100), MockBucketStatScanner, 'jobs', 'archives', 'results')
        
        queued_jobs = list(backend.get_paginated(None, None, status="QUEUED"))
        self.assertEqual(queued_jobs, [JobInformation('that_file.tgz', 23, 77, "QUEUED", "you")])

    def test_get_queued_jobs_two_jobs(self):
        self._create_buckets('jobs', 'archives', 'results')
        self._add_to_bucket('jobs', {'owner': 'me', 'last_modified': 22, 'filename': 'this_file.tgz'})
        self._add_to_bucket('jobs', {'owner': 'you', 'last_modified': 23, 'filename': 'that_file.tgz'})
        backend = LegacyBackend(MockClock(100), MockBucketStatScanner, 'jobs', 'archives', 'results')
        
        queued_jobs = list(backend.get_paginated(None, None, status="QUEUED"))
        expected_queued_jobs = [
            JobInformation('this_file.tgz', 22, 78, "QUEUED", "me"),
            JobInformation('that_file.tgz', 23, 77, "QUEUED", "you")
        ]

        self.assertEqual(queued_jobs, expected_queued_jobs)

    def test_get_queued_jobs_two_jobs_different_bucket(self):
        self._create_buckets('jobs2', 'archives', 'results')
        self._add_to_bucket('jobs2', {'owner': 'me', 'last_modified': 22, 'filename': 'this_file.tgz'})
        self._add_to_bucket('jobs2', {'owner': 'you', 'last_modified': 23, 'filename': 'that_file.tgz'})
        backend = LegacyBackend(MockClock(100), MockBucketStatScanner, 'jobs2', 'archives', 'results')
        
        queued_jobs = list(backend.get_paginated(None, None, status="QUEUED"))
        expected_queued_jobs = [
            JobInformation('this_file.tgz', 22, 78, "QUEUED", "me"),
            JobInformation('that_file.tgz', 23, 77, "QUEUED", "you")
        ]

        self.assertEqual(queued_jobs, expected_queued_jobs)

    def test_get_running_jobs_no_jobs(self):
        self._create_buckets('jobs', 'archives', 'results')
        backend = LegacyBackend(MockClock(), MockBucketStatScanner, 'jobs', 'archives', 'results')
        
        running_jobs = list(backend.get_paginated(None, None, status="RUNNING"))
        self.assertEqual(running_jobs, [])

    def test_get_running_jobs_no_jobs_one_queued(self):
        self._create_buckets('jobs', 'archives', 'results')
        self._add_to_bucket('jobs', {'owner': 'me', 'last_modified': 22, 'filename': 'this_file.tgz'})
        backend = LegacyBackend(MockClock(), MockBucketStatScanner, 'jobs', 'archives', 'results')
        
        running_jobs = list(backend.get_paginated(None, None, status="RUNNING"))
        self.assertEqual(running_jobs, [])

    def test_get_running_jobs_one_job(self):
        self._create_buckets('jobs', 'archives', 'results')
        self._add_to_bucket('archives', {'owner': 'me', 'last_modified': 22, 'filename': 'this_file.tgz'})
        backend = LegacyBackend(MockClock(100), MockBucketStatScanner, 'jobs', 'archives', 'results')
        
        running_jobs = list(backend.get_paginated(None, None, status="RUNNING"))
        self.assertEqual(running_jobs, [JobInformation('this_file.tgz', 22, 78, "RUNNING", "me")])

    def test_get_running_jobs_one_job_different_job(self):
        self._create_buckets('jobs', 'archives', 'results')
        self._add_to_bucket('archives', {'owner': 'you', 'last_modified': 25, 'filename': 'that_file.tgz'})
        backend = LegacyBackend(MockClock(100), MockBucketStatScanner, 'jobs', 'archives', 'results')
        
        running_jobs = list(backend.get_paginated(None, None, status="RUNNING"))
        self.assertEqual(running_jobs, [JobInformation('that_file.tgz', 25, 75, "RUNNING", "you")])

    def test_get_running_jobs_two_jobs_different_bucket(self):
        self._create_buckets('jobs', 'archives2', 'results')
        self._add_to_bucket('archives2', {'owner': 'me', 'last_modified': 22, 'filename': 'this_file.tgz'})
        self._add_to_bucket('archives2', {'owner': 'you', 'last_modified': 23, 'filename': 'that_file.tgz'})
        backend = LegacyBackend(MockClock(100), MockBucketStatScanner, 'jobs', 'archives2', 'results')
        
        running_jobs = list(backend.get_paginated(None, None, status="RUNNING"))
        expected_running_jobs = [
            JobInformation('this_file.tgz', 22, 78, "RUNNING", "me"),
            JobInformation('that_file.tgz', 23, 77, "RUNNING", "you")
        ]

        self.assertEqual(running_jobs, expected_running_jobs)

    def test_get_running_jobs_two_jobs_one_running_one_done(self):
        self._create_buckets('jobs', 'archives', 'results')
        self._add_to_bucket('archives', {'owner': 'me', 'last_modified': 22, 'filename': 'this_file.tgz'})
        self._add_to_bucket('archives', {'owner': 'you', 'last_modified': 23, 'filename': 'that_file.tgz'})
        self._add_to_bucket('results', {'owner': 'you', 'last_modified': 27, 'filename': 'that_file.tgz'})
        backend = LegacyBackend(MockClock(100), MockBucketStatScanner, 'jobs', 'archives', 'results')
        
        running_jobs = list(backend.get_paginated(None, None, status="RUNNING"))
        expected_running_jobs = [
            JobInformation('this_file.tgz', 22, 78, "RUNNING", "me")
        ]

        self.assertEqual(running_jobs, expected_running_jobs)

    def test_get_running_jobs_five_jobs_three_running_two_done(self):
        self._create_buckets('jobs', 'archives', 'results')
        self._add_to_bucket('archives', {'owner': 'me', 'last_modified': 22, 'filename': 'this_file.tgz'})
        self._add_to_bucket('archives', {'owner': 'you', 'last_modified': 23, 'filename': 'that_file.tgz'})
        self._add_to_bucket('archives', {'owner': 'they', 'last_modified': 22, 'filename': 'it_file.tgz'})
        self._add_to_bucket('archives', {'owner': 'them', 'last_modified': 24, 'filename': 'what_file.tgz'})
        self._add_to_bucket('archives', {'owner': 'pippin', 'last_modified': 26, 'filename': 'where_file.tgz'})
        self._add_to_bucket('results', {'owner': 'they', 'last_modified': 30, 'filename': 'it_file.tgz'})
        self._add_to_bucket('results', {'owner': 'them', 'last_modified': 40, 'filename': 'what_file.tgz'})
        backend = LegacyBackend(MockClock(100), MockBucketStatScanner, 'jobs', 'archives', 'results')
        
        running_jobs = list(backend.get_paginated(None, None, status="RUNNING"))
        expected_running_jobs = [
            JobInformation('this_file.tgz', 22, 78, "RUNNING", "me"),
            JobInformation('that_file.tgz', 23, 77, "RUNNING", "you"),
            JobInformation('where_file.tgz', 26, 74, "RUNNING", "pippin")
        ]

        self.assertEqual(running_jobs, expected_running_jobs)

    def test_get_completed_jobs_five_jobs_three_running_two_done(self):
        self._create_buckets('jobs', 'archives', 'results')
        self._add_to_bucket('archives', {'owner': 'me', 'last_modified': 22, 'filename': 'this_file.tgz'})
        self._add_to_bucket('archives', {'owner': 'you', 'last_modified': 23, 'filename': 'that_file.tgz'})
        self._add_to_bucket('archives', {'owner': 'they', 'last_modified': 22, 'filename': 'it_file.tgz'})
        self._add_to_bucket('archives', {'owner': 'them', 'last_modified': 24, 'filename': 'what_file.tgz'})
        self._add_to_bucket('archives', {'owner': 'pippin', 'last_modified': 26, 'filename': 'where_file.tgz'})
        self._add_to_bucket('results', {'owner': 'they', 'last_modified': 30, 'filename': 'it_file.tgz'})
        self._add_to_bucket('results', {'owner': 'them', 'last_modified': 40, 'filename': 'what_file.tgz'})
        backend = LegacyBackend(MockClock(100), MockBucketStatScanner, 'jobs', 'archives', 'results')
        
        completed_jobs = list(backend.get_paginated(None, None, status="COMPLETED"))
        expected_completed_jobs = [
            JobInformation('it_file.tgz', 22, 8, "COMPLETED", "they"),
            JobInformation('what_file.tgz', 24, 16, "COMPLETED", "them")
        ]

        self.assertEqual(completed_jobs, expected_completed_jobs)

    def test_get_all_jobs(self):
        self._create_buckets('jobs', 'archives', 'results')
        self._add_to_bucket('jobs', {'owner': 'me', 'last_modified': 22, 'filename': 'this_file.tgz'})
        self._add_to_bucket('archives', {'owner': 'you', 'last_modified': 23, 'filename': 'that_file.tgz'})
        self._add_to_bucket('archives', {'owner': 'they', 'last_modified': 22, 'filename': 'it_file.tgz'})
        self._add_to_bucket('archives', {'owner': 'them', 'last_modified': 24, 'filename': 'what_file.tgz'})
        self._add_to_bucket('archives', {'owner': 'pippin', 'last_modified': 26, 'filename': 'where_file.tgz'})
        self._add_to_bucket('results', {'owner': 'they', 'last_modified': 30, 'filename': 'it_file.tgz'})
        self._add_to_bucket('results', {'owner': 'them', 'last_modified': 40, 'filename': 'what_file.tgz'})
        backend = LegacyBackend(MockClock(100), MockBucketStatScanner, 'jobs', 'archives', 'results')
        
        all_jobs = list(backend.get_paginated(None, None, status=None))
        expected_all_jobs = [
            JobInformation('this_file.tgz', 22, 78, "QUEUED", "me"),
            JobInformation('that_file.tgz', 23, 77, "RUNNING", "you"),
            JobInformation('it_file.tgz', 22, 8, "COMPLETED", "they"),
            JobInformation('what_file.tgz', 24, 16, "COMPLETED", "them"),
            JobInformation('where_file.tgz', 26, 74, "RUNNING", "pippin")
        ]

        self.assertEqual(all_jobs, expected_all_jobs)
    
    def test_get_all_jobs_different_setting(self):
        self._create_buckets('jobs', 'archives', 'results')
        self._add_to_bucket('archives', {'owner': 'me', 'last_modified': 22, 'filename': 'this_file.tgz'})
        self._add_to_bucket('jobs', {'owner': 'you', 'last_modified': 23, 'filename': 'that_file.tgz'})
        self._add_to_bucket('archives', {'owner': 'they', 'last_modified': 22, 'filename': 'it_file.tgz'})
        self._add_to_bucket('archives', {'owner': 'them', 'last_modified': 24, 'filename': 'what_file.tgz'})
        self._add_to_bucket('archives', {'owner': 'pippin', 'last_modified': 26, 'filename': 'where_file.tgz'})
        self._add_to_bucket('results', {'owner': 'them', 'last_modified': 40, 'filename': 'what_file.tgz'})
        backend = LegacyBackend(MockClock(100), MockBucketStatScanner, 'jobs', 'archives', 'results')
        
        all_jobs = list(backend.get_paginated(None, None, status=None))
        expected_all_jobs = [
            JobInformation('that_file.tgz', 23, 77, "QUEUED", "you"),
            JobInformation('this_file.tgz', 22, 78, "RUNNING", "me"),
            JobInformation('it_file.tgz', 22, 78, "RUNNING", "they"),
            JobInformation('what_file.tgz', 24, 16, "COMPLETED", "them"),
            JobInformation('where_file.tgz', 26, 74, "RUNNING", "pippin")
        ]

        self.assertEqual(all_jobs, expected_all_jobs)

    def test_invalid_status(self):
        self._create_buckets('jobs', 'archives', 'results')
        backend = LegacyBackend(MockClock(100), MockBucketStatScanner, 'jobs', 'archives', 'results')

        with self.assertRaises(ValueError):
            backend.get_paginated(None, None, status="STATUS")

    def test_invalid_status_different_status(self):
        self._create_buckets('jobs', 'archives', 'results')
        backend = LegacyBackend(MockClock(100), MockBucketStatScanner, 'jobs', 'archives', 'results')

        with self.assertRaises(ValueError):
            backend.get_paginated(None, None, status="STATUS2")