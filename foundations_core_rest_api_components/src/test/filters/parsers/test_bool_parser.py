"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 12 2018
"""
import unittest
from foundations_core_rest_api_components.filters.parsers import BoolParser


class TestBoolParser(unittest.TestCase):

    def setUp(self):
        self._parser = BoolParser()

    def test_random_value(self):
        value = 'attack'
        parsed_value = self._parser.parse(value)
        self.assertIsNone(parsed_value)

    def test_good_string_lowercase_true(self):
        value = 'true'
        parsed_value = self._parser.parse(value)
        expected_result = True
        self.assertEqual(expected_result, parsed_value)

    def test_good_string_uppercase_true(self):
        value = 'TRUE'
        parsed_value = self._parser.parse(value)
        expected_result = True
        self.assertEqual(expected_result, parsed_value)

    def test_good_string_randomcase_true(self):
        value = 'tRuE'
        parsed_value = self._parser.parse(value)
        expected_result = True
        self.assertEqual(expected_result, parsed_value)

    def test_good_bool_true(self):
        value = True
        parsed_value = self._parser.parse(value)
        expected_result = True
        self.assertEqual(expected_result, parsed_value)

    def test_good_string_lowercase_false(self):
        value = 'false'
        parsed_value = self._parser.parse(value)
        expected_result = False
        self.assertEqual(expected_result, parsed_value)

    def test_good_string_uppercase_false(self):
        value = 'FALSE'
        parsed_value = self._parser.parse(value)
        expected_result = False
        self.assertEqual(expected_result, parsed_value)

    def test_good_string_randomcase_false(self):
        value = 'fALsE'
        parsed_value = self._parser.parse(value)
        expected_result = False
        self.assertEqual(expected_result, parsed_value)

    def test_good_bool_false(self):
        value = False
        parsed_value = self._parser.parse(value)
        expected_result = False
        self.assertEqual(expected_result, parsed_value)

    def test_bad_none_value(self):
        value = None
        parsed_value = self._parser.parse(value)
        self.assertIsNone(parsed_value)

    def test_bad_null_value(self):
        value = 'null'
        parsed_value = self._parser.parse(value)
        self.assertIsNone(parsed_value)

    def test_bad_float_value(self):
        value = 3.14
        parsed_value = self._parser.parse(value)
        self.assertIsNone(parsed_value)

    def test_bad_int_value(self):
        value = 5
        parsed_value = self._parser.parse(value)
        self.assertIsNone(parsed_value)

    def test_bad_one_value(self):
        value = 1
        parsed_value = self._parser.parse(value)
        self.assertIsNone(parsed_value)

    def test_bad_zero_value(self):
        value = 0
        parsed_value = self._parser.parse(value)
        self.assertIsNone(parsed_value)
