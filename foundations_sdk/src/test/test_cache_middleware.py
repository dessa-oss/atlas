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

        self._called_callback = False
        self._callback_args = None
        self._callback_kwargs = None

    def _function(self):
        pass

    def _make_middleware(self):
        return CacheMiddleware(self.MockCache, self._stage_config, self._stage_context, self._stage)
