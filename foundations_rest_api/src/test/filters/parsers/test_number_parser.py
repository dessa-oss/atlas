"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 12 2018
"""
import unittest
from foundations_rest_api.filters.parsers import NumberParser


class TestNumberParser(unittest.TestCase):

    def setUp(self):
        self._parser = NumberParser()

    def test_random_value(self):
        value = 'attack'
        self.assertRaises(ValueError, self._parser.parse, value)

    def test_good_string_value(self):
        value = '3.14'
        parsed_value = self._parser.parse(value)
        expected_result = 3.14
        self.assertEqual(expected_result, parsed_value)

    def test_good_float_value(self):
        value = 9.8
        parsed_value = self._parser.parse(value)
        expected_result = 9.8
        self.assertEqual(expected_result, parsed_value)

    def test_goog_int_value(self):
        value = 5
        parsed_value = self._parser.parse(value)
        expected_result = 5
        self.assertEqual(expected_result, parsed_value)

    def test_good_string_int_value(self):
        value = '10'
        parsed_value = self._parser.parse(value)
        expected_result = 10
        self.assertEqual(expected_result, parsed_value)

    def test_bad_none_value(self):
        value = None
        with self.assertRaises(ValueError) as cm:
            self._parser.parse(value)
        self.assertEqual(str(cm.exception), 'Not able to convert "None" to a number')

    def test_bad_null_good_value(self):
        value = 'null'
        self.assertRaises(ValueError, self._parser.parse, value)
