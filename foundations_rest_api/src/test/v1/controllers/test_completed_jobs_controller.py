"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch
from foundations_rest_api.v1.controllers.completed_jobs_controller import CompletedJobsController
from foundations_rest_api.v1.models.property_model import PropertyModel


class TestCompletedJobsController(unittest.TestCase):

    class Mock(PropertyModel):
        name = PropertyModel.define_property()
        completed_jobs = PropertyModel.define_property()
        garbage = PropertyModel.define_property()

    @patch('foundations_rest_api.v1.models.project.Project.find_by')
    def test_index_returns_all_completed_jobs(self, mock):
        mock.return_value = self._make_response('some project', 'some jobs')

        controller = CompletedJobsController()
        controller.params = {'project_name': 'the great potato project'}

        expected_result = {
            'completed_jobs': 'some jobs', 'name': 'some project'}
        self.assertEqual(expected_result, controller.index().as_json())
        mock.assert_called_with(name='the great potato project')

    @patch('foundations_rest_api.v1.models.project.Project.find_by')
    def test_index_returns_all_completed_jobs_different_value(self, mock):
        mock.return_value = self._make_response(
            'some other project', 'some more jobs')

        controller = CompletedJobsController()
        controller.params = {'project_name': 'the not so great potato project'}

        expected_result = {'completed_jobs': 'some more jobs',
                           'name': 'some other project'}
        self.assertEqual(expected_result, controller.index().as_json())
        mock.assert_called_with(name='the not so great potato project')

    def _make_response(self, name, completed_jobs):
        from foundations_rest_api.response import Response

        def _callback():
            return self.Mock(name=name, completed_jobs=completed_jobs)

        return Response('Mock', _callback)
