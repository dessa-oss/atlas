"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.argument import Argument
from foundations.basic_stage_middleware import BasicStageMiddleware


class TestArgument(unittest.TestCase):

    class Parameter(object):

        def __init__(self, value, value_hash):
            self._value = value
            self._hash = value_hash
            self.computed_count = 0
            self.cache_enabled = False

        def compute_value(self, runtime_data):
            self.computed_count += 1
            return self._value * runtime_data

        def hash(self, runtime_data):
            return self._hash * runtime_data

        def enable_caching(self):
            self.cache_enabled = True

    def test_generate_argument_generates_constant(self):
        argument = Argument.generate_from(5, None)
        self.assertEqual(5, argument.value(None))

    def test_generate_argument_generates_constant_different_value(self):
        argument = Argument.generate_from(11, None)
        self.assertEqual(11, argument.value(None))

    def test_generate_argument_stores_name(self):
        argument = Argument.generate_from(5, 'hello')
        self.assertEqual('hello', argument.name())

    def test_generate_argument_stores_name_different_name(self):
        argument = Argument.generate_from(5, 'nope')
        self.assertEqual('nope', argument.name())

    def test_generate_argument_generates_dynamic_parameter(self):
        from foundations.hyperparameter import Hyperparameter

        argument = Argument.generate_from(Hyperparameter('hello'), None)
        self.assertEqual(5, argument.value({'hello': 5}))

    def test_generate_argument_generates_dynamic_parameter_without_name(self):
        from foundations.hyperparameter import Hyperparameter

        argument = Argument.generate_from(Hyperparameter(), 'hello')
        self.assertEqual(5, argument.value({'hello': 5}))

    def test_generate_argument_generates_dynamic_parameter_different_runtime_data(self):
        from foundations.hyperparameter import Hyperparameter

        argument = Argument.generate_from(Hyperparameter('hello'), None)
        self.assertEqual(15, argument.value({'hello': 15}))

    def test_generate_argument_generates_stage_parameter(self):
        def method():
            return 1233

        argument = Argument.generate_from(self._make_stage(method), None)
        self.assertEqual(1233, argument.value({}))

    def test_generate_argument_generates_stage_parameter_different_runtime_data(self):
        from foundations.hyperparameter import Hyperparameter

        argument = Argument.generate_from(Hyperparameter('hello'), None)
        self.assertEqual(15, argument.value({'hello': 15}))

    def test_stores_name(self):
        parameter = self.Parameter('hello', None)
        argument = Argument('world', parameter)
        self.assertEqual('world', argument.name())

    def test_stores_name_different_name(self):
        parameter = self.Parameter('potato', None)
        argument = Argument('spinach', parameter)
        self.assertEqual('spinach', argument.name())

    def test_uses_run_parameters(self):
        parameter = self.Parameter('hello', None)
        argument = Argument('world', parameter)
        self.assertEqual('hellohellohello', argument.value(3))

    def test_uses_run_parameters_different_value(self):
        parameter = self.Parameter('hello', None)
        argument = Argument('world', parameter)
        self.assertEqual('hellohello', argument.value(2))

    def test_returns_computed_value(self):
        parameter = self.Parameter('hello', None)
        argument = Argument('world', parameter)
        self.assertEqual('hello', argument.value(1))

    def test_returns_computed_value_different_value(self):
        parameter = self.Parameter('byebye', None)
        argument = Argument('world', parameter)
        self.assertEqual('byebye', argument.value(1))

    def _make_stage(self, function):
        from foundations.pipeline import Pipeline
        from foundations.pipeline_context import PipelineContext

        return Pipeline(PipelineContext()).stage(function)

    def test_forwards_hash(self):
        from foundations.argument import Argument

        parameter = self.Parameter(None, 'abcdef')
        argument = Argument('world', parameter)
        self.assertEqual('abcdef', argument.hash(1))

    def test_forwards_hash_different_hash(self):
        from foundations.argument import Argument

        parameter = self.Parameter(None, 'fedcba')
        argument = Argument('world', parameter)
        self.assertEqual('fedcba', argument.hash(1))

    def test_forwards_hash_different_runtime_data(self):
        from foundations.argument import Argument

        parameter = self.Parameter(None, 'fedcba')
        argument = Argument('world', parameter)
        self.assertEqual('fedcbafedcba', argument.hash(2))

    def test_forwards_enable_caching(self):
        from foundations.argument import Argument

        parameter = self.Parameter(None, 'abcdef')
        argument = Argument('world', parameter)
        argument.enable_caching()
        self.assertTrue(parameter.cache_enabled)

