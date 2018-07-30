"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.basic_stage_middleware import BasicStageMiddleware


class TestBasicStageMiddleware(unittest.TestCase):

    class MockStageMiddleware(BasicStageMiddleware):

        def pipeline_context(self):
            return self._pipeline_context

        def stage_config(self):
            return self._stage_config

        def stage_context(self):
            return self._stage_context

        def stage(self):
            return self._stage

        def uuid(self):
            return self._uuid()

        def name(self):
            return self._name()

    def setUp(self):
        from foundations.pipeline_context import PipelineContext
        from foundations.stage_config import StageConfig
        from foundations.stage_context import StageContext
        from foundations.stage import Stage

        from uuid import uuid4

        self._pipeline_context = PipelineContext()
        self._stage_config = StageConfig()
        self._stage_context = StageContext()
        self._uuid = str(uuid4())
        self._stage = Stage(None, self._uuid, self._function, self._function)

        self._called_callback = False
        self._callback_args = None
        self._callback_kwargs = None

    def test_stores_pipeline_context(self):
        middleware = self._make_middleware()
        self.assertEqual(self._pipeline_context, middleware.pipeline_context())

    def test_stores_stage_config(self):
        middleware = self._make_middleware()
        self.assertEqual(self._stage_config, middleware.stage_config())

    def test_stores_stage_context(self):
        middleware = self._make_middleware()
        self.assertEqual(self._stage_context, middleware.stage_context())

    def test_stores_stage(self):
        middleware = self._make_middleware()
        self.assertEqual(self._stage, middleware.stage())

    def test_uuid(self):
        middleware = self._make_middleware()
        self.assertEqual(self._uuid, middleware.uuid())

    def test_name(self):
        middleware = self._make_middleware()
        self.assertEqual('_function', middleware.name())

    def test_name_different_function(self):
        from foundations.stage import Stage

        self._stage = Stage(
            None, self._uuid, self._other_function, self._other_function)
        middleware = self._make_middleware()
        self.assertEqual('_other_function', middleware.name())

    def test_calls_callback(self):
        middleware = self._make_middleware()
        middleware.call(None, None, None, (), {}, self._callback)
        self.assertTrue(self._called_callback)

    def test_calls_callback_with_args(self):
        middleware = self._make_middleware()
        middleware.call(None, None, None, ('hello', 'world'), {}, self._callback)
        self.assertEqual(('hello', 'world'), self._callback_args)

    def test_calls_callback_with_different_args(self):
        middleware = self._make_middleware()
        middleware.call(None, None, None, ('goodbye'), {}, self._callback)
        self.assertEqual(('goodbye'), self._callback_args)

    def test_calls_callback_with_kwargs(self):
        middleware = self._make_middleware()
        middleware.call(None, None, None, (), {'hello': 'world'}, self._callback)
        self.assertEqual({'hello': 'world'}, self._callback_kwargs)

    def test_calls_callback_with_different_kwargs(self):
        middleware = self._make_middleware()
        middleware.call(None, None, None, (), {'basket': 'case'}, self._callback)
        self.assertEqual({'basket': 'case'}, self._callback_kwargs)

    def _make_middleware(self):
        return self.MockStageMiddleware(self._pipeline_context, self._stage_config, self._stage_context, self._stage)

    def _function(self):
        pass

    def _other_function(self):
        pass

    def _callback(self, args, kwargs):
        self._called_callback = True
        self._callback_args = args
        self._callback_kwargs = kwargs
