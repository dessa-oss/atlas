"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.redundant_execution_middleware import RedundantExecutionMiddleware

from test.shared_examples.test_middleware_callback import TestMiddlewareCallback


class TestRedundantExecutionMiddleware(unittest.TestCase, TestMiddlewareCallback):

    def setUp(self):
        from foundations.stage import Stage

        from uuid import uuid4

        self._uuid = str(uuid4())
        self._stage = Stage(None, self._uuid, self._function, self._function)

        self._called_callback = False
        self._callback_args = None
        self._callback_kwargs = None

    def test_executes_callback_only_once(self):
        middleware = self._make_middleware()
        middleware.call(None, None, None, (), {}, self._callback)
        self._called_callback = False
        middleware.call(None, None, None, (), {}, self._callback)
        self.assertFalse(self._called_callback)

    def test_calls_returns_stored_callback_result(self):
        middleware = self._make_middleware()
        middleware.call(None, None, None, (), {}, self._callback)
        result = middleware.call(None, None, None, (), {}, self._callback)
        self.assertEqual(self._callback_result, result)

    def _function(self):
        pass

    def _make_middleware(self):
        return RedundantExecutionMiddleware(self._stage)
