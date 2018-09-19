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

    @patch('foundations_rest_api.v1.models.project.Project.find_by')
    def test_index_returns_all_completed_jobs(self, mock):
        mock.return_value = 'some project'

        controller = CompletedJobsController()
        controller.params = {'project_name': 'the great potato project'}

        self.assertEqual('some project', controller.index())
        mock.assert_called_with(name='the great potato project')

    @patch('foundations_rest_api.v1.models.project.Project.find_by')
    def test_index_returns_all_completed_jobs_different_value(self, mock):
        mock.return_value = 'some other project'

        controller = CompletedJobsController()
        controller.params = {'project_name': 'the not so great potato project'}

        self.assertEqual('some other project', controller.index())
        mock.assert_called_with(name='the not so great potato project')
