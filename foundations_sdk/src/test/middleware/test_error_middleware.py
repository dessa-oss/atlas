"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.middleware.error_middleware import ErrorMiddleware
from foundations.stage_context import StageContext

from test.shared_examples.test_middleware_callback import TestMiddlewareCallback


class TestErrorMiddleware(unittest.TestCase, TestMiddlewareCallback):

    class MockStageContext(StageContext):

        def add_error_information(self, exception_info):
            self.exception_info = exception_info

    def setUp(self):
        self._stage_context = self.MockStageContext()

        self._called_callback = False
        self._callback_args = None
        self._callback_kwargs = None

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

    def _error_callback(self, args, kwargs):
        raise Exception('NOPE')
