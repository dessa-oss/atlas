"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from test.shared_examples.test_callback import TestCallback


class TestMiddlewareCallback(TestCallback):

    class MockFiller(object):

        def __init__(self, *args, **kwargs):
            self._args = args
            self._kwargs = kwargs

        def fill(self, **filler_kwargs):
            return (self._args, self._kwargs)

    def test_calls_callback(self):
        middleware = self._make_middleware()
        middleware.call(None, self.MockFiller, {}, (), {}, self._callback)
        self.assertTrue(self._called_callback)

    def test_calls_callback_with_args(self):
        middleware = self._make_middleware()
        middleware.call(None, self.MockFiller, {}, ('hello', 'world'),
                        {}, self._callback)
        self.assertEqual(('hello', 'world'), self._callback_args)

    def test_calls_callback_with_different_args(self):
        middleware = self._make_middleware()
        middleware.call(None, self.MockFiller, {},
                        ('goodbye',), {}, self._callback)
        self.assertEqual(('goodbye',), self._callback_args)

    def test_calls_callback_with_kwargs(self):
        middleware = self._make_middleware()
        middleware.call(None, self.MockFiller, {}, (), {
                        'hello': 'world'}, self._callback)
        self.assertEqual({'hello': 'world'}, self._callback_kwargs)

    def test_calls_callback_with_different_kwargs(self):
        middleware = self._make_middleware()
        middleware.call(None, self.MockFiller, {}, (), {
                        'basket': 'case'}, self._callback)
        self.assertEqual({'basket': 'case'}, self._callback_kwargs)

    def test_calls_returns_callback_result(self):
        middleware = self._make_middleware()
        result = middleware.call(
            None, self.MockFiller, {}, (), {}, self._callback)
        self.assertEqual(self._callback_result, result)

    def assertTrue(self, value):
        raise NotImplementedError()

    def assertEqual(self, lhs, rhs):
        raise NotImplementedError()

    def _make_middleware(self):
        raise NotImplementedError()
