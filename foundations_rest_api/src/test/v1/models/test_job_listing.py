"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

import unittest
from mock import patch
from foundations_rest_api.v1.models.job import Job


class TestJobListing(unittest.TestCase):

    __name__ = 'TestJobListing' # avoid crazy Python 2 bug: failure of unittest.skip decorator

    class MockJob(object):

        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

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


    @patch('foundations_contrib.models.pipeline_context_listing.PipelineContextListing.pipeline_contexts')
    @patch('foundations_rest_api.v1.models.completed_job.CompletedJob._job_properties')
    @patch('foundations_internal.scheduler.Scheduler.get_job_information')
    def test_all_returns_multiple_jobs(self, mock_get_job_information, mock_job_properties, mock_pipeline_contexts):
        from datetime import datetime

        mock_pipeline_contexts.return_value = [('who', 'cares')]

        mock_job_properties.return_value = {
            'project_name': 'random test project',
            'job_id': 'my job',
            'user': 'Unspecified',
            'job_parameters': {},
            'input_params': [],
            'output_metrics': {'loss': 15.33},
            'status': 'Completed',
            'start_time': datetime.utcfromtimestamp(123456789).isoformat(),
            'completed_time': datetime.utcfromtimestamp(2222222222).isoformat()
        }

        mock_get_job_information.return_value = iter([
            self.MockJob(
            uuid=lambda: '00000000-0000-0000-0000-000000000000',
            user_submitted=lambda: 'soju hero',
            job_parameters=[],
            input_params=[],
            output_metrics=[],
            status='Running',
            submission_datetime=lambda: datetime.utcfromtimestamp(999999999),
            completed_time=None
        )])

        expected_job_1 = Job(
            job_id='00000000-0000-0000-0000-000000000000',
            user='soju hero',
            start_time=datetime.utcfromtimestamp(999999999).isoformat(),
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
            start_time=datetime.utcfromtimestamp(123456789).isoformat(),
            completed_time=datetime.utcfromtimestamp(2222222222).isoformat()
        )


        result = Job.all().evaluate()
        expected_jobs = [expected_job_1, expected_job_2]
        self.assertEqual(expected_jobs, result)
