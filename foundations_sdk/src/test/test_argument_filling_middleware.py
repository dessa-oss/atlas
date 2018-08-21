"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.argument_filling_middleware import ArgumentFillingMiddleware
from foundations.argument import Argument
from test.shared_examples.test_middleware_callback import TestMiddlewareCallback


class TestArgumentFillingMiddleware(unittest.TestCase, TestMiddlewareCallback):

    class MockArgument(Argument):

        def __init__(self, name, value):
            self._name = name
            self._value = value

        def name(self):
            return self._name

        def value(self, runtime_data):
            return self._value

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
        self._callback_result = None
        self._callback_kwargs = None

    def test_resolves_arguments(self):
        from foundations.live_argument import LiveArgument

        argument = self.MockArgument(None, 5)
        argument = LiveArgument(argument, {})
        middleware = self._make_middleware()
        middleware.call(None, None, {}, (argument,), {}, self._callback)
        self.assertEqual(self._callback_args, (5,))

    def test_resolves_arguments_multiple_arguments(self):
        from foundations.live_argument import LiveArgument

        argument = self.MockArgument(None, 7)
        argument = LiveArgument(argument, {})
        argument_two = self.MockArgument(None, 5)
        argument_two = LiveArgument(argument_two, {})
        middleware = self._make_middleware()
        middleware.call(None, None, {}, (argument, argument_two), {}, self._callback)
        self.assertEqual(self._callback_args, (7, 5))

    def test_resolves_named_arguments(self):
        from foundations.live_argument import LiveArgument

        argument = self.MockArgument('hello', 5)
        argument = LiveArgument(argument, {})
        middleware = self._make_middleware()
        middleware.call(None, None, {}, (argument,), {}, self._callback)
        self.assertEqual(self._callback_kwargs, {'hello': 5})

    def test_resolves_named_arguments_different_value(self):
        from foundations.live_argument import LiveArgument

        argument = self.MockArgument('world', 878)
        argument = LiveArgument(argument, {})
        middleware = self._make_middleware()
        middleware.call(None, None, {}, (argument,), {}, self._callback)
        self.assertEqual(self._callback_kwargs, {'world': 878})

    def test_resolves_named_arguments_without_duplication(self):
        from foundations.live_argument import LiveArgument

        argument = self.MockArgument('hello', 5)
        argument = LiveArgument(argument, {})
        middleware = self._make_middleware()
        middleware.call(None, None, {}, (argument,), {}, self._callback)
        self.assertEqual(self._callback_args, ())

    def _function(self):
        pass

    def _make_middleware(self):
        return ArgumentFillingMiddleware(self._pipeline_context, self._stage_config, self._stage_context, self._stage)