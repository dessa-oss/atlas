"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_rest_api.v1.models.queued_job import QueuedJob
from foundations.scheduler_legacy_backend import LegacyBackend
from .jobs_tests_helper_mixin import JobsTestsHelperMixin


class TestQueuedJob(unittest.TestCase, JobsTestsHelperMixin):

    def setUp(self):
        self._setup_deployment('QUEUED')

    def tearDown(self):
        self._cleanup()

    def test_has_job_id(self):
        from uuid import uuid4

        job_id = str(uuid4())
        job = QueuedJob(job_id=job_id)

        self.assertEqual(job_id, job.job_id)

    def test_has_user(self):
        job = QueuedJob(user='Louis')
        self.assertEqual('Louis', job.user)

    def test_has_user_different_user(self):
        job = QueuedJob(user='Lenny')
        self.assertEqual('Lenny', job.user)

    def test_has_submitted_time(self):
        job = QueuedJob(submitted_time=484848448448844)
        self.assertEqual(484848448448844, job.submitted_time)

    def test_has_submitted_time_different_params(self):
        job = QueuedJob(submitted_time=984222255555546)
        self.assertEqual(984222255555546, job.submitted_time)

    def test_all_is_empty_response(self):
        self.assertEqual([], QueuedJob.all().evaluate())

    def test_all_returns_job_information_from_scheduler(self):
        self._make_queued_job('00000000-0000-0000-0000-000000000000', 123456789, 9999, 'soju hero')

        expected_job = QueuedJob(job_id='00000000-0000-0000-0000-000000000000', user='soju hero', submitted_time='1973-11-29T21:33:09')
        result = QueuedJob.all().evaluate()[0]

        self.assertEqual(expected_job, result)

    def test_all_returns_job_information_from_scheduler_with_different_jobs(self):
        self._make_queued_job('00000000-0000-0000-0000-000000000000', 987654321, 4444, 'soju zero')
        self._make_queued_job('00000000-0000-0000-0000-000000000001', 888888888, 3214, 'potato hero')

        expected_job = QueuedJob(job_id='00000000-0000-0000-0000-000000000000', user='soju zero', submitted_time='2001-04-19T04:25:21')
        expected_job_two = QueuedJob(job_id='00000000-0000-0000-0000-000000000001', user='potato hero', submitted_time='1998-03-03T01:34:48')
        expected_jobs = [expected_job, expected_job_two]
        result = QueuedJob.all().evaluate()

        self.assertEqual(expected_jobs, result)
