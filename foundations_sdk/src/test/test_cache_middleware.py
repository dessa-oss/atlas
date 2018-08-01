"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.cache_middleware import CacheMiddleware

from test.shared_examples.test_middleware_callback import TestMiddlewareCallback


class TestCacheMiddleware(unittest.TestCase, TestMiddlewareCallback):

    class MockCache(object):
        def __init__(self, cached_enabled, cache_name, uuid, args, kwargs, upstream_result_callback):
            self.cached_enabled = cached_enabled
            self._cache_name = cache_name
            self.uuid = uuid
            self.args = args
            self.kwargs = kwargs
            self.upstream_result_callback = upstream_result_callback

        def cache_name(self):
            return self._cache_name

        def fetch_cache(self):
            pass

        def fetch_cache_option(self):
            from foundations.nothing import Nothing
            return Nothing()

        def submit_cache(self, value):
            pass

    def setUp(self):
        from foundations.stage_config import StageConfig
        from foundations.stage_context import StageContext
        from foundations.stage import Stage

        from uuid import uuid4

        self._stage_config = StageConfig()
        self._stage_context = StageContext()
        self._uuid = str(uuid4())
        self._stage = Stage(None, self._uuid, self._function, self._function)

        self._cache = None
        self._called_callback = False
        self._callback_args = None
        self._callback_kwargs = None

    def test_creates_cache_with_configured_cache_name(self):
        from uuid import uuid4

        middleware = self._make_middleware()
        self._stage_config.enable_caching()

        self._stage_config.cache(uuid4())

        middleware.call(
            self._upstream_callback, None,
            {}, (), {}, self._callback
        )
        self.assertEqual(
            self._stage_config.cache_name(),
            self._cache.cache_name()
        )

    def test_creates_cache_with_cache_enabled(self):
        middleware = self._make_middleware()
        self._stage_config.enable_caching()

        middleware.call(
            self._upstream_callback, None,
            {}, (), {}, self._callback
        )
        self.assertTrue(self._cache.cached_enabled)

    def test_creates_cache_with_stage_uuid(self):
        middleware = self._make_middleware()
        self._stage_config.enable_caching()

        middleware.call(
            self._upstream_callback, None,
            {}, (), {}, self._callback
        )
        self.assertEqual(self._stage.uuid(), self._cache.uuid)

    def _upstream_callback(self):
        pass

    def _function(self):
        pass

    def _make_middleware(self):
        return CacheMiddleware(self._make_cache, self._stage_config, self._stage_context, self._stage)

    def _make_cache(self, cached_enabled, cache_name, uuid, args, kwargs, upstream_result_callback):
        self._cache = self.MockCache(
            cached_enabled, cache_name, uuid, args, kwargs, upstream_result_callback)
        return self._cache
