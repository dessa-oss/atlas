"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch
from foundations.models.completed_job_data_listing import CompletedJobDataListing
from foundations.job_data_redis import JobDataRedis
from foundations.job_data_shaper import JobDataShaper


class TestCompletedJobDataListing(unittest.TestCase):

    @patch.object(JobDataRedis, 'get_all_jobs_data')
    @patch.object(JobDataShaper, 'shape_data')
    def test_gets_completed_job_data(self, mock_shaper, mock):
        some_data = [{'data': 'here'}]
        mock.return_value = some_data
        some_shaped_data = [{'data': 'there'}]
        mock_shaper.return_value = some_shaped_data

        self.assertEqual(CompletedJobDataListing.completed_job_data(
            'project_name'), some_shaped_data)
        mock.assert_called_once()
        mock_shaper.assert_called_once()

    @patch.object(JobDataRedis, 'get_all_jobs_data')
    @patch.object(JobDataShaper, 'shape_data')
    def test_gets_completed_job_data_different_values(self,  mock_shaper, mock):
        some_data = [{'new': 'data'}]
        mock.return_value = some_data
        some_shaped_data = [{'new': 'data', 'newer': 'data'}]
        mock_shaper.return_value = some_shaped_data

        self.assertEqual(CompletedJobDataListing.completed_job_data(
            'another_project'), some_shaped_data)
        mock.assert_called_once()
        mock_shaper.assert_called_once()
