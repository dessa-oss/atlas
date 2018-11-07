"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_rest_api.v1.models.completed_job import CompletedJob
from .job_manager_mixin import JobManagerMixin


class TestCompletedJob(unittest.TestCase, JobManagerMixin):

    def setUp(self):
        self._setup_results_archiving()

    def tearDown(self):
        self._cleanup()

    def test_has_job_id(self):
        from uuid import uuid4

        job_id = str(uuid4())
        job = CompletedJob(job_id=job_id)

        self.assertEqual(job_id, job.job_id)

    def test_has_user(self):
        job = CompletedJob(user='Louis')
        self.assertEqual('Louis', job.user)

    def test_has_user_different_user(self):
        job = CompletedJob(user='Lenny')
        self.assertEqual('Lenny', job.user)

    def test_has_job_parameters(self):
        job = CompletedJob(job_parameters={'a': 5})
        self.assertEqual({'a': 5}, job.job_parameters)

    def test_has_job_parameters_different_params(self):
        job = CompletedJob(job_parameters={'b': 3, 'c': 4})
        self.assertEqual({'b': 3, 'c': 4}, job.job_parameters)

    def test_has_input_params(self):
        job = CompletedJob(input_params=['some list of parameters'])
        self.assertEqual(['some list of parameters'], job.input_params)

    def test_has_input_params_different_params(self):
        job = CompletedJob(input_params=['some different list of parameters'])
        self.assertEqual(['some different list of parameters'], job.input_params)

    def test_has_output_metrics(self):
        job = CompletedJob(output_metrics={'a': 5})
        self.assertEqual({'a': 5}, job.output_metrics)

    def test_has_output_metrics_different_params(self):
        job = CompletedJob(output_metrics={'b': 3, 'c': 4})
        self.assertEqual({'b': 3, 'c': 4}, job.output_metrics)

    def test_has_status(self):
        job = CompletedJob(status='completed')
        self.assertEqual('completed', job.status)

    def test_has_status_different_params(self):
        job = CompletedJob(status='completed in error')
        self.assertEqual('completed in error', job.status)

    def test_has_start_time(self):
        job = CompletedJob(start_time=123423423434)
        self.assertEqual(123423423434, job.start_time)

    def test_has_start_time_different_params(self):
        job = CompletedJob(start_time=884234222323)
        self.assertEqual(884234222323, job.start_time)

    def test_has_completed_time(self):
        job = CompletedJob(completed_time=123423423434)
        self.assertEqual(123423423434, job.completed_time)

    def test_has_completed_time_different_params(self):
        job = CompletedJob(completed_time=884234222323)
        self.assertEqual(884234222323, job.completed_time)

    def test_all_returns_a_job(self):
        def method():
            from foundations.stage_logging import log_metric
            log_metric('loss', 15.33)

        stage = self._pipeline.stage(method)

        self._make_completed_job('my job', stage, 9999999999, 9999999999)

        job = CompletedJob.all().evaluate()[0]
        expected_job = CompletedJob(
            job_id='my job', 
            user='Unspecified',
            job_parameters={}, 
            input_params=[],
            output_metrics={'loss': 15.33}, 
            status='Completed',
            start_time='2286-11-20T17:46:39',
            completed_time='2286-11-20T17:46:39'
        )
        self.assertEqual(expected_job, job)

    def test_all_returns_a_job_different_name(self):
        def method():
            pass

        stage = self._pipeline.stage(method)

        self._make_completed_job('my other job', stage, 123232233, 312333333)

        job = CompletedJob.all().evaluate()[0]
        expected_job = CompletedJob(
            job_id='my other job', 
            user='Unspecified',
            job_parameters={}, 
            input_params=[],
            output_metrics={}, 
            status='Completed',
            start_time='1973-11-27T07:10:33',
            completed_time='1979-11-24T23:15:33'
        )
        self.assertEqual(expected_job, job)

    def test_all_returns_a_job_different_metrics(self):
        def method():
            from foundations.stage_logging import log_metric
            log_metric('win', 99.9)
            log_metric('accuracy', 0)

        stage = self._pipeline.stage(method)

        self._make_completed_job('my job', stage, 444444, 5555555)

        job = CompletedJob.all().evaluate()[0]
        expected_job = CompletedJob(
            job_id='my job', 
            user='Unspecified',
            job_parameters={}, 
            input_params=[],
            output_metrics={'win': 99.9, 'accuracy': 0}, 
            status='Completed',
            start_time='1970-01-06T03:27:24',
            completed_time='1970-03-06T07:12:35'
        )
        self.assertEqual(expected_job, job)

    def test_all_returns_a_job_metric_multiple_instances(self):
        def method():
            from foundations.stage_logging import log_metric
            log_metric('win', 99.9)
            log_metric('win', 99.99)

        stage = self._pipeline.stage(method)

        self._make_completed_job('my job', stage, 444444, 5555555)

        job = CompletedJob.all().evaluate()[0]
        expected_job = CompletedJob(
            job_id='my job', 
            user='Unspecified',
            job_parameters={}, 
            input_params=[], 
            output_metrics={'win': [99.9, 99.99]}, 
            status='Completed',
            start_time='1970-01-06T03:27:24',
            completed_time='1970-03-06T07:12:35'
        )
        self.assertEqual(expected_job, job)

    def test_all_returns_a_job_with_run_data(self):
        from foundations.hyperparameter import Hyperparameter

        def method(hello):
            pass

        stage = self._pipeline.stage(method, hello=Hyperparameter('hello'))

        self._make_completed_job('my job', stage, 343433, 43444, hello='world')

        job = CompletedJob.all().evaluate()[0]
        input_params = [{'stage_uuid': 'e56573879d1a601ec8845955e194dff00942bf30', 'name': 'hello', 'value': {'type': 'dynamic', 'name': 'hello'}}]
        expected_job = CompletedJob(
            job_id='my job', 
            user='Unspecified',
            job_parameters={'hello': 'world'}, 
            input_params=input_params,
            output_metrics={}, 
            status='Completed',
            start_time='1970-01-04T23:23:53',
            completed_time='1970-01-01T12:04:04',
        )
        self.assertEqual(expected_job, job)

    def test_all_returns_multiple_jobs(self):
        def method():
            from foundations.stage_logging import log_metric
            log_metric('loss', 15.33)

        stage = self._pipeline.stage(method)

        self._make_completed_job('my job', stage, 9999999999, 9999999999)
        self._make_completed_job('my job two', stage, 77777777, 77777777)

        jobs = CompletedJob.all().evaluate()
        expected_job = CompletedJob(
            job_id='my job', 
            user='Unspecified',
            job_parameters={}, 
            input_params=[],
            output_metrics={'loss': 15.33}, 
            status='Completed',
            start_time='2286-11-20T17:46:39',
            completed_time='2286-11-20T17:46:39'
        )
        expected_job_two = CompletedJob(
            job_id='my job two', 
            user='Unspecified',
            job_parameters={}, 
            input_params=[],
            output_metrics={'loss': 15.33}, 
            status='Completed',
            start_time='1972-06-19T04:56:17',
            completed_time='1972-06-19T04:56:17'
        )

        sort_key = lambda job: job.job_id

        self.assertEqual(sorted([expected_job, expected_job_two], key=sort_key), sorted(jobs, key=sort_key))

    def test_all_returns_project_filtered_jobs(self):
        def method():
            from foundations.stage_logging import log_metric
            log_metric('loss', 15.33)

        stage = self._pipeline.stage(method)

        self._pipeline_context.provenance.project_name = 'project 1'
        self._make_completed_job('my job', stage, 9999999999, 9999999999)

        self._pipeline_context.provenance.project_name = 'project 2'
        self._make_completed_job('my job two', stage, 77777777, 77777777)

        jobs = CompletedJob.all(project_name='project 1').evaluate()
        expected_job = CompletedJob(
            job_id='my job', 
            user='Unspecified',
            job_parameters={}, 
            input_params=[],
            output_metrics={'loss': 15.33}, 
            status='Completed',
            start_time='2286-11-20T17:46:39',
            completed_time='2286-11-20T17:46:39'
        )
        self.assertEqual([expected_job], jobs)

    def test_all_returns_project_filtered_jobs_different_project(self):
        def method():
            from foundations.stage_logging import log_metric
            log_metric('loss', 15.33)

        stage = self._pipeline.stage(method)

        self._pipeline_context.provenance.project_name = 'project 1'
        self._make_completed_job('my job', stage, 9999999999, 9999999999)

        self._pipeline_context.provenance.project_name = 'project 2'
        self._make_completed_job('my job two', stage, 77777777, 77777777)

        jobs = CompletedJob.all(project_name='project 2').evaluate()
        expected_job = CompletedJob(
            job_id='my job two', 
            user='Unspecified',
            job_parameters={}, 
            input_params=[],
            output_metrics={'loss': 15.33}, 
            status='Completed',
            start_time='1972-06-19T04:56:17',
            completed_time='1972-06-19T04:56:17'
        )
        self.assertEqual([expected_job], jobs)

