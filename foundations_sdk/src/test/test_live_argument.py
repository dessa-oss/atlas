"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.live_argument import LiveArgument
from foundations.middleware.basic_stage_middleware import BasicStageMiddleware


class TestLiveArgument(unittest.TestCase):

    class Parameter(object):

        def __init__(self, parameter_hash):
            self.computed_count = 0
            self._hash = parameter_hash

        def compute_value(self, runtime_data):
            self.computed_count += 1

        def hash(self, runtime_data):
            return self._hash

    def test_stores_name(self):
        from foundations.argument import Argument

        argument = Argument.generate_from('world', 'hello')
        live_argument = LiveArgument(argument, {})
        self.assertEqual('hello', live_argument.name())

    def test_stores_name_different_name(self):
        from foundations.argument import Argument

        argument = Argument.generate_from('haro', 'taro')
        live_argument = LiveArgument(argument, {})
        self.assertEqual('taro', live_argument.name())

    def test_value_returns_computed_value(self):
        from foundations.argument import Argument

        argument = Argument.generate_from('haro', 'taro')
        live_argument = LiveArgument(argument, {})
        self.assertEqual('haro', live_argument.value())

    def test_value_returns_computed_value_different_value(self):
        from foundations.argument import Argument

        argument = Argument.generate_from('mako', 'tomato')
        live_argument = LiveArgument(argument, {})
        self.assertEqual('mako', live_argument.value())

    def test_value_caches_value(self):
        from foundations.argument import Argument

        parameter = self.Parameter(None)
        argument = Argument('world', parameter)
        live_argument = LiveArgument(argument, {'mako': 'potato'})
        live_argument.value()
        live_argument.value()
        self.assertEqual(1, parameter.computed_count)

    def test_value_returns_computed_value_dynamic_value(self):
        from foundations.hyperparameter import Hyperparameter
        from foundations.argument import Argument

        argument = Argument.generate_from(Hyperparameter('mako'), 'tomato')
        live_argument = LiveArgument(argument, {'mako': 'potato'})
        self.assertEqual('potato', live_argument.value())

    def test_value_returns_computed_value_dynamic_value_different_value(self):
        from foundations.hyperparameter import Hyperparameter
        from foundations.argument import Argument

        argument = Argument.generate_from(Hyperparameter('mako'), 'tomato')
        live_argument = LiveArgument(argument, {'mako': 'mush'})
        self.assertEqual('mush', live_argument.value())

    def test_supports_non_arguments(self):
        argument = 137
        live_argument = LiveArgument(argument, {'mako': 'mush'})
        self.assertEqual(137, live_argument.value())

    def test_forwards_hash(self):
        from foundations.argument import Argument

        parameter = self.Parameter('abcdef')
        argument = Argument('world', parameter)
        live_argument = LiveArgument(argument, {})
        self.assertEqual('abcdef', live_argument.hash())

    def test_forwards_hash_different_runtime_data(self):
        from foundations.argument import Argument

        parameter = self.Parameter('abcdef')
        argument = Argument('world', parameter)
        live_argument = LiveArgument(argument, {})
        self.assertEqual('abcdef', live_argument.hash())

    def test_forwards_hash_dynamic_hash(self):
        from foundations.hyperparameter import Hyperparameter
        from foundations.argument import Argument

        argument = Argument.generate_from(Hyperparameter('mako'), 'tomato')
        live_argument = LiveArgument(argument, {'mako': 'mush'})
        self.assertEqual(
            '931a75bc4f56074653580a195ccb623a6e99a9eb', live_argument.hash())

    def test_forwards_hash_dynamic_hash_different_hash(self):
        from foundations.hyperparameter import Hyperparameter
        from foundations.argument import Argument

        argument = Argument.generate_from(Hyperparameter('mako'), 'tomato')
        live_argument = LiveArgument(argument, {'mako': 'mash potato'})
        self.assertEqual(
            '178fc9b765f0e81eae83af16b273edc5d078357c', live_argument.hash())
