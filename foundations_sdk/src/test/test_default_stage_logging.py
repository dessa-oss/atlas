"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch

from foundations.stage_logging import log_metric


class TestDefaultStageLogging(unittest.TestCase):

    class MockLoggingContext(object):

        def __init__(self):
            self.metric = None

        def log_metric(self, key, value):
            self.metric = {key: value}

    def test_context_is_stage_logging_context(self):
        from foundations.stage_logging import stage_logging_context
        from foundations.stage_logging_context import StageLoggingContext

        self.assertTrue(isinstance(stage_logging_context, StageLoggingContext))

    @patch('foundations.null_stage_logger.NullStageLogger.log_metric')
    def test_context_log_metric_uses_null_implementation(self, mock):
        from foundations.stage_logging import stage_logging_context

        stage_logging_context.log_metric('loss', 9.55)
        mock.assert_called_with('loss', 9.55)

    @patch('foundations.null_stage_logger.NullStageLogger.log_metric')
    def test_context_log_metric_uses_null_implementation_different_metric(self, mock):
        from foundations.stage_logging import stage_logging_context

        stage_logging_context.log_metric('gain', 999999.55)
        mock.assert_called_with('gain', 999999.55)

    @patch('foundations.stage_logging.stage_logging_context', MockLoggingContext())
    def test_log_metric_forwards_to_context(self):
        from foundations.stage_logging import stage_logging_context

        log_metric('loss', 9.44)
        self.assertEqual({'loss': 9.44}, stage_logging_context.metric)

    @patch('foundations.stage_logging.stage_logging_context', MockLoggingContext())
    def test_log_metric_forwards_to_context_different_metric(self):
        from foundations.stage_logging import stage_logging_context

        log_metric('rocauc', 343434)
        self.assertEqual({'rocauc': 343434}, stage_logging_context.metric)

    def test_global_log_metric_uses_log_metric(self):
        import foundations
        self.assertEqual(foundations.log_metric, log_metric)
