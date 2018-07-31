"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.context_aware_middleware import ContextAwareMiddleware

from test.shared_examples.test_middleware_callback import TestMiddlewareCallback


class TestContextAwareMiddleware(unittest.TestCase, TestMiddlewareCallback):

    def setUp(self):
        from foundations.stage_context import StageContext

        self._stage_context = StageContext()

        self._called_callback = False
        self._callback_args = None
        self._callback_kwargs = None

    def test_calls_callback_with_context(self):
        middleware = self._make_middleware(context_aware=True)
        middleware.call(None, None, None, ('hello', 'world'),
                        {}, self._callback)
        self.assertEqual((self._stage_context, 'hello',
                          'world'), self._callback_args)

    def test_calls_callback_with_context_with_different_args(self):
        middleware = self._make_middleware(context_aware=True)
        middleware.call(None, None, None, ('goodbye',), {}, self._callback)
        self.assertEqual((self._stage_context, 'goodbye'), self._callback_args)

    def _make_middleware(self, context_aware=False):
        from foundations.context_aware import ContextAware
        from foundations.stage import Stage

        method = self._method
        if context_aware:
            method = ContextAware(method)

        stage = Stage(None, None, method, method)

        return ContextAwareMiddleware(self._stage_context, stage)

    def _method(self, *args, **kwargs):
        pass
