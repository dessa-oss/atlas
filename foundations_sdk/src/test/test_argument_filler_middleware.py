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

    class FillerBuilder(object):

        def __init__(self, fill_args, fill_kwargs, *args, **kwargs):
            self.fill_args = fill_args
            self.fill_kwargs = fill_kwargs
            self.args = args
            self.kwargs = kwargs

        def fill(self, **filler_kwargs):
            new_kwargs = {}
            new_kwargs.update(self.fill_kwargs)
            new_kwargs.update(self.kwargs)
            new_kwargs.update(filler_kwargs)

            return (self.fill_args + self.args, new_kwargs)

    def setUp(self):
        from foundations.stage import Stage

        from uuid import uuid4

        self._uuid = str(uuid4())
        self._stage = Stage(None, self._uuid, self._function, self._function)

        self._called_callback = False
        self._callback_args = None
        self._callback_kwargs = None

    def test_fills_args(self):
        middleware = self._make_middleware()
        args = ('hello',)
        kwargs = {}
        middleware.call(None, self._filler_builder(
            args, kwargs), {}, ('potato',), {}, self._callback)
        self.assertEqual(('hello', 'potato'), self._callback_args)

    def test_fills_args_different_value(self):
        middleware = self._make_middleware()
        args = ('goodbye', 'world')
        kwargs = {}
        middleware.call(None, self._filler_builder(
            args, kwargs), {}, ('driver',), {}, self._callback)
        self.assertEqual(('goodbye', 'world', 'driver'), self._callback_args)

    def test_fills_kwargs(self):
        middleware = self._make_middleware()
        args = ()
        kwargs = {'hello': 'world'}
        middleware.call(None, self._filler_builder(
            args, kwargs), {'too many': 'kwargs'}, (), {'goodbye': 'cruel world'}, self._callback)
        self.assertEqual({'hello': 'world', 'goodbye': 'cruel world', 'too many': 'kwargs'}, self._callback_kwargs)

    def test_fills_kwargs_different_value(self):
        middleware = self._make_middleware()
        args = ()
        kwargs = {'loss': 'very lost'}
        middleware.call(None, self._filler_builder(
            args, kwargs), {'so many': 'args'}, (), {'win': 'did not win'}, self._callback)
        self.assertEqual({'loss': 'very lost', 'win': 'did not win', 'so many': 'args'}, self._callback_kwargs)

    def _filler_builder(self, fill_args, fill_kwargs):
        def builder(*args, **kwargs):
            return self.FillerBuilder(fill_args, fill_kwargs, *args, **kwargs)
        return builder

    def _function(self):
        pass

    def _make_middleware(self):
        return ArgumentFillerMiddleware(self._stage)
