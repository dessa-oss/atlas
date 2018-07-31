"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.argument_filler_middleware import ArgumentFillerMiddleware

from test.shared_examples.test_middleware_callback import TestMiddlewareCallback


class TestArgumentFillerMiddleware(unittest.TestCase, TestMiddlewareCallback):

    def setUp(self):
        from foundations.stage import Stage

        from uuid import uuid4

        self._uuid = str(uuid4())
        self._stage = Stage(None, self._uuid, self._function, self._function)

        self._called_callback = False
        self._callback_args = None
        self._callback_kwargs = None

    def _function(self):
        pass

    def _make_middleware(self):
        return ArgumentFillerMiddleware(self._stage)
