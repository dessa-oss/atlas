"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations_contrib.middleware.stage_output_middleware import StageOutputMiddleware

from test.shared_examples.test_middleware_callback import TestMiddlewareCallback


class TestStageOutputMiddleware(unittest.TestCase, TestMiddlewareCallback):

    def setUp(self):
        from foundations_internal.stage_config import StageConfig
        from foundations_internal.stage_context import StageContext

        self._stage_config = StageConfig()
        self._stage_context = StageContext()

        self._called_callback = False
        self._callback_args = None
        self._callback_kwargs = None

    def test_stores_stage_output(self):
        self._stage_config.persist()

        middleware = self._make_middleware()
        middleware.call(None, None, None, (), {}, self._callback)
        self.assertEqual(self._callback_result,
                         self._stage_context.stage_output)

    def test_does_not_store_stage_output_if_not_persisted(self):
        middleware = self._make_middleware()
        middleware.call(None, None, None, (), {}, self._callback)
        self.assertEqual(None, self._stage_context.stage_output)

    def _make_middleware(self):
        return StageOutputMiddleware(self._stage_config, self._stage_context)
