"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from vcat_ui.stage_log_middleware import StageLogMiddleware


class TestStageLogMiddleware(unittest.TestCase):

    def test_call_calls_callback(self):
        middleware = StageLogMiddleware(
            None, None, self._make_context(), self._make_stage())
        middleware.call(None, None, None, [], {}, self._callback)
        self.assertEqual(True, self._callback_called())

    def test_call_returns_callback_result(self):
        middleware = StageLogMiddleware(
            None, None, self._make_context(), self._make_stage())
        result = middleware.call(None, None, None, [], {}, self._callback)
        self.assertEqual(self._stage_result(), result)

    def test_call_creates_metric(self):
        from test.helpers import mlflow_hacks
        from test.helpers.mlflow_hacks import get_metric_info

        mlflow_hacks.reset()

        stage_output = {'score': 0.95}
        middleware = StageLogMiddleware(
            None, None, self._make_context(True), self._make_stage())
        middleware.call(None, None, None, [],
                                 {}, self._make_callback(stage_output))

        result_metric = get_metric_info('_stage_function.score')

        self.assertEqual(0.95, result_metric)

    def test_call_creates_metric_different_stage_name(self):
        from test.helpers import mlflow_hacks
        from test.helpers.mlflow_hacks import get_metric_info

        mlflow_hacks.reset()

        stage_output = {'score': 0.95}
        middleware = StageLogMiddleware(
            None, None, self._make_context(True), self._make_stage(self._other_stage_function))
        middleware.call(None, None, None, [],
                                 {}, self._make_callback(stage_output))

        result_metric = get_metric_info('_other_stage_function.score')

        self.assertEqual(0.95, result_metric)

    def test_call_creates_multiple_metrics(self):
        from test.helpers import mlflow_hacks
        from test.helpers.mlflow_hacks import get_metric_info

        mlflow_hacks.reset()

        stage_output = {'score': 0.35, 'loss': 9.44}
        middleware = StageLogMiddleware(
            None, None, self._make_context(True), self._make_stage())
        middleware.call(None, None, None, [],
                                 {}, self._make_callback(stage_output))

        result_metric = get_metric_info('_stage_function.score')
        self.assertEqual(0.35, result_metric)

        result_metric = get_metric_info('_stage_function.loss')
        self.assertEqual(9.44, result_metric)

    def _make_stage(self, function=None):
        from vcat.stage import Stage
        from vcat.middleware_chain import MiddlewareChain
        from uuid import uuid4

        middleware = MiddlewareChain()

        if function is None:
            function = self._stage_function

        return Stage(middleware, str(uuid4()), self._stage_function, function)

    def _stage_result(self):
        return getattr(self, 'stage_result', None)

    def _stage_function(self):
        pass

    def _other_stage_function(self):
        pass

    def _callback_called(self):
        return getattr(self, 'callback_called', None)

    def _make_context(self, has_output=False):
        from vcat.stage_context import StageContext

        context = StageContext()
        context.has_stage_output = has_output

        return context

    def _callback(self, args, kwargs):
        from uuid import uuid4

        setattr(self, 'callback_called', True)

        stage_output = uuid4()
        setattr(self, 'stage_result', stage_output)
        return stage_output

    def _make_callback(self, output):
        def callback(args, kwargs):
            return self._callback(args, kwargs), output

        return callback
