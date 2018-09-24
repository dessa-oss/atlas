"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch

from foundations.null_stage_logger import NullStageLogger


class TestNullStageLogger(unittest.TestCase):

    class MockLogger(object):

        def __init__(self):
            self.log = None
            self.name = None

        def warn(self, message):
            self.log = message

    def setUp(self):
        self._mock_logger = self.MockLogger()

    @patch('foundations.log_manager.get_logger')
    def test_log_metric_warn_stage_context(self, mock):
        mock.side_effect = self._logger

        NullStageLogger().log_metric('loss', 0.56)
        self.assertEqual(
            'Tried to save metric `loss` outside the context of a stage', self._mock_logger.log)

    @patch('foundations.log_manager.get_logger')
    def test_log_metric_warn_stage_context_different_metric(self, mock):
        mock.side_effect = self._logger

        NullStageLogger().log_metric('win', 0.98856)
        self.assertEqual(
            'Tried to save metric `win` outside the context of a stage', self._mock_logger.log)

    @patch('foundations.log_manager.get_logger')
    def test_log_metric_uses_correct_logger(self, mock):
        mock.side_effect = self._logger

        NullStageLogger().log_metric('win', 0.98856)
        self.assertEqual('foundations.null_stage_logger', self._mock_logger.name)

    def test_pipeline_context_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            NullStageLogger().pipeline_context()

    def test_stage_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            NullStageLogger().stage()

    def test_stage_context_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            NullStageLogger().stage_context()

    def test_stage_config_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            NullStageLogger().stage_config()

    def _logger(self, name):
        self._mock_logger.name = name
        return self._mock_logger
