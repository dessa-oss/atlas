"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_rest_api.v1.models.running_job import RunningJob


class TestRunningJob(unittest.TestCase):

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

    def test_all_is_empty_response(self):
        self.assertEqual([], RunningJob.all().evaluate())