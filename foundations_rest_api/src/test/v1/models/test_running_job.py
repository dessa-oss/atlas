"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_rest_api.v1.models.running_job import RunningJob
from foundations.scheduler_legacy_backend import LegacyBackend
from .jobs_tests_helper_mixin import JobsTestsHelperMixin


class TestRunningJob(unittest.TestCase, JobsTestsHelperMixin):

    def setUp(self):
        self._setup_deployment('RUNNING')

    def tearDown(self):
        self._cleanup()

    def test_has_job_id(self):
        from uuid import uuid4

        job_id = str(uuid4())
        job = RunningJob(job_id=job_id)

        self.assertEqual(job_id, job.job_id)

    def test_has_user(self):
        job = RunningJob(user='Louis')
        self.assertEqual('Louis', job.user)

    def test_has_user_different_user(self):
        job = RunningJob(user='Lenny')
        self.assertEqual('Lenny', job.user)

    def test_has_job_parameters(self):
        job = RunningJob(job_parameters={'a': 5})
        self.assertEqual({'a': 5}, job.job_parameters)

    def test_has_job_parameters_different_params(self):
        job = RunningJob(job_parameters={'b': 3, 'c': 4})
        self.assertEqual({'b': 3, 'c': 4}, job.job_parameters)

    def test_has_input_params(self):
        job = RunningJob(input_params={'a': 5})
        self.assertEqual({'a': 5}, job.input_params)

    def test_has_input_params_different_params(self):
        job = RunningJob(input_params={'b': 3, 'c': 4})
        self.assertEqual({'b': 3, 'c': 4}, job.input_params)

    def test_has_output_metrics(self):
        job = RunningJob(output_metrics={'a': 5})
        self.assertEqual({'a': 5}, job.output_metrics)

    def test_has_output_metrics_different_params(self):
        job = RunningJob(output_metrics={'b': 3, 'c': 4})
        self.assertEqual({'b': 3, 'c': 4}, job.output_metrics)

    def test_has_start_time(self):
        job = RunningJob(start_time=123423423434)
        self.assertEqual(123423423434, job.start_time)

    def test_has_start_time_different_params(self):
        job = RunningJob(start_time=884234222323)
        self.assertEqual(884234222323, job.start_time)

    def test_all_is_empty_response(self):
        self.assertEqual([], RunningJob.all().evaluate())

    def test_all_returns_job_information_from_scheduler(self):
        self._make_running_job('00000000-0000-0000-0000-000000000000', 123456789, 9999, 'soju hero')

        expected_job = RunningJob(
            job_id='00000000-0000-0000-0000-000000000000', 
            user='soju hero', 
            start_time='1973-11-29T21:33:09', 
            job_parameters={},
            input_params=[], 
            output_metrics={}
        )
        result = RunningJob.all().evaluate()[0]

        self.assertEqual(expected_job, result)

    def test_all_returns_job_information_from_scheduler_with_different_jobs(self):
        self._make_running_job('00000000-0000-0000-0000-000000000000', 987654321, 4444, 'soju zero')
        self._make_running_job('00000000-0000-0000-0000-000000000001', 888888888, 3214, 'potato hero')

        expected_job = RunningJob(
            job_id='00000000-0000-0000-0000-000000000000', 
            user='soju zero', 
            start_time='2001-04-19T04:25:21', 
            job_parameters={},
            input_params=[], 
            output_metrics={}
        )
        expected_job_two = RunningJob(
            job_id='00000000-0000-0000-0000-000000000001', 
            user='potato hero', 
            start_time='1998-03-03T01:34:48', 
            job_parameters={},
            input_params=[], 
            output_metrics={}
        )
        expected_jobs = [expected_job, expected_job_two]
        result = RunningJob.all().evaluate()

        self.assertEqual(expected_jobs, result)
