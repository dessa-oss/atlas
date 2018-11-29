"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.dynamic_parameter import DynamicParameter
from foundations.middleware.basic_stage_middleware import BasicStageMiddleware


class TestDynamicParameter(unittest.TestCase):

    def test_compute_value_returns_input(self):
        from foundations.hyperparameter import Hyperparameter

        hyper_parameter = Hyperparameter('hello')
        parameter = DynamicParameter(hyper_parameter)
        self.assertEqual(5, parameter.compute_value({'hello': 5}))

    def test_compute_value_returns_input_different_value(self):
        from foundations.hyperparameter import Hyperparameter

        hyper_parameter = Hyperparameter('hello')
        parameter = DynamicParameter(hyper_parameter)
        self.assertEqual(87, parameter.compute_value({'hello': 87}))

    def test_raises_value_error_on_missing_value(self):
        from foundations.hyperparameter import Hyperparameter

        hyper_parameter = Hyperparameter('hello')
        parameter = DynamicParameter(hyper_parameter)

        with self.assertRaises(ValueError) as context:
            parameter.compute_value({})

        self.assertIn(
            'No value provided for dynamic parameter `hello`', context.exception.args)

    def test_raises_value_error_on_missing_value_different_name(self):
        from foundations.hyperparameter import Hyperparameter

        hyper_parameter = Hyperparameter('why am I here')
        parameter = DynamicParameter(hyper_parameter)

        with self.assertRaises(ValueError) as context:
            parameter.compute_value({})

        self.assertIn(
            'No value provided for dynamic parameter `why am I here`', context.exception.args)

    def test_provenance(self):
        from foundations.hyperparameter import Hyperparameter

        hyper_parameter = Hyperparameter('why am I here')
        parameter = DynamicParameter(hyper_parameter)
        self.assertEqual(
            {'type': 'dynamic', 'name': 'why am I here'}, parameter.provenance())

    def test_provenance_different_value(self):
        from foundations.hyperparameter import Hyperparameter

        hyper_parameter = Hyperparameter('haro')
        parameter = DynamicParameter(hyper_parameter)
        self.assertEqual({'type': 'dynamic', 'name': 'haro'},
                         parameter.provenance())

    def test_value_hash(self):
        from foundations.hyperparameter import Hyperparameter

        hyper_parameter = Hyperparameter('hello')
        parameter = DynamicParameter(hyper_parameter)
        self.assertEqual('3e2e95f5ad970eadfa7e17eaf73da97024aa5359',
                         parameter.hash({'hello': 'potato'}))

    def test_value_hash_different_value(self):
        from foundations.hyperparameter import Hyperparameter

        hyper_parameter = Hyperparameter('goodbye')
        parameter = DynamicParameter(hyper_parameter)
        self.assertEqual('321e42b16eff1d6695a97ed82dc8b24f455db67d',
                         parameter.hash({'goodbye': 'mashed potato'}))

    def test_has_enable_caching_method(self):
        from foundations.hyperparameter import Hyperparameter

        hyper_parameter = Hyperparameter('goodbye')
        parameter = DynamicParameter(hyper_parameter)
        parameter.enable_caching()

    def test_str_returns_parameter_and_name(self):
        from foundations.hyperparameter import Hyperparameter

        hyper_parameter = Hyperparameter('goodbye')

        parameter = DynamicParameter(hyper_parameter)
        expected_string = 'parameter::goodbye'
        self.assertEqual(expected_string, str(parameter))

    def test_str_returns_parameter_and_name_different_name(self):
        from foundations.hyperparameter import Hyperparameter

        hyper_parameter = Hyperparameter('fire burns')

        parameter = DynamicParameter(hyper_parameter)
        expected_string = 'parameter::fire burns'
        self.assertEqual(expected_string, str(parameter))
