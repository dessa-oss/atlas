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
            {'name': 'b', 'stage_uuid': '1', 'value': {'type': 'stage', 'stage_name': 'stagely'}},
            {'name': 'c', 'stage_uuid': '2', 'value': {'type': 'dynamic', 'name': 'a'}},
            {'name': 'd', 'stage_uuid': '3', 'value': {'type': 'constant', 'value': 35}},
        ]
        output_metrics = {'loss': 100}
        mock.return_value = [{'project_name': 'project1', 'job_parameters': {
            'a': 5}, 'input_params': input_params, 'output_metrics': output_metrics}]

        expected_result = DataFrame(
            [{'project_name': 'project1', 'b': 'stagely', 'c': 5, 'd': 35, 'loss': 100}])
        assert_frame_equal(expected_result, get_metrics_for_all_jobs(
            'project1'), check_like=True)

    @patch('foundations_contrib.models.completed_job_data_listing.CompletedJobDataListing.completed_job_data')
    def test_get_metrics_for_all_jobs_returns_all_completed_job_data_with_two_variables_same_name(self, mock):
        from pandas import DataFrame
        from pandas.util.testing import assert_frame_equal

        input_params = [
            {'name': 'b', 'stage_uuid': '1', 'value': {'type': 'stage', 'stage_name': 'stagely'}},
            {'name': 'c', 'stage_uuid': '2', 'value': {'type': 'dynamic', 'name': 'a'}},
            {'name': 'd', 'stage_uuid': '3', 'value': {'type': 'constant', 'value': 35}},
            {'name': 'd', 'stage_uuid': '4', 'value': {'type': 'constant', 'value': 45}},
        ]
        output_metrics = {'loss': 100}
        mock.return_value = [{'project_name': 'project1', 'job_parameters': {
            'a': 5}, 'input_params': input_params, 'output_metrics': output_metrics}]

        expected_result = DataFrame(
            [{'d': 35, 'd-1': 45, 'project_name': 'project1', 'loss': 100, 'c': 5, 'b': 'stagely'}])
        assert_frame_equal(expected_result, get_metrics_for_all_jobs(
            'project1'), check_like=True)

    @patch('foundations_contrib.models.completed_job_data_listing.CompletedJobDataListing.completed_job_data')
    def test_get_metrics_for_all_jobs_returns_all_completed_job_data_with_two_variables_same_name_different_position_in_list(self, mock):
        from pandas import DataFrame
        from pandas.util.testing import assert_frame_equal

        input_params = [
            {'name': 'b', 'stage_uuid': '3', 'value': {'type': 'stage', 'stage_name': 'stagely'}},
            {'name': 'c', 'stage_uuid': '2', 'value': {'type': 'dynamic', 'name': 'a'}},
            {'name': 'd', 'stage_uuid': '1', 'value': {'type': 'constant', 'value': 35}},
            {'name': 'd', 'stage_uuid': '4', 'value': {'type': 'constant', 'value': 45}},
        ]
        output_metrics = {'loss': 100}
        mock.return_value = [{'project_name': 'project1', 'job_parameters': {
            'a': 5}, 'input_params': input_params, 'output_metrics': output_metrics}]

        expected_result = DataFrame(
            [{'d': 35, 'd-1': 45, 'project_name': 'project1', 'loss': 100, 'c': 5, 'b': 'stagely'}])
        assert_frame_equal(expected_result, get_metrics_for_all_jobs(
            'project1'), check_like=True)

    @patch('foundations_contrib.models.completed_job_data_listing.CompletedJobDataListing.completed_job_data')
    def test_get_metrics_for_all_jobs_returns_all_completed_job_data_with_two_variables_same_name_same_different_position(self, mock):
        from pandas import DataFrame
        from pandas.util.testing import assert_frame_equal

        input_params = [
            {'name': 'b', 'stage_uuid': '2', 'value': {'type': 'stage', 'stage_name': 'stagely'}},
            {'name': 'c', 'stage_uuid': '1', 'value': {'type': 'dynamic', 'name': 'a'}},
            {'name': 'd', 'stage_uuid': '3', 'value': {'type': 'constant', 'value': 35}},
            {'name': 'd', 'stage_uuid': '3', 'value': {'type': 'constant', 'value': 45}},
        ]
        output_metrics = {'loss': 100}
        mock.return_value = [{'project_name': 'project1', 'job_parameters': {
            'a': 5}, 'input_params': input_params, 'output_metrics': output_metrics}]

        expected_result = DataFrame(
            [{'d': 35, 'd-1': 45, 'project_name': 'project1', 'loss': 100, 'c': 5, 'b': 'stagely'}])
        assert_frame_equal(expected_result, get_metrics_for_all_jobs(
            'project1'), check_like=True)

    @patch('foundations_contrib.models.completed_job_data_listing.CompletedJobDataListing.completed_job_data')
    def test_get_metrics_for_all_jobs_returns_all_completed_job_data_different_data(self, mock):
        from pandas import DataFrame
        from pandas.util.testing import assert_frame_equal

        input_params = [
            {'name': 'b', 'stage_uuid': '1', 'value': {'type': 'stage', 'stage_name': 'stagely'}},
            {'name': 'c', 'stage_uuid': '2', 'value': {'type': 'dynamic', 'name': 'a'}},
            {'name': 'd', 'stage_uuid': '3', 'value': {'type': 'constant', 'value': 35}},
        ]
        output_metrics = {'loss': 100}
        input_params_2 = [
            {'name': 'd', 'stage_uuid': '4', 'value': {'type': 'stage', 'stage_name': 'another stagel'}},
            {'name': 'e', 'stage_uuid': '5', 'value': {'type': 'dynamic', 'name': 'bad'}},
            {'name': 'f', 'stage_uuid': '6', 'value': {'type': 'constant', 'value': 97}},
        ]
        output_metrics_2 = {'win': 56}
        mock.return_value = [
            {'project_name': 'project2', 'job_parameters': {'a': 5},
                'input_params': input_params, 'output_metrics': output_metrics},
            {'project_name': 'project2', 'job_parameters': {'bad': 77},
                'input_params': input_params_2, 'output_metrics': output_metrics_2},
        ]

        expected_data = [
            {'project_name': 'project2', 'b': 'stagely',
                'loss': 100, 'd': 35, 'c': 5},
            {'e': 77, 'project_name': 'project2',
                'win': 56, 'd': 'another stagel', 'f': 97},
        ]
        expected_result = DataFrame(expected_data)
        assert_frame_equal(expected_result, get_metrics_for_all_jobs(
            'project2'), check_like=True)

    @patch('foundations_contrib.models.completed_job_data_listing.CompletedJobDataListing.completed_job_data')
    def test_get_metrics_for_all_jobs_correct_order(self, mock):
        from pandas import DataFrame
        from pandas.util.testing import assert_frame_equal

        input_params = [
            {'name': 'b', 'stage_uuid': '1', 'value': {'type': 'stage', 'stage_name': 'stagely'}},
            {'name': 'c', 'stage_uuid': '2', 'value': {'type': 'dynamic', 'name': 'a'}},
            {'name': 'd', 'stage_uuid': '3', 'value': {'type': 'constant', 'value': 35}},
        ]
        output_metrics = {'loss': 100}

        mock.return_value = [
            {'project_name': 'project1', 'job_parameters': {'a': 5},
                'input_params': input_params, 'output_metrics': output_metrics}
        ]

        expected_data = [
            {'project_name': 'project1', 'b': 'stagely',
                'c': 5, 'd': 35, 'loss': 100},
        ]
        expected_result = DataFrame(expected_data, columns=[
                                    'project_name', 'b', 'c', 'd', 'loss'])
        assert_frame_equal(
            expected_result, get_metrics_for_all_jobs('project1'))

    def test_get_metrics_for_all_jobs_is_defined_globally(self):
        import foundations

        self.assertEqual(get_metrics_for_all_jobs,
                         foundations.get_metrics_for_all_jobs)
