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


    @patch('foundations.models.completed_job_data_listing.CompletedJobDataListing.completed_job_data')
    def test_get_metrics_for_all_jobs_returns_all_completed_job_data(self, mock):
        from pandas import DataFrame
        from pandas.util.testing import assert_frame_equal

        mock.return_value = [{'project_name': 'project1', 'stuff': 'more stuff'}]

        expected_result = DataFrame(mock.return_value)
        assert_frame_equal(expected_result, get_metrics_for_all_jobs('project1'))

    @patch('foundations.models.completed_job_data_listing.CompletedJobDataListing.completed_job_data')
    def test_get_metrics_for_all_jobs_returns_all_completed_job_data_different_data(self, mock):
        from pandas import DataFrame
        from pandas.util.testing import assert_frame_equal

        mock.return_value = [{'project_name': 'project2', 'stuff': 'a lot more stuff'}, {'project_name': 'project2', 'stuff': 'a little bit of stuff'}]

        expected_result = DataFrame(mock.return_value)
        assert_frame_equal(expected_result, get_metrics_for_all_jobs('project2'))

    @patch('foundations.models.completed_job_data_listing.CompletedJobDataListing.completed_job_data')
    def test_get_metrics_for_all_jobs_filters_to_project(self, mock):
        from pandas import DataFrame
        from pandas.util.testing import assert_frame_equal

        mock.return_value = [{'project_name': 'project1', 'stuff': 'a lot more stuff'}, {'project_name': 'project2', 'stuff': 'a little bit of stuff'}]

        expected_result = DataFrame([{'project_name': 'project1', 'stuff': 'a lot more stuff'}])
        assert_frame_equal(expected_result, get_metrics_for_all_jobs('project1'))

    def test_get_metrics_for_all_jobs_is_defined_globally(self):
        import foundations

        self.assertEqual(get_metrics_for_all_jobs, foundations.get_metrics_for_all_jobs)