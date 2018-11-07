"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

import unittest
from foundations_rest_api.v1.models.job import Job
from .job_manager_mixin import JobManagerMixin


class TestJobListing(unittest.TestCase, JobManagerMixin):

    __name__ = 'TestJobListing' # avoid crazy Python 2 bug: failure of unittest.skip decorator

    def setUp(self):
        self._setup_deployment('RUNNING')
        self._setup_results_archiving()

    def tearDown(self):
        self._cleanup()

    def test_has_job_id(self):
        from uuid import uuid4

        job_id = str(uuid4())
        job = Job(job_id=job_id)

        self.assertEqual(job_id, job.job_id)

    def test_has_user(self):
        job = Job(user='Louis')
        self.assertEqual('Louis', job.user)

    def test_has_user_different_user(self):
        job = Job(user='Lenny')
        self.assertEqual('Lenny', job.user)

    def test_has_job_parameters(self):
        job = Job(job_parameters={'a': 5})
        self.assertEqual({'a': 5}, job.job_parameters)

    def test_has_job_parameters_different_params(self):
        job = Job(job_parameters={'b': 3, 'c': 4})
        self.assertEqual({'b': 3, 'c': 4}, job.job_parameters)

    def test_has_input_params(self):
        job = Job(input_params=['some list of parameters'])
        self.assertEqual(['some list of parameters'], job.input_params)

    def test_has_input_params_different_params(self):
        job = Job(input_params=['some different list of parameters'])
        self.assertEqual(['some different list of parameters'], job.input_params)

    def test_has_output_metrics(self):
        job = Job(output_metrics={'a': 5})
        self.assertEqual({'a': 5}, job.output_metrics)

    def test_has_output_metrics_different_params(self):
        job = Job(output_metrics={'b': 3, 'c': 4})
        self.assertEqual({'b': 3, 'c': 4}, job.output_metrics)

    def test_has_status_completed(self):
        job = Job(status='completed')
        self.assertEqual('completed', job.status)

    def test_has_status_running(self):
        job = Job(status='running')
        self.assertEqual('running', job.status)

    def test_has_status_different_params(self):
        job = Job(status='completed in error')
        self.assertEqual('completed in error', job.status)

    def test_has_start_time(self):
        job = Job(start_time=123423423434)
        self.assertEqual(123423423434, job.start_time)

    def test_has_start_time_different_params(self):
        job = Job(start_time=884234222323)
        self.assertEqual(884234222323, job.start_time)

    def test_has_completed_time(self):
        job = Job(completed_time=123423423434)
        self.assertEqual(123423423434, job.completed_time)

    def test_has_completed_time_none(self):
        job = Job(completed_time=None)
        self.assertIsNone(job.completed_time)

    def test_has_completed_time_different_params(self):
        job = Job(completed_time=884234222323)
        self.assertEqual(884234222323, job.completed_time)

    def test_all_returns_multiple_jobs(self):
        def method():
            from foundations.stage_logging import log_metric
            log_metric('loss', 15.33)

        stage = self._pipeline.stage(method)
        self._make_completed_job('my job', stage, 9999999999, 9999999999)
        self._make_running_job('00000000-0000-0000-0000-000000000000', 123456789, 9999, 'soju hero')

        expected_job_1 = Job(
            job_id='00000000-0000-0000-0000-000000000000', 
            user='soju hero', 
            start_time='1973-11-29T21:33:09', 
            job_parameters={},
            input_params=[], 
            output_metrics={},
            status='Running',
            completed_time=None
        )

        expected_job_2 = Job(
            job_id='my job', 
            user='Unspecified',
            job_parameters={}, 
            input_params=[],
            output_metrics={'loss': 15.33}, 
            status='Completed',
            start_time='2286-11-20T17:46:39',
            completed_time='2286-11-20T17:46:39'
        )


        result = Job.all().evaluate()
        expected_jobs = [expected_job_2, expected_job_1]
        self.assertEqual(expected_jobs, result)

    @unittest.skip
    ### THIS TEST IS GOING TO BE SKIPPED UNTIL THOMAS DISCUSSES HOW TO RELATE PROJECTS WITH RUNNING JOBS WITH ASHWIN ####
    def test_all_returns_jobs_filtered_by_project(self):
        def method():
            from foundations.stage_logging import log_metric
            log_metric('loss', 15.33)

        stage = self._pipeline.stage(method)

        self._pipeline_context.provenance.project_name = 'project 1'
        self._make_completed_job('my job', stage, 9999999999, 9999999999)
        self._make_running_job('00000000-0000-0000-0000-000000000001', 123456789, 9999, 'soju hero')

        self._pipeline_context.provenance.project_name = 'project 2'
        self._make_running_job('00000000-0000-0000-0000-000000000002', 987654321, 8888, 'quin lin')

        expected_job_1 = Job(
            job_id='00000000-0000-0000-0000-000000000001', 
            user='soju hero', 
            start_time='1973-11-29T21:33:09', 
            job_parameters={},
            input_params=[], 
            output_metrics={},
            status='Running',
            completed_time=None
        )

        expected_job_2 = Job(
            job_id='my job', 
            user='Unspecified',
            job_parameters={}, 
            input_params=[],
            output_metrics={'loss': 15.33}, 
            status='Completed',
            start_time='2286-11-20T17:46:39',
            completed_time='2286-11-20T17:46:39'
        )

        result = Job.all(project_name='project 1').evaluate()
        expected_jobs = [expected_job_2, expected_job_1]
        self.assertEqual(len(result), 2)
        self.assertEqual(expected_jobs, result)
