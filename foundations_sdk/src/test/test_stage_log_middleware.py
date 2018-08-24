"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.stage_log_middleware import StageLogMiddleware

from test.shared_examples.test_middleware_callback import TestMiddlewareCallback


class TestStageLogMiddleware(unittest.TestCase, TestMiddlewareCallback):

    def setUp(self):
        from foundations.stage_context import StageContext

        self._stage_context = StageContext()

        self._called_callback = False
        self._callback_args = None
        self._callback_kwargs = None

    def test_stores_stage_log(self):
        middleware = self._make_middleware()
        middleware.call(None, None, None, (), {},
                        self._log_callback('hello', {'loss': 56.33}))
        self.assertEqual({'loss': 56.33}, self._parse_stage_log())

    def test_ignores_bad_stage_log(self):
        def _wide_tuple_callback(args, kwargs):
            return (1, 2, 3)

        middleware = self._make_middleware()
        result = middleware.call(None, None, None, (), {}, _wide_tuple_callback)
        self.assertEqual((1, 2, 3), result)

    def test_stores_stage_log_different_values(self):
        middleware = self._make_middleware()
        middleware.call(None, None, None, (), {},
                        self._log_callback('hello', {'gain': 36.33, 'rock_n_awk': 9001}))
        self.assertEqual({'gain': 36.33, 'rock_n_awk': 9001},
                         self._parse_stage_log())

    def test_stores_removes_log_from_result(self):
        middleware = self._make_middleware()
        result = middleware.call(None, None, None, (), {},
                                 self._log_callback('hello', {}))
        self.assertEqual('hello', result)

    def test_stores_removes_log_from_result_different_value(self):
        middleware = self._make_middleware()
        result = middleware.call(None, None, None, (), {},
                                 self._log_callback('guitars', {}))
        self.assertEqual('guitars', result)

    def _log_callback(self, result, log):
        def _callback(args, kwargs):
            return result, log
        return _callback

    def _make_middleware(self):
        return StageLogMiddleware(self._stage_context)

    def _parse_stage_log(self):
        result = {}
        for log_item in self._stage_context.stage_log:
            result[log_item['key']] = log_item['value']
        return result

