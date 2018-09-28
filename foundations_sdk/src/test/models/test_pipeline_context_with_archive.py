"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch

from foundations.models.pipeline_context_with_archive import PipelineContextWithArchive

class TestPipelineContextWithArchive(unittest.TestCase):

    class MockArchive(object):
        pass

    def setUp(self):
        self._archive = self.MockArchive()
        self._context = PipelineContextWithArchive(self._archive)

    @patch('foundations.pipeline_context.PipelineContext.load_stage_log_from_archive')
    def test_wraps_load_stage_log_from_archive(self, mock):
        self._context.load_stage_log_from_archive()
        mock.assert_called_with(self._archive)

    @patch('foundations.pipeline_context.PipelineContext.load_persisted_data_from_archive')
    def test_wraps_load_persisted_data_from_archive(self, mock):
        self._context.load_persisted_data_from_archive()
        mock.assert_called_with(self._archive)

    @patch('foundations.pipeline_context.PipelineContext.load_provenance_from_archive')
    def test_wraps_load_provenance_from_archive(self, mock):
        self._context.load_provenance_from_archive()
        mock.assert_called_with(self._archive)

    @patch('foundations.pipeline_context.PipelineContext.load_job_source_from_archive')
    def test_wraps_load_job_source_from_archive(self, mock):
        self._context.load_job_source_from_archive()
        mock.assert_called_with(self._archive)

    @patch('foundations.pipeline_context.PipelineContext.load_artifact_from_archive')
    def test_wraps_load_artifact_from_archive(self, mock):
        self._context.load_artifact_from_archive()
        mock.assert_called_with(self._archive)

    @patch('foundations.pipeline_context.PipelineContext.load_miscellaneous_from_archive')
    def test_wraps_load_miscellaneous_from_archive(self, mock):
        self._context.load_miscellaneous_from_archive()
        mock.assert_called_with(self._archive)

    @patch('foundations.pipeline_context.PipelineContext.load_from_archive')
    def test_wraps_load_from_archive(self, mock):
        self._context.load_from_archive()
        mock.assert_called_with(self._archive)