"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.middleware.upstream_result_middleware import UpstreamResultMiddleware

from test.shared_examples.test_callback import TestCallback


class TestUpstreamResultMiddleware(unittest.TestCase, TestCallback):

    def setUp(self):
        from uuid import uuid4

        self._result = uuid4()

        self._called_callback = False
        self._callback_args = None
        self._callback_kwargs = None

    def test_calls_callback(self):
        middleware = self._make_middleware()
        middleware.call(self._upstream_result, None,
                        None, (), {}, self._callback)
        self.assertTrue(self._called_callback)

    def test_calls_callback_with_args(self):
        middleware = self._make_middleware()
        middleware.call(self._upstream_result, None, None, ('hello', 'world'),
                        {}, self._callback)
        self.assertEqual((self._result, 'hello', 'world'), self._callback_args)

    def test_calls_callback_with_list_args(self):
        middleware = self._make_middleware()
        middleware.call(self._upstream_result, None, None, ['hello', 'world'],
                        {}, self._callback)
        self.assertEqual((self._result, 'hello', 'world'), self._callback_args)

    def test_calls_callback_with_different_args(self):
        middleware = self._make_middleware()
        middleware.call(self._upstream_result, None, None,
                        ('goodbye',), {}, self._callback)
        self.assertEqual((self._result, 'goodbye'), self._callback_args)

    def test_calls_callback_with_kwargs(self):
        middleware = self._make_middleware()
        middleware.call(self._upstream_result, None, None, (), {
                        'hello': 'world'}, self._callback)
        self.assertEqual({'hello': 'world'}, self._callback_kwargs)

    def test_calls_callback_with_different_kwargs(self):
        middleware = self._make_middleware()
        middleware.call(self._upstream_result, None, None, (), {
                        'basket': 'case'}, self._callback)
        self.assertEqual({'basket': 'case'}, self._callback_kwargs)

    def test_calls_returns_callback_result(self):
        middleware = self._make_middleware()
        result = middleware.call(
            self._upstream_result, None, None, (), {}, self._callback)
        self.assertEqual(self._callback_result, result)

    def _upstream_result(self):
        return (self._result,)

    def _function(self):
        pass

    def _make_middleware(self):
        return UpstreamResultMiddleware()
