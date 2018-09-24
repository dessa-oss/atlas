"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 09 2018
"""

import unittest
from mock import patch

from foundations.scheduler_local_backend import LocalBackend
from foundations.scheduler_job_information import JobInformation

class MockJob(object):
    def __init__(self, pipeline_context):
        self._pipeline_context = pipeline_context

    def pipeline_context(self):
        return self._pipeline_context

class MockListing(object):
    def __init__(self):
        pass

    def track_pipeline(self, pipeline_filename):
        MockListing.all_pipeline_names.append(pipeline_filename)

    def get_pipeline_names(self):
        return MockListing.all_pipeline_names

class MockArchive(object):
    def __init__(self):
        pass

    def fetch(self, name, prefix=None):
        if prefix:
            name = prefix + "/" + name

        return MockArchive.items[name]

    def append(self, name, item, prefix=None):
        if prefix:
            name = prefix + "/" + name

        MockArchive.items[name] = item
    
    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

class MockOS(object):
    pass

def mock_whoami():
    return MockOS.whoami

@patch("foundations.utils.whoami", mock_whoami)
class TestSchedulerLocalBackend(unittest.TestCase):
    def setUp(self):
        from foundations.global_state import config_manager

        config_manager["archive_listing_implementation"] = {
            "archive_listing_type": MockListing
        }

        config_manager["miscellaneous_archive_implementation"] = {
            "archive_type": MockArchive
        }

        MockListing.all_pipeline_names = []
        MockArchive.items = {}
        MockOS.whoami = None

    def _set_user(self, user_name):
        MockOS.whoami = user_name

    def _add_job(self, job_name, begin_time, duration):
        from foundations.pipeline_context import PipelineContext
        from foundations.job_persister import JobPersister

        pipeline_context = PipelineContext()

        pipeline_context.file_name = job_name
        pipeline_context.global_stage_context.start_time = begin_time
        pipeline_context.global_stage_context.delta_time = duration

        JobPersister(MockJob(pipeline_context)).persist()

    def test_running_status_unsupported(self):
        backend = LocalBackend()

        with self.assertRaises(ValueError):
            backend.get_paginated(None, None, "RUNNING")

    def test_get_completed_jobs_no_jobs(self):
        backend = LocalBackend()

        completed_jobs = list(backend.get_paginated(None, None, "COMPLETED"))
        self.assertEqual(completed_jobs, [])

    def test_get_completed_one_job_returns_non_list_iterable(self):
        self._add_job("this_job", 123, 22)

        backend = LocalBackend()

        completed_jobs = backend.get_paginated(None, None, "COMPLETED")
        self.assertTrue(hasattr(completed_jobs, "__iter__") and not isinstance(completed_jobs, list))

    def test_get_completed_one_job(self):
        self._set_user("ja")
        self._add_job("this_job", 123, 22)

        backend = LocalBackend()

        completed_jobs = list(backend.get_paginated(None, None, "COMPLETED"))
        expected_completed_jobs = [JobInformation("this_job", 123, 22, "COMPLETED", "ja")]
        self.assertEqual(completed_jobs, expected_completed_jobs)

    def test_get_completed_one_job_contains_ints_only(self):
        self._set_user("ja")
        self._add_job("this_job", 123.33, 22.44)

        backend = LocalBackend()

        completed_jobs = list(backend.get_paginated(None, None, "COMPLETED"))
        expected_completed_jobs = [JobInformation("this_job", 123, 22, "COMPLETED", "ja")]
        self.assertEqual(completed_jobs, expected_completed_jobs)

    def test_get_completed_one_job_different_job(self):
        self._set_user("tr")
        self._add_job("that_job", 456, 24)

        backend = LocalBackend()

        completed_jobs = list(backend.get_paginated(None, None, "COMPLETED"))
        expected_completed_jobs = [JobInformation("that_job", 456, 24, "COMPLETED", "tr")]
        self.assertEqual(completed_jobs, expected_completed_jobs)

    def test_get_completed_two_jobs(self):
        self._set_user("ja")
        self._add_job("this_job", 123, 22)
        self._add_job("that_job", 456, 24)

        backend = LocalBackend()

        completed_jobs = list(backend.get_paginated(None, None, "COMPLETED"))
        expected_completed_jobs = [
            JobInformation("this_job", 123, 22, "COMPLETED", "ja"),
            JobInformation("that_job", 456, 24, "COMPLETED", "ja")
        ]

        self.assertEqual(completed_jobs, expected_completed_jobs)

    def test_get_all_three_jobs(self):
        self._set_user("ja")
        self._add_job("this_job", 123, 22)
        self._add_job("that_job", 456, 24)
        self._add_job("what_job", 2332323, 1080)

        backend = LocalBackend()

        completed_jobs = list(backend.get_paginated(None, None, None))
        expected_completed_jobs = [
            JobInformation("this_job", 123, 22, "COMPLETED", "ja"),
            JobInformation("that_job", 456, 24, "COMPLETED", "ja"),
            JobInformation("what_job", 2332323, 1080, "COMPLETED", "ja")
        ]
        
        self.assertEqual(completed_jobs, expected_completed_jobs)