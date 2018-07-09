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
        from test.helpers.mlflow_hacks import get_artifact_info
        from vcat.serializer import deserialize

        middleware = StageOutputMiddleware(
            None, None, self._make_context(True), self._make_stage())
        result = middleware.call(None, None, None, [], {}, self._callback)

        serialized_result_artifact, _ = get_artifact_info()
        result_artifact = deserialize(serialized_result_artifact)

        self.assertEqual(result, result_artifact)

    def test_call_uses_stage_name(self):
        from test.helpers.mlflow_hacks import get_artifact_info
        from pandas import read_csv

        middleware = StageOutputMiddleware(
            None, None, self._make_context(True), self._make_stage())
        middleware.call(None, None, None, [], {}, self._csv_callback)

        _, artifact_name = get_artifact_info()

        self.assertEqual('_stage_function', artifact_name)

    def test_call_uses_stage_name_different_name(self):
        from test.helpers.mlflow_hacks import get_artifact_info

        middleware = StageOutputMiddleware(
            None, None, self._make_context(True), self._make_stage(self._stage_function_two))
        middleware.call(None, None, None, [], {}, self._csv_callback)

        _, artifact_name = get_artifact_info()

        self.assertEqual('_stage_function_two', artifact_name)

    def test_call_creates_artifact_csv(self):
        from test.helpers.mlflow_hacks import get_artifact_info
        from pandas import read_csv

        middleware = StageOutputMiddleware(
            None, None, self._make_context(True), self._make_stage())
        result = middleware.call(None, None, None, [], {}, self._csv_callback)

        string_result_artifact, _ = get_artifact_info()
        io_result_artifact = self._make_string_io(string_result_artifact)
        result_artifact = read_csv(io_result_artifact)

        self.assertEqual(result[0].all(), result_artifact['0'].all())

    def _make_context(self, has_output=False):
        from vcat.stage_context import StageContext

        context = StageContext()
        context.has_stage_output = has_output

        return context

    def _make_stage(self, function=None):
        from vcat.stage import Stage
        from vcat.middleware_chain import MiddlewareChain
        from uuid import uuid4

        middleware = MiddlewareChain()

        if function is None:
            function = self._stage_function

        return Stage(middleware, str(uuid4()), self._stage_function, function)

    def _callback_called(self):
        return getattr(self, 'callback_called', None)

    def _callback(self, args, kwargs):
        from uuid import uuid4

        setattr(self, 'callback_called', True)

        stage_output = uuid4()
        setattr(self, 'stage_result', stage_output)
        return stage_output

    def _csv_callback(self, args, kwargs):
        from pandas import DataFrame
        from random import randint

        stage_output = DataFrame([[randint(1, 10)]])
        setattr(self, 'stage_result', stage_output)
        return stage_output
    
    def _stage_result(self):
        return getattr(self, 'stage_result', None)

    def _stage_function(self):
        pass

    def _stage_function_two(self):
        pass

    def _make_string_io(self, byte_string):
        import sys
        from vcat.utils import string_from_bytes

        if sys.version_info[0] < 3: 
            from StringIO import StringIO
        else:
            from io import StringIO

        return StringIO(string_from_bytes(byte_string))