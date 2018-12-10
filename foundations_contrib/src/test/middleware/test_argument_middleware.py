"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations_contrib.middleware.argument_middleware import ArgumentMiddleware
from test.shared_examples.test_middleware_callback import TestMiddlewareCallback


class TestArgumentMiddleware(unittest.TestCase, TestMiddlewareCallback):

    def setUp(self):
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

        self._called_callback = False
        self._callback_args = None
        self._callback_result = None
        self._callback_kwargs = None

    def test_resolves_arguments(self):
        from foundations_internal.argument import Argument

        argument = Argument.generate_from(5, 'hello')
        middleware = self._make_middleware()
        middleware.call(None, None, {}, (argument,), {}, self._callback)
        self.assertEqual(self._callback_args, (5,))

    def test_resolves_arguments_multiple_arguments(self):
        from foundations_internal.argument import Argument

        argument = Argument.generate_from(7, 'hello')
        argument_two = Argument.generate_from(5, 'world')
        middleware = self._make_middleware()
        middleware.call(None, None, {}, (argument,
                                         argument_two), {}, self._callback)
        self.assertEqual(self._callback_args, (7, 5))

    def test_resolves_dynamic_arguments(self):
        from foundations_internal.argument import Argument
        from foundations.hyperparameter import Hyperparameter

        argument = Argument.generate_from(Hyperparameter('hello'), 'world')
        middleware = self._make_middleware()
        middleware.call(None, None, {'hello': 137},
                        (argument,), {}, self._callback)
        self.assertEqual(self._callback_args, (137,))

    def _function(self):
        pass

    def _callback(self, args, kwargs):
        from uuid import uuid4

        self._called_callback = True
        self._callback_args = self._resolve_args(args)
        self._callback_kwargs = kwargs

        if not hasattr(self, '_callback_result'):
            self._callback_result = uuid4()
        return self._callback_result

    def _make_middleware(self):
        return ArgumentMiddleware(self._pipeline_context, self._stage_config, self._stage_context, self._stage)

    def _resolve_args(self, args):
        new_args = (argument.value() for argument in args)
        return tuple(new_args)
