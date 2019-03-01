"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_internal.testing.helpers.spec import Spec
from foundations_internal.testing.helpers import let_patch_mock, let
from pandas import DataFrame
from pandas.util.testing import assert_frame_equal

from foundations.prototype.jobs import get_queued_jobs

class TestPrototypeJobs(Spec):

    all_queued_jobs_mock = let_patch_mock('foundations_contrib.models.queued_job.QueuedJob.all')
    
    def test_get_queued_jobs_returns_empty_data_frame(self):
        self.all_queued_jobs_mock.return_value = []

        expected_result = DataFrame([])
        assert_frame_equal(expected_result, get_queued_jobs())

    def test_get_queued_jobs_returns_a_queued_job(self):
        first_queued_job = self._random_queued_job()
        
        self.all_queued_jobs_mock.return_value = [first_queued_job]
        
        expected_result = DataFrame([
            {
                'job_id': first_queued_job.job_id,
                'queued_time': first_queued_job.queued_time,
                'time_since_queued': first_queued_job.time_since_queued,
                'project_name': first_queued_job.project_name,
            }
        ])
        assert_frame_equal(expected_result, get_queued_jobs())

    def test_get_queued_jobs_returns_queued_jobs(self):
        first_queued_job = self._random_queued_job()
        second_queued_job = self._random_queued_job()
        
        self.all_queued_jobs_mock.return_value = [first_queued_job, second_queued_job]
        
        expected_result = DataFrame([
            {
                'job_id': first_queued_job.job_id,
                'queued_time': first_queued_job.queued_time,
                'time_since_queued': first_queued_job.time_since_queued,
                'project_name': first_queued_job.project_name,
            },
            {
                'job_id': second_queued_job.job_id,
                'queued_time': second_queued_job.queued_time,
                'time_since_queued': second_queued_job.time_since_queued,
                'project_name': second_queued_job.project_name,
            }
        ])
        assert_frame_equal(expected_result, get_queued_jobs())
        
    def test_get_queued_jobs_is_global(self):
        import foundations.prototype
        self.assertEqual(get_queued_jobs, foundations.prototype.get_queued_jobs)

    def _random_queued_job(self):
        from foundations_contrib.models.queued_job import QueuedJob
        import random

        return QueuedJob(
            job_id=self.faker.sha256(),
            queued_time=random.randint(1, 100),
            time_since_queued=random.randint(1, 100),
            project_name=self.faker.name()
        )