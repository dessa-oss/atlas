"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import patch
from foundations.middleware.new_stage_log_middleware import NewStageLogMiddleware
from foundations.stage_logging_context import StageLoggingContext

from test.shared_examples.test_middleware_callback import TestMiddlewareCallback


class TestNewStageLogMiddleware(unittest.TestCase, TestMiddlewareCallback):

    class MockStageLoggingContext(StageLoggingContext):

        def __init__(self):
            from foundations.null_stage_logger import NullStageLogger
            super(self.__class__, self).__init__(NullStageLogger())

        def logger(self):
            return self._logger

    def setUp(self):
        from foundations.pipeline_context import PipelineContext
        from foundations.stage_config import StageConfig
        from foundations.stage_context import StageContext
        from foundations.stage import Stage

        from uuid import uuid4

        self._pipeline_context = PipelineContext()
        self._stage_config = StageConfig()
        self._stage_context = StageContext()
        self._uuid = str(uuid4())
        self._stage = Stage(None, self._uuid, self._function, self._function)

        self._mock_stage_cache = None
        self._called_callback = False
        self._callback_args = None
        self._callback_kwargs = None

    @patch('foundations.stage_logging.stage_logging_context', MockStageLoggingContext())
    def test_sets_stage_log_sets_stage(self):
        def method(args, kwargs):
            from foundations.stage_logging import stage_logging_context
            self.assertEqual(
                self._stage, stage_logging_context.logger().stage())

        middleware = self._make_middleware()
        middleware.call(None, None, None, (), {}, method)

    @patch('foundations.stage_logging.stage_logging_context', MockStageLoggingContext())
    def test_sets_stage_log_sets_stage_config(self):
        def method(args, kwargs):
            from foundations.stage_logging import stage_logging_context
            self.assertEqual(self._stage_config,
                             stage_logging_context.logger().stage_config())

        middleware = self._make_middleware()
        middleware.call(None, None, None, (), {}, method)

    @patch('foundations.stage_logging.stage_logging_context', MockStageLoggingContext())
    def test_sets_stage_log_sets_stage_context(self):
        def method(args, kwargs):
            from foundations.stage_logging import stage_logging_context
            self.assertEqual(self._stage_context,
                             stage_logging_context.logger().stage_context())

        middleware = self._make_middleware()
        middleware.call(None, None, None, (), {}, method)

    @patch('foundations.stage_logging.stage_logging_context', MockStageLoggingContext())
    def test_sets_stage_log_sets_pipeline_context(self):
        def method(args, kwargs):
            from foundations.stage_logging import stage_logging_context
            self.assertEqual(self._pipeline_context,
                             stage_logging_context.logger().pipeline_context())

        middleware = self._make_middleware()
        middleware.call(None, None, None, (), {}, method)

    def _function(self):
        pass

    def _make_middleware(self):
        return NewStageLogMiddleware(self._pipeline_context, self._stage_config, self._stage_context, self._stage)
