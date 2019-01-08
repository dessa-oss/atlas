"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""

import unittest
from mock import patch
from foundations_rest_api.v2beta.controllers.jobs_controller import JobsController
from foundations_rest_api.v2beta.models.property_model import PropertyModel


class TestJobsControllerV2(unittest.TestCase):

    class Mock(PropertyModel):
        name = PropertyModel.define_property()
        jobs = PropertyModel.define_property()
        input_parameter_names = PropertyModel.define_property()
        output_metric_names = PropertyModel.define_property()
        garbage = PropertyModel.define_property()

    def _make_lazy_result(self, name, jobs=[], input_parameter_names = [], output_metric_names = []):
        from foundations_rest_api.lazy_result import LazyResult

        def _callback():
            return self.Mock(name=name,
                             jobs=jobs,
                             output_metric_names = output_metric_names,
                             input_parameter_names = input_parameter_names)
        return LazyResult(_callback)

    @patch('foundations_rest_api.v2beta.models.project.Project.find_by')
    def test_index_returns_only_completed_jobs(self, mock):
        mock.return_value = self._make_lazy_result(
            'some project',
            jobs = ['completed job 1', 'running job 2'],
            input_parameter_names = 'param',
            output_metric_names = 'metrics'
        )

        controller = JobsController()
        controller.params = {'project_name': 'the great potato project'}

        expected_result = {
            'jobs': ['completed job 1', 'running job 2'], 'name': 'some project', 'input_parameter_names': 'param', 'output_metric_names': 'metrics'}
        self.assertEqual(expected_result, controller.index().as_json())
        mock.assert_called_with(name='the great potato project')

    @patch('foundations_rest_api.v2beta.models.project.Project.find_by')
    def test_index_returns_only_running_jobs(self, mock):
        mock.return_value = self._make_lazy_result(
            'some project',
            jobs = ['completed job 1', 'running job 2'])

        controller = JobsController()
        controller.params = {'project_name': 'the not so great potato project'}

        expected_result = {
            'jobs': ['completed job 1', 'running job 2'], 'name': 'some project', 'input_parameter_names': [], 'output_metric_names': []}
        self.assertEqual(expected_result, controller.index().as_json())
        mock.assert_called_with(name='the not so great potato project')
