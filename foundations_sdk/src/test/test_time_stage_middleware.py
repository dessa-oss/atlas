"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.time_stage_middleware import TimeStageMiddleware
from foundations.stage_context import StageContext

from test.shared_examples.test_middleware_callback import TestMiddlewareCallback


class TestTimeStageMiddleware(unittest.TestCase, TestMiddlewareCallback):

    class MockStageContext(StageContext):

        def time_callback(self, callback):
            self.callback = callback
            self.callback()

    def setUp(self):
        from foundations.stage import Stage

        from uuid import uuid4

        self._stage_context = self.MockStageContext()
        self._uuid = str(uuid4())
        self._stage = Stage(None, self._uuid, self._function, self._function)

        self._called_callback = False
        self._callback_args = None
        self._callback_kwargs = None

    def test_calls_time_callback_with_callback(self):
        middleware = self._make_middleware()
        middleware.call(None, None, None, (), {}, self._callback)

        self._called_callback = False
        self._stage_context.callback()
        self.assertTrue(self._called_callback)

    def _function(self):
        pass

    def _make_middleware(self):
        return TimeStageMiddleware(self._stage_context, self._stage)
