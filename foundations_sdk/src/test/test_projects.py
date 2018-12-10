"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch

from foundations.projects import set_project_name
from foundations.projects import get_metrics_for_all_jobs


class TestProjects(unittest.TestCase):

    def test_set_project_name_sets_project_name(self):
        from foundations.global_state import foundations_context

        set_project_name('some project')
        self.assertEqual(
            'some project', foundations_context.pipeline_context().provenance.project_name)

    def test_set_project_name_sets_project_name_different_name(self):
        from foundations.global_state import foundations_context

        set_project_name('some different project name')
        self.assertEqual('some different project name',
                         foundations_context.pipeline_context().provenance.project_name)

    def test_set_project_name_is_global(self):
        from foundations.global_state import foundations_context
        import foundations

        foundations.set_project_name('some project')
        self.assertEqual(
            'some project', foundations_context.pipeline_context().provenance.project_name)

    def test_set_project_name_is_global(self):
        from foundations.global_state import foundations_context
        import foundations

        foundations.set_project_name('some different project name')
        self.assertEqual('some different project name',
                         foundations_context.pipeline_context().provenance.project_name)

    @patch('foundations_contrib.models.completed_job_data_listing.CompletedJobDataListing.completed_job_data')
    def test_get_metrics_for_all_jobs_returns_all_completed_job_data(self, mock):
        from pandas import DataFrame, concat
        from pandas.util.testing import assert_frame_equal

        input_params = [
            {'name': 'b', 'value': '1', 'type': 'string', 'source': 'constant'},
            {'name': 'c', 'value': '2', 'type': 'string', 'source': 'constant'},
            {'name': 'd', 'value': '3', 'type': 'string', 'source': 'constant'},
        ]
        output_metrics = {'loss': 100}
        mock.return_value = [{'project_name': 'project1', 'job_parameters': {
            'a': 5}, 'input_params': input_params, 'output_metrics': output_metrics}]

        expected_result = DataFrame(
            [{'project_name': 'project1', 'b': '1', 'c': '2', 'd': '3', 'loss': 100}])
        assert_frame_equal(expected_result, get_metrics_for_all_jobs(
            'project1'), check_like=True)

    @patch('foundations_contrib.models.completed_job_data_listing.CompletedJobDataListing.completed_job_data')
    def test_get_metrics_for_all_jobs_returns_all_completed_job_data_with_two_variables_same_name_different_position_in_list(self, mock):
        from pandas import DataFrame
        from pandas.util.testing import assert_frame_equal

        input_params = [
            {'name': 'b', 'value': '3', 'type': 'string', 'source': 'constant'},
            {'name': 'c', 'value': '2', 'type': 'string', 'source': 'constant'},
            {'name': 'd-0', 'value': '1', 'type': 'string', 'source': 'constant'},
            {'name': 'd-1', 'value': '4', 'type': 'string', 'source': 'constant'},
        ]
        output_metrics = {'loss': 100}
        mock.return_value = [{'project_name': 'project1', 'job_parameters': {
            'a': 5}, 'input_params': input_params, 'output_metrics': output_metrics}]

        expected_result = DataFrame(
            [{'d-0': '1', 'd-1': '4', 'project_name': 'project1', 'loss': 100, 'c': '2', 'b': '3'}])
        assert_frame_equal(expected_result, get_metrics_for_all_jobs(
            'project1'), check_like=True)


    @patch('foundations_contrib.models.completed_job_data_listing.CompletedJobDataListing.completed_job_data')
    def test_get_metrics_for_all_jobs_returns_all_completed_job_data_different_data(self, mock):
        from pandas import DataFrame
        from pandas.util.testing import assert_frame_equal

        input_params = [
            {'name': 'b-0', 'value': '1', 'type': 'string', 'source': 'constant'},
            {'name': 'c-1', 'value': '2', 'type': 'string', 'source': 'constant'},
            {'name': 'd-2', 'value': '3', 'type': 'string', 'source': 'constant'},
        ]
        output_metrics = {'loss': 100}
        input_params_2 = [
            {'name': 'd-3', 'value': '4', 'type': 'string', 'source': 'constant'},
            {'name': 'e-4', 'value': '5', 'type': 'string', 'source': 'constant'},
            {'name': 'f-5', 'value': '6', 'type': 'string', 'source': 'constant'},
        ]
        output_metrics_2 = {'win': 56}
        mock.return_value = [
            {'project_name': 'project2', 'job_parameters': {'a': 5},
                'input_params': input_params, 'output_metrics': output_metrics},
            {'project_name': 'project2', 'job_parameters': {'bad': 77},
                'input_params': input_params_2, 'output_metrics': output_metrics_2},
        ]

        expected_data = [
            {'project_name': 'project2', 'b-0': '1','loss': 100, 'd-2': '3', 'c-1': '2'},
            {'e-4': '5', 'project_name': 'project2','win': 56, 'd-3': '4', 'f-5': '6'},
        ]
        expected_result = DataFrame(expected_data)
        assert_frame_equal(expected_result, get_metrics_for_all_jobs(
            'project2'), check_like=True)

    @patch('foundations_contrib.models.completed_job_data_listing.CompletedJobDataListing.completed_job_data')
    def test_get_metrics_for_all_jobs_correct_order(self, mock):
        from pandas import DataFrame
        from pandas.util.testing import assert_frame_equal

        input_params = [
            {'name': 'b-0', 'value': '1', 'type': 'string', 'source': 'constant'},
            {'name': 'c-1', 'value': '2', 'type': 'string', 'source': 'constant'},
            {'name': 'd-2', 'value': '3', 'type': 'string', 'source': 'constant'}
        ]
        output_metrics = {'loss': 100}

        mock.return_value = [
            {'project_name': 'project1', 'job_parameters': {'a': 5},
                'input_params': input_params, 'output_metrics': output_metrics}
        ]

        expected_data = [
            {'project_name': 'project1', 'b-0': '1',
                'c-1': '2', 'd-2': '3', 'loss': 100},
        ]
        expected_result = DataFrame(expected_data, columns=['project_name', 'b-0', 'c-1', 'd-2', 'loss'])
        assert_frame_equal(expected_result, get_metrics_for_all_jobs('project1'))

    def test_get_metrics_for_all_jobs_is_defined_globally(self):
        import foundations

        self.assertEqual(get_metrics_for_all_jobs, foundations.get_metrics_for_all_jobs)
