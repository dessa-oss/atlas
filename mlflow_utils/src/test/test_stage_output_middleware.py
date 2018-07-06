"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
import unittest
from vcat_mlflow.stage_output_middleware import StageOutputMiddleware


class TestStageOutputMiddleware(unittest.TestCase):
    def test_call_calls_callback(self):
        middleware = StageOutputMiddleware(
            None, None, self._make_context(), self._make_stage())
        middleware.call(None, None, None, [], {}, self._callback)
        self.assertEqual(True, self._callback_called())

    def test_call_returns_callback_result(self):
        middleware = StageOutputMiddleware(
            None, None, self._make_context(), self._make_stage())
        result = middleware.call(None, None, None, [], {}, self._callback)
        self.assertEqual(self._stage_result(), result)

    def test_call_creates_artifact_binary(self):
        from uuid import uuid4
        from test.helpers.mlflow_hacks import get_artifact_info
        from vcat.serializer import deserialize

        middleware = StageOutputMiddleware(
            None, None, self._make_context(True), self._make_stage())
        result = middleware.call(None, None, None, [], {}, self._callback)

        serialized_result_artifact, _ = get_artifact_info()
        result_artifact = deserialize(serialized_result_artifact)

        self.assertEqual(result, result_artifact)

    def _make_context(self, has_output=False):
        from vcat.stage_context import StageContext

        context = StageContext()
        context.has_stage_output = has_output

        return context

    def _make_stage(self):
        from vcat.stage import Stage
        from vcat.middleware_chain import MiddlewareChain
        from uuid import uuid4

        middleware = MiddlewareChain()
        return Stage(middleware, str(uuid4()), self._stage_function, self._stage_function)

    def _callback_called(self):
        return getattr(self, 'callback_called', None)

    def _callback(self, args, kwargs):
        from uuid import uuid4

        setattr(self, 'callback_called', True)

        stage_result = uuid4()
        setattr(self, 'stage_result', stage_result)
        return stage_result

    def _stage_result(self):
        return getattr(self, 'stage_result', None)

    def _stage_function(self):
        pass
