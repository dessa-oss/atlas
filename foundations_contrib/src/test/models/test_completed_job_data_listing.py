"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch
from foundations_contrib.models.completed_job_data_listing import CompletedJobDataListing
from foundations_contrib.job_data_redis import JobDataRedis
from foundations_contrib.job_data_shaper import JobDataShaper
from foundations_contrib.format_input_parameters import FormatInputParameters


class TestCompletedJobDataListing(unittest.TestCase):

    @patch.object(FormatInputParameters, 'format_input_parameters')
    @patch.object(JobDataRedis, 'get_all_jobs_data')
    @patch.object(JobDataShaper, 'shape_output_metrics')
    def test_gets_completed_job_data(self, mock_shaper, mock, mock_input_param_formatter):
        some_data = [{'input_params': 'here', 'job_parameters': 'something', 'output_metrics': 'idk'}]
        mock.return_value = some_data
        mock_shaper.return_value = 'idk'
        mock_input_param_formatter.return_value = 'here'

        some_shaped_data = [{'input_params': 'here', 'job_parameters': 'something', 'output_metrics': 'idk'}]

        self.assertEqual(CompletedJobDataListing.completed_job_data(
            'project_name'), some_shaped_data)

        mock.assert_called_once()
        mock_shaper.assert_called_once()
        mock_input_param_formatter.assert_called_once()

    @patch.object(FormatInputParameters, 'format_input_parameters')
    @patch.object(JobDataRedis, 'get_all_jobs_data')
    @patch.object(JobDataShaper, 'shape_output_metrics')
    def test_gets_completed_job_data_different_values(self,  mock_shaper, mock, mock_input_param_formatter):
        some_data = [{'input_params': 'why', 'job_parameters': 'where', 'output_metrics': 'how'}]
        mock.return_value = some_data
        mock_shaper.return_value = 'how'
        mock_input_param_formatter.return_value = 'why'

        some_shaped_data = [{'input_params': 'why', 'job_parameters': 'where', 'output_metrics': 'how'}]

        self.assertEqual(CompletedJobDataListing.completed_job_data(
            'project_name'), some_shaped_data)

        mock.assert_called_once()
        mock_shaper.assert_called_once()
        mock_input_param_formatter.assert_called_once()
