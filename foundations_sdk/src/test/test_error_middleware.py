"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.error_middleware import ErrorMiddleware
from foundations.stage_context import StageContext


class TestErrorMiddleware(unittest.TestCase):

    class MockStageContext(StageContext):

        def add_error_information(self, exception_info):
            self.exception_info = exception_info

    def setUp(self):
        self._stage_context = self.MockStageContext()

        self._called_callback = False
        self._callback_args = None
        self._callback_kwargs = None

    def test_calls_callback(self):
        middleware = self._make_middleware()
        middleware.call(None, None, None, (), {}, self._callback)
        self.assertTrue(self._called_callback)

    def test_calls_callback_with_args(self):
        middleware = self._make_middleware()
        middleware.call(None, None, None, ('hello', 'world'),
                        {}, self._callback)
        self.assertEqual(('hello', 'world'), self._callback_args)

    def test_calls_callback_with_different_args(self):
        middleware = self._make_middleware()
        middleware.call(None, None, None, ('goodbye'), {}, self._callback)
        self.assertEqual(('goodbye'), self._callback_args)

    def test_calls_callback_with_kwargs(self):
        middleware = self._make_middleware()
        middleware.call(None, None, None, (), {
                        'hello': 'world'}, self._callback)
        self.assertEqual({'hello': 'world'}, self._callback_kwargs)

    def test_calls_callback_with_different_kwargs(self):
        middleware = self._make_middleware()
        middleware.call(None, None, None, (), {
                        'basket': 'case'}, self._callback)
        self.assertEqual({'basket': 'case'}, self._callback_kwargs)

    def test_calls_callback_and_saves_error_information(self):
        middleware = self._make_middleware()
        try:
            middleware.call(None, None, None, (), {
                            'basket': 'case'}, self._error_callback)
        except:
            pass
        self.assertEqual(self._stage_context.exception_info[0], Exception)
        self.assertEqual(self._stage_context.exception_info[1].args, ('NOPE',))

        type_name = type(self._stage_context.exception_info[2]).__name__
        self.assertEqual('traceback', type_name)

    def _make_middleware(self):
        return ErrorMiddleware(self._stage_context)

    def _callback(self, args, kwargs):
        self._called_callback = True
        self._callback_args = args
        self._callback_kwargs = kwargs

    def _error_callback(self, args, kwargs):
        raise Exception('NOPE')
