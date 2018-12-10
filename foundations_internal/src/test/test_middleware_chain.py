"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations_internal.middleware_chain import MiddlewareChain


class TestMiddlewareChain(unittest.TestCase):

    class MockData(object):
        pass

    class MockMiddleware(object):

        def __init__(self):
            self.called = False
            self.upstream_result_callback = None
            self.filler_builder = None
            self.filler_kwargs = None

        def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
            self.called = True
            self.upstream_result_callback = upstream_result_callback
            self.filler_builder = filler_builder
            self.filler_kwargs = filler_kwargs

            return callback(args, kwargs)

    def setUp(self):
        from uuid import uuid4

        self._callback_args = None
        self._callback_kwargs = None
        self._callback_result = uuid4()

        self._middleware_chain = MiddlewareChain()
        self._middleware = self.MockMiddleware()
        self._middleware_chain.append_middleware(self._middleware)

    def test_call_returns_callback_result(self):
        result = self._middleware_chain.call(
            None, None, None, None, None, self._callback)
        self.assertEqual(self._callback_result, result)

    def test_call_returns_callback_result_with_args(self):
        args = self._random_args()
        self._middleware_chain.call(
            None, None, None, args, None, self._callback)

        self.assertEqual(args, self._callback_args)

    def test_call_returns_callback_result_with_kwargs(self):
        kwargs = self._random_kwargs()
        self._middleware_chain.call(
            None, None, None, None, kwargs, self._callback)

        self.assertEqual(kwargs, self._callback_kwargs)

    def test_call_calls_middleware(self):
        self._middleware_chain.call(
            None, None, None, None, None, self._callback)
        self.assertTrue(self._middleware.called)

    def test_call_calls_multiple_middleware(self):
        middleware_two = self.MockMiddleware()
        self._middleware_chain.append_middleware(middleware_two)

        self._middleware_chain.call(
            None, None, None, None, None, self._callback)
        self.assertTrue(self._middleware.called and middleware_two.called)

    def test_call_calls_multiple_middleware_with_extend(self):
        middleware_two = self.MockMiddleware()
        middleware_three = self.MockMiddleware()
        self._middleware_chain.extend([middleware_two, middleware_three])

        self._middleware_chain.call(
            None, None, None, None, None, self._callback)
        self.assertTrue(
            self._middleware.called and middleware_two.called and middleware_three.called)

    def test_call_calls_middleware_with_upstream_result(self):
        expected_result = self.MockData()
        self._middleware_chain.call(
            expected_result, None, None, None, None, self._callback)
        self.assertEqual(
            expected_result, self._middleware.upstream_result_callback)

    def test_call_calls_middleware_with_filler_builder(self):
        expected_result = self.MockData()
        self._middleware_chain.call(
            None, expected_result, None, None, None, self._callback)
        self.assertEqual(expected_result, self._middleware.filler_builder)

    def test_call_calls_middleware_with_filler_kwargs(self):
        expected_result = self.MockData()
        self._middleware_chain.call(
            None, None, expected_result, None, None, self._callback)
        self.assertEqual(expected_result, self._middleware.filler_kwargs)

    def test_chain_returns_chain(self):
        expected_result = [self._middleware]
        self.assertEqual(expected_result, self._middleware_chain.chain())

    def test_chain_returns_chain_multiple_items(self):
        middleware_two = self.MockMiddleware()
        self._middleware_chain.append_middleware(middleware_two)
        expected_result = [self._middleware, middleware_two]
        self.assertEqual(expected_result, self._middleware_chain.chain())

    def test_add_concatenates_middleware(self):
        middleware_chain_two = MiddlewareChain()
        middleware_two = self.MockMiddleware()
        middleware_chain_two.append_middleware(middleware_two)

        expected_result = [self._middleware, middleware_two]
        result = self._middleware_chain + middleware_chain_two
        self.assertEqual(expected_result, result.chain())

    def test_add_is_non_destructive(self):
        expected_result = [self._middleware]
        self._middleware_chain + self._middleware_chain
        self.assertEqual(expected_result, self._middleware_chain.chain())

    def test_add_concatenates_middleware_with_list(self):
        middleware_two = self.MockMiddleware()

        expected_result = [self._middleware, middleware_two]
        result = self._middleware_chain + [middleware_two]
        self.assertEqual(expected_result, result.chain())

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
