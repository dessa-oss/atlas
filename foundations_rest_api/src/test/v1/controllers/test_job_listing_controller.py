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

    def _make_response(self, name, queued_jobs=[], running_jobs=[], completed_jobs=[]):
        from foundations_rest_api.response import Response

        def _callback():
            return self.Mock(name=name,
                             queued_jobs=queued_jobs,
                             running_jobs=running_jobs,
                             completed_jobs=completed_jobs)
        return Response('Mock', _callback)

    @patch('foundations_rest_api.v1.models.project.Project.find_by')
    def test_index_returns_only_completed_jobs(self, mock):
        mock.return_value = self._make_response(
            'some project',
            queued_jobs = ['queued job 1', 'queued job 2'],
            completed_jobs = ['completed job 1', 'completed jobs 2'])

        controller = JobsController()
        controller.params = {'project_name': 'the great potato project'}

        expected_result = {
            'jobs': ['completed job 1', 'completed job 2'], 'name': 'some project'}
        self.assertEqual(expected_result, controller.index().as_json())
        mock.assert_called_with(name='the great potato project')

    @patch('foundations_rest_api.v1.models.project.Project.find_by')
    def test_index_returns_only_running_jobs(self, mock):
        mock.return_value = self._make_response(
            'some project',
            queued_jobs = ['queued job 1', 'queued job 2'],
            running_jobs = ['running job 1', 'running jobs 2'])

        controller = JobsController()
        controller.params = {'project_name': 'the great potato project'}

        expected_result = {
            'jobs': ['running job 1', 'running job 2'], 'name': 'some project'}
        self.assertEqual(expected_result, controller.index().as_json())
        mock.assert_called_with(name='the great potato project')

    @patch('foundations_rest_api.v1.models.project.Project.find_by')
    def test_index_returns_mixed_status_jobs(self, mock):
        mock.return_value = self._make_response(
            'some project',
            queued_jobs = ['queued job 1', 'queued job 2'],
            running_jobs = ['running job 1'] ,
            completed_jobs = ['completed job 1'])

        controller = JobsController()
        controller.params = {'project_name': 'the great potato project'}

        expected_result = {
            'jobs': ['running job 1', 'completed job 2'], 'name': 'some project'}
        self.assertEqual(expected_result, controller.index().as_json())
        mock.assert_called_with(name='the great potato project')

    @patch('foundations_rest_api.v1.models.project.Project.find_by')
    def test_index_returns_empty_job_listing(self, mock):
        mock.return_value = self._make_response('some project')

        controller = JobsController()
        controller.params = {'project_name': 'the not so great potato project'}

        expected_result = {'jobs': [],
                           'name': 'some other project'}
        self.assertEqual(expected_result, controller.index().as_json())
        mock.assert_called_with(name='the not so great potato project')
