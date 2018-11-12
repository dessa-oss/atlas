"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

import unittest
from mock import patch
from foundations_rest_api.v1.controllers.jobs_controller import JobsController
from foundations_rest_api.v1.models.property_model import PropertyModel


class TestJobsController(unittest.TestCase):

    class Mock(PropertyModel):
        name = PropertyModel.define_property()
        jobs = PropertyModel.define_property()
        garbage = PropertyModel.define_property()

    def _make_response(self, name, jobs=[]):
        from foundations_rest_api.response import Response

        def _callback():
            return self.Mock(name=name,
                             jobs=jobs)
        return Response('Mock', _callback)

    @patch('foundations_rest_api.v1.models.project.Project.find_by')
    def test_index_returns_only_completed_jobs(self, mock):
        mock.return_value = self._make_response(
            'some project',
            jobs = ['completed job 1', 'running job 2'])

        controller = JobsController()
        controller.params = {'project_name': 'the great potato project'}

        expected_result = {
            'jobs': ['completed job 1', 'running job 2'], 'name': 'some project'}
        self.assertEqual(expected_result, controller.index().as_json())
        mock.assert_called_with(name='the great potato project')

    @patch('foundations_rest_api.v1.models.project.Project.find_by')
    def test_index_returns_only_running_jobs(self, mock):
        mock.return_value = self._make_response(
            'some project',
            jobs = ['completed job 1', 'running job 2'])

        controller = JobsController()
        controller.params = {'project_name': 'the not so great potato project'}

        expected_result = {
            'jobs': ['completed job 1', 'running job 2'], 'name': 'some project'}
        self.assertEqual(expected_result, controller.index().as_json())
        mock.assert_called_with(name='the not so great potato project')




