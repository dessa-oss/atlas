"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations_internal.argument import Argument
from foundations_contrib.middleware.basic_stage_middleware import BasicStageMiddleware


class TestArgument(unittest.TestCase):

    class Parameter(object):

        def __init__(self, value, value_hash, provenance):
            self._value = value
            self._hash = value_hash
            self._provenance = provenance
            self.cache_enabled = False

        def compute_value(self, runtime_data):
            return self._value * runtime_data

        def hash(self, runtime_data):
            return self._hash * runtime_data

        def provenance(self):
            return self._provenance

        def enable_caching(self):
            self.cache_enabled = True

    def test_generate_argument_generates_constant(self):
        argument = Argument.generate_from(5, None)
        self.assertEqual(5, argument.value(None))

    def test_generate_argument_generates_constant_different_value(self):
        argument = Argument.generate_from(11, None)
        self.assertEqual(11, argument.value(None))

    def test_generate_argument_generates_list_of_stages(self):
        def method():
            return 1233

        argument = Argument.generate_from([self._make_stage(method)], None)
        self.assertEqual([1233], argument.value({}))

    def test_generate_argument_generates_list_of_parameters(self):
        def method():
            return 1233

        argument = Argument.generate_from([733, self._make_stage(method)], None)
        self.assertEqual([733, 1233], argument.value({}))

    def test_generate_argument_generates_dict_of_stages(self):
        def method():
            return 1233

        argument = Argument.generate_from({'hello': self._make_stage(method)}, None)
        self.assertEqual({'hello': 1233}, argument.value({}))

    def test_generate_argument_generates_dict_of_parameters(self):
        def method():
            return 1233

        argument = Argument.generate_from({'hello': 733, 'goodbye': self._make_stage(method)}, None)
        self.assertEqual({'hello': 733, 'goodbye': 1233}, argument.value({}))

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

        def method(hello):
            return hello

        hyper_parameter = Hyperparameter('hello')
        argument = Argument.generate_from(
            self._make_stage(method, hyper_parameter), None)

        self.assertEqual(77, argument.value({'hello': 77}))

    def test_generate_argument_returns_argument_when_argument_provided(self):
        argument = Argument.generate_from(42, None)
        argument2 = Argument.generate_from(argument, None)
        self.assertEqual(argument, argument2)

    def test_stores_name(self):
        parameter = self.Parameter('hello', None, None)
        argument = Argument('world', parameter)
        self.assertEqual('world', argument.name())

    def test_stores_name_different_name(self):
        parameter = self.Parameter('potato', None, None)
        argument = Argument('spinach', parameter)
        self.assertEqual('spinach', argument.name())

    def test_set_namestores_name(self):
        parameter = self.Parameter('hello', None, None)
        argument = Argument(None, parameter)
        argument.set_name('world')
        self.assertEqual('world', argument.name())

    def test_set_namestores_name_different_name(self):
        parameter = self.Parameter('potato', None, None)
        argument = Argument(None, parameter)
        argument.set_name('spinach')
        self.assertEqual('spinach', argument.name())

    def test_uses_run_parameters(self):
        parameter = self.Parameter('hello', None, None)
        argument = Argument('world', parameter)
        self.assertEqual('hellohellohello', argument.value(3))

    def test_uses_run_parameters_different_value(self):
        parameter = self.Parameter('hello', None, None)
        argument = Argument('world', parameter)
        self.assertEqual('hellohello', argument.value(2))

    def test_returns_computed_value(self):
        parameter = self.Parameter('hello', None, None)
        argument = Argument('world', parameter)
        self.assertEqual('hello', argument.value(1))

    def test_returns_computed_value_different_value(self):
        parameter = self.Parameter('byebye', None, None)
        argument = Argument('world', parameter)
        self.assertEqual('byebye', argument.value(1))

    def test_returns_provenance(self):
        parameter = self.Parameter(None, None, 'okaype')
        argument = Argument('world', parameter)
        self.assertEqual({'value': 'okaype', 'name': 'world'},
                         argument.provenance())

    def test_returns_provenance_different_value(self):
        parameter = self.Parameter(None, None, 'fet')
        argument = Argument('world', parameter)
        self.assertEqual({'value': 'fet', 'name': 'world'},
                         argument.provenance())

    def _make_stage(self, function, *args, **kwargs):
        from foundations_internal.pipeline import Pipeline
        from foundations_internal.pipeline_context import PipelineContext

        return Pipeline(PipelineContext()).stage(function, *args, **kwargs)

    def test_forwards_hash(self):
        from foundations_internal.argument import Argument

        parameter = self.Parameter(None, 'abcdef', None)
        argument = Argument('world', parameter)
        self.assertEqual('abcdef', argument.hash(1))

    def test_forwards_hash_different_hash(self):
        from foundations_internal.argument import Argument

        parameter = self.Parameter(None, 'fedcba', None)
        argument = Argument('world', parameter)
        self.assertEqual('fedcba', argument.hash(1))

    def test_forwards_hash_different_runtime_data(self):
        from foundations_internal.argument import Argument

        parameter = self.Parameter(None, 'fedcba', None)
        argument = Argument('world', parameter)
        self.assertEqual('fedcbafedcba', argument.hash(2))

    def test_forwards_enable_caching(self):
        parameter = self.Parameter(None, 'abcdef', None)
        argument = Argument('world', parameter)
        argument.enable_caching()
        self.assertTrue(parameter.cache_enabled)

    def test_forwards_string_representation(self):
        parameter = self.Parameter(None, 'abcdef', None)
        string_parameter = str(parameter)

        argument = Argument('world', parameter)
        self.assertEqual(string_parameter, str(argument))
