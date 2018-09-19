"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch
from foundations_rest_api.v1.controllers.completed_jobs_controller import CompletedJobsController


def _mock_project(expected_name, result):
    def _mock(name):
        if expected_name == name:
            return result
        return None
    return _mock

class TestCompletedJobsController(unittest.TestCase):

    @patch('foundations_rest_api.v1.models.project.Project.find_by', _mock_project('the great potato project', 'some project'))
    def test_index_returns_all_completed_jobs(self):
        controller = CompletedJobsController()
        controller.params = {'project_name': 'the great potato project'}
        self.assertEqual('some project', controller.index())

    @patch('foundations_rest_api.v1.models.project.Project.find_by', _mock_project('the not so great potato project', 'some other project'))
    def test_index_returns_all_completed_jobs_different_value(self):
        controller = CompletedJobsController()
        controller.params = {'project_name': 'the not so great potato project'}
        self.assertEqual('some other project', controller.index())
