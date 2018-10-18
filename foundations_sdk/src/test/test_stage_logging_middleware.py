"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.stage_logging_middleware import StageLoggingMiddleware

from test.shared_examples.test_middleware_callback import TestMiddlewareCallback

from mock import patch, call


class TestStageLoggingMiddleware(unittest.TestCase, TestMiddlewareCallback):

    def setUp(self):
        from foundations.stage import Stage

        from uuid import uuid4

        self._uuid = str(uuid4())
        self._stage = Stage(None, self._uuid, self._function, self._function)

        self._called_callback = False
        self._callback_args = None
        self._callback_kwargs = None

    def _function(self):
        pass

    def _make_middleware(self):
        return StageLoggingMiddleware(self._stage)

    class MockStage(object):

        def __init__(self, uuid, function_name, source_file, source_line):
            self._uuid = uuid
            self._function_name = function_name
            self._source_file = source_file
            self._source_line = source_line
        
        def uuid(self):
            return self._uuid
        
        def function_name(self):
            return self._function_name

        def source_file(self):
            return self._source_file

        def source_line(self):
            return self._source_line

    @patch('logging.Logger.info')
    def test_stage_logging_middleware_begin_end_info_logs(self, mock):

        def dummy(*args,**kwargs):
            return 3

        mock_stage = self.MockStage(uuid = '123', function_name = 'hello', source_file = 'hello.py', source_line = 10)
        StageLoggingMiddleware(mock_stage).call(None, None, None, None, None, callback = dummy)

        message1 = call('Running stage `%s` (uuid: `%s`), file: %s, line: %s', 'hello', '123', 'hello.py', 10)
        message2 = call('Finished stage %s (uuid: %s)', 'hello', '123')

        mock.assert_has_calls([message1, message2])

    @patch('logging.Logger.info')
    def test_stage_logging_middleware_begin_end_info_logs_different_values(self, mock):

        def dummy(*args,**kwargs):
            return 3

        mock_stage = self.MockStage(uuid = '781', function_name = 'goodbye', source_file = 'hello.py', source_line = 109)
        StageLoggingMiddleware(mock_stage).call(None, None, None, None, None, callback = dummy)

        message1 = call('Running stage `%s` (uuid: `%s`), file: %s, line: %s', 'goodbye', '781', 'hello.py', 109)
        message2 = call('Finished stage %s (uuid: %s)', 'goodbye', '781')

        mock.assert_has_calls([message1, message2])