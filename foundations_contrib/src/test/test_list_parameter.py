"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from mock import Mock

from foundations_contrib.list_parameter import ListParameter
from foundations_contrib.middleware.basic_stage_middleware import BasicStageMiddleware


class TestListParameter(unittest.TestCase):

    def test_stores_value(self):
        parameter = ListParameter([self._make_parameter('world')])
        self.assertEqual(['world'], parameter.compute_value(None))

    def test_stores_value_different_value(self):
        parameter = ListParameter([self._make_parameter('potato')])
        self.assertEqual(['potato'], parameter.compute_value(None))

    def test_stores_value_multiple_values(self):
        parameter = ListParameter([self._make_parameter('potato'), self._make_parameter('tomato')])
        self.assertEqual(['potato', 'tomato'], parameter.compute_value(None))

    def test_provenance(self):
        parameter = ListParameter([self._make_parameter('world')])
        self.assertEqual({'parameters': [{'type': 'constant', 'value': 'world'}], 'type': 'list'},
                         parameter.provenance())

    def test_provenance_different_value(self):
        parameter = ListParameter([self._make_parameter('potato')])
        self.assertEqual(
            {'parameters': [{'type': 'constant', 'value': 'potato'}], 'type': 'list'}, parameter.provenance())

    def test_provenance_mutiple_values(self):
        parameter = ListParameter([self._make_parameter('potato'), self._make_parameter('tomato')])
        expeceted_parameters = [{'type': 'constant', 'value': 'potato'}, {'type': 'constant', 'value': 'tomato'}]
        self.assertEqual(
            {'parameters': expeceted_parameters, 'type': 'list'}, parameter.provenance())

    def test_value_hash(self):
        parameter = ListParameter([self._make_parameter('potato')])
        self.assertEqual(
            'c4dbf747c350e8c14b8b16826ec84b8bac5dcf6c', parameter.hash(None))

    def test_value_hash_different_value(self):
        parameter = ListParameter([self._make_parameter('mashed potato')])
        self.assertEqual(
            '72185826ad9e84048b24dcb34c57e1c8f4480598', parameter.hash(None))

    def test_value_hash_multiple_values(self):
        parameter = ListParameter([self._make_parameter('mashed potato'), self._make_parameter('squashed tomato')])
        self.assertEqual(
            'f4cc1a4f1965026d903c062c136f3e51f9799953', parameter.hash(None))

    def test_enable_caching_method_calls_parameter(self):
        child_parameter = Mock()
        parameter = ListParameter([child_parameter])
        parameter.enable_caching()
        child_parameter.enable_caching.assert_called_once()

    def test_enable_caching_method_calls_parameter_multiple_parameters(self):
        child_parameter = Mock()
        child_parameter_two = Mock()
        parameter = ListParameter([child_parameter, child_parameter_two])
        parameter.enable_caching()
        child_parameter.enable_caching.assert_called_once()
        child_parameter_two.enable_caching.assert_called_once()

    def test_str_returns_underlying_str(self):
        parameter = ListParameter([self._make_parameter('1')])
        self.assertEqual("['1']", str(parameter))

    def test_str_returns_underlying_str_different_value(self):
        parameter = ListParameter([self._make_parameter('hello world')])
        self.assertEqual("['hello world']", str(parameter))

    def test_str_returns_underlying_str_multiple_values(self):
        parameter = ListParameter([self._make_parameter('hello world'), self._make_parameter('goodbye potatoes')])
        self.assertEqual("['hello world', 'goodbye potatoes']", str(parameter))

    def _make_parameter(self, value):
        from foundations_contrib.constant_parameter import ConstantParameter
        return ConstantParameter(value)