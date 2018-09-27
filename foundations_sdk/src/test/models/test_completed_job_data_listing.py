"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch
from foundations.models.completed_job_data_listing import CompletedJobDataListing


class TestCompletedJobDataListing(unittest.TestCase):

    class MockCompletedJobData(object):

        def __init__(self, job_id, context):
            self._job_id = job_id
            self._context = context

        def load_job(self):
            return {'job_id': self._job_id, 'context': self._context}

    @patch('foundations.models.pipeline_context_listing.PipelineContextListing.pipeline_contexts')
    @patch('foundations.models.completed_job_data.CompletedJobData', MockCompletedJobData)
    def test_generate_completed_job_data_returns_empty_list(self, mock):
        mock.return_value = []
        self.assertEqual([], self._completed_job_list())

    @patch('foundations.models.pipeline_context_listing.PipelineContextListing.pipeline_contexts')
    @patch('foundations.models.completed_job_data.CompletedJobData', MockCompletedJobData)
    def test_generate_completed_job_data_returns_single_job_listing(self, mock):
        mock.return_value = [('job_name', 'context...')]

        expected_result = [{'job_id': 'job_name', 'context': 'context...'}]
        self.assertEqual(expected_result, self._completed_job_list())

    @patch('foundations.models.pipeline_context_listing.PipelineContextListing.pipeline_contexts')
    @patch('foundations.models.completed_job_data.CompletedJobData', MockCompletedJobData)
    def test_generate_completed_job_data_returns_different_single_job_listing(self, mock):
        mock.return_value = [('space2vec', 'space stuff')]

        expected_result = [{'job_id': 'space2vec', 'context': 'space stuff'}]
        self.assertEqual(expected_result, self._completed_job_list())

    @patch('foundations.models.pipeline_context_listing.PipelineContextListing.pipeline_contexts')
    @patch('foundations.models.completed_job_data.CompletedJobData', MockCompletedJobData)
    def test_generate_completed_job_data_returns_multiple_jobs(self, mock):
        mock.return_value = [('space2vec', 'space stuff'),
                             ('snowbork', 'snowbork stuff')]

        expected_result = [{'job_id': 'space2vec', 'context': 'space stuff'}, {
            'job_id': 'snowbork', 'context': 'snowbork stuff'}]
        self.assertEqual(expected_result, self._completed_job_list())

    def _completed_job_list(self):
        return list(CompletedJobDataListing.completed_job_data())
