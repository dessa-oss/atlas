"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.middleware_chain import MiddlewareChain


class TestMiddlewareChain(unittest.TestCase):

    class MockMiddleware(object):

        def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
            pass

    def setUp(self):
        from uuid import uuid4

        self._callback_args = None
        self._callback_kwargs = None
        self._callback_result = uuid4()

    def test_call_returns_callback_result(self):
        chain = MiddlewareChain()
        result = chain.call(None, None, None, None, None, self._callback)
        self.assertEqual(self._callback_result, result)

    def test_call_returns_callback_result_with_args(self):
        chain = MiddlewareChain()
        args = self._random_args()
        chain.call(None, None, None, args, None, self._callback)

        self.assertEqual(args, self._callback_args)

    def test_call_returns_callback_result_with_kwargs(self):
        chain = MiddlewareChain()
        kwargs = self._random_kwargs()
        chain.call(None, None, None, None, kwargs, self._callback)

        self.assertEqual(kwargs, self._callback_kwargs)

    def _random_args(self):
        import random
        from uuid import uuid4

        return [uuid4() for _ in range(random.randint(1, 5))]

    def _random_kwargs(self):
        import random
        from uuid import uuid4

        return {uuid4(): uuid4() for _ in range(random.randint(1, 5))}

    def _callback(self, args, kwargs):
        self._callback_args = args
        self._callback_kwargs = kwargs

        return self._callback_result
