"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch
from foundations_rest_api.v1.controllers.completed_jobs_controller import CompletedJobsController


class TestCompletedJobsController(unittest.TestCase):

    @patch('foundations_rest_api.v1.models.completed_job.CompletedJob.all', lambda: 'some completed jobs')
    def test_index_returns_all_completed_jobs(self):
        controller = CompletedJobsController()
        self.assertEqual('some completed jobs', controller.index())

    @patch('foundations_rest_api.v1.models.completed_job.CompletedJob.all', lambda: 'some other completed jobs')
    def test_index_returns_all_completed_jobs_different_value(self):
        controller = CompletedJobsController()
        self.assertEqual('some other completed jobs', controller.index())
