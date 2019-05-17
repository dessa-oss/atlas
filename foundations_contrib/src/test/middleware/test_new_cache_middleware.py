"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_contrib.middleware.new_cache_middleware import NewCacheMiddleware

from test.shared_examples.test_middleware_callback import TestMiddlewareCallback


class TestNewCacheMiddleware(Spec, TestMiddlewareCallback):

    class MockStageCache(object):

        def __init__(self, pipeline_context, stage, stage_config, live_arguments):
            from foundations_contrib.nothing import Nothing

            self.pipeline_context = pipeline_context
            self.stage = stage
            self.stage_config = stage_config
            self.live_arguments = live_arguments
            self.value = None
            self.cached_value = Nothing()
            self.name_of_cache = None

        def cache_name(self):
            return self.name_of_cache

        def fetch_option(self):
            return self.cached_value

        def submit(self, value):
            self.value = value

    @set_up
    def set_up(self):
        from foundations_internal.pipeline_context import PipelineContext
        from foundations_internal.stage_config import StageConfig
        from foundations_internal.stage_context import StageContext
        from foundations_internal.stage import Stage

        from uuid import uuid4

        self._pipeline_context = PipelineContext()
        self._stage_config = StageConfig()
        self._stage_context = StageContext()
        self._uuid = str(uuid4())
        self._stage = Stage(None, self._uuid, self._function, self._function)

        self._stage_config.enable_caching()

        self._mock_stage_cache = None
        self._called_callback = False
        self._callback_args = None
        self._callback_kwargs = None

    def test_sets_up_stage_cache_with_pipeline_context(self):
        middleware = self._make_middleware()
        middleware.call(None, self.MockFiller, {}, (), {}, self._callback)
        self.assertEqual(self._pipeline_context,
                         self._mock_stage_cache.pipeline_context)

    def test_sets_up_stage_cache_with_stage(self):
        middleware = self._make_middleware()
        middleware.call(None, self.MockFiller, {}, (), {}, self._callback)
        self.assertEqual(self._stage, self._mock_stage_cache.stage)

    def test_sets_up_stage_cache_with_stage_config(self):
        middleware = self._make_middleware()
        middleware.call(None, self.MockFiller, {}, (), {}, self._callback)
        self.assertEqual(self._stage_config,
                         self._mock_stage_cache.stage_config)

    def test_sets_up_stage_cache_with_arguments(self):
        middleware = self._make_middleware()
        middleware.call(None, self.MockFiller, {},
                        ('hello',), {}, self._callback)
        self.assertEqual(('hello',), self._mock_stage_cache.live_arguments)

    def test_sets_up_stage_cache_with_arguments_multiple_arguments(self):
        middleware = self._make_middleware()
        middleware.call(None, self.MockFiller, {},
                        ('i', 'am', 'a', 'potato'), {}, self._callback)
        self.assertEqual(('i', 'am', 'a', 'potato'),
                         self._mock_stage_cache.live_arguments)

    def test_submits_cache(self):
        middleware = self._make_middleware()
        middleware.call(None, self.MockFiller, {}, (), {}, self._callback)
        self.assertEqual(self._callback_result, self._mock_stage_cache.value)

    def test_returns_cached_result(self):
        from foundations_contrib.something import Something

        cache = self._mock_stage_cache_method(
            self._pipeline_context, self._stage, self._stage_config, ())
        cache.cached_value = Something('some value')

        middleware = self._make_middleware()
        result = middleware.call(
            None, self.MockFiller, {}, (), {}, self._callback)
        self.assertEqual('some value', result)

    def test_does_not_use_cache_when_disabled(self):
        from foundations_contrib.something import Something

        self._stage_config.disable_caching()
        cache = self._mock_stage_cache_method(
            self._pipeline_context, self._stage, self._stage_config, ())
        cache.cached_value = Something('some value')

        middleware = self._make_middleware()
        result = middleware.call(
            None, self.MockFiller, {}, (), {}, self._callback)
        self.assertEqual(self._callback_result, result)

    def test_indicates_cache_used_when_present(self):
        from foundations_contrib.something import Something

        cache = self._mock_stage_cache_method(
            self._pipeline_context, self._stage, self._stage_config, ())
        cache.cached_value = Something('some value')

        middleware = self._make_middleware()
        middleware.call(None, self.MockFiller, {}, (), {}, self._callback)
        self.assertTrue(self._stage_context.used_cache)

    def test_does_not_indicate_cache_used_when_not_present(self):
        middleware = self._make_middleware()
        middleware.call(None, self.MockFiller, {}, (), {}, self._callback)
        self.assertFalse(self._stage_context.used_cache)

    def test_indicates_cache_name_when_present(self):
        from foundations_contrib.something import Something

        cache = self._mock_stage_cache_method(
            self._pipeline_context, self._stage, self._stage_config, ())
        cache.name_of_cache = 'some stuff'

        middleware = self._make_middleware()
        middleware.call(None, self.MockFiller, {}, (), {}, self._callback)

        self.assertEqual('some stuff', self._stage_context.cache_uuid)

    def test_indicates_cache_name_when_present_different_name(self):
        from foundations_contrib.something import Something

        cache = self._mock_stage_cache_method(
            self._pipeline_context, self._stage, self._stage_config, ())
        cache.name_of_cache = 'some different stuff'

        middleware = self._make_middleware()
        middleware.call(None, self.MockFiller, {}, (), {}, self._callback)

        self.assertEqual('some different stuff',
                         self._stage_context.cache_uuid)

    def test_does_not_indicate_cache_name_when_not_present(self):
        middleware = self._make_middleware()
        middleware.call(None, self.MockFiller, {}, (), {}, self._callback)
        self.assertEqual(None, self._stage_context.cache_uuid)

    def test_does_not_submit_cache_when_already_cached(self):
        from foundations_contrib.something import Something

        cache = self._mock_stage_cache_method(
            self._pipeline_context, self._stage, self._stage_config, ())
        cache.cached_value = Something('some value')

        middleware = self._make_middleware()
        middleware.call(None, self.MockFiller, {}, (), {}, self._callback)
        self.assertEqual(None, self._mock_stage_cache.value)

    def test_does_not_run_callback_when_already_cached(self):
        from foundations_contrib.something import Something

        cache = self._mock_stage_cache_method(
            self._pipeline_context, self._stage, self._stage_config, ())
        cache.cached_value = Something('some value')

        middleware = self._make_middleware()
        middleware.call(None, self.MockFiller, {}, (), {}, self._callback)
        self.assertFalse(self._called_callback)

    def _function(self):
        pass

    def _make_middleware(self):
        return NewCacheMiddleware(self._mock_stage_cache_method, self._pipeline_context, self._stage_config, self._stage_context, self._stage)

    def _mock_stage_cache_method(self, pipeline_context, stage, stage_config, live_arugments):
        if self._mock_stage_cache is None:
            self._mock_stage_cache = self.MockStageCache(
                pipeline_context, stage, stage_config, live_arugments)
        return self._mock_stage_cache
