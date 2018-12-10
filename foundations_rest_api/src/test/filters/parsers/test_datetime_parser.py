"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 12 2018
"""
import unittest
from datetime import datetime
from foundations_rest_api.filters.parsers import DateTimeParser


class TestDateTimeParser(unittest.TestCase):

    def setUp(self):
        self._parser = DateTimeParser()

    def test_random_value(self):
        value = 'attack'
        self.assertRaises(ValueError, self._parser.parse, value)

    def test_good_input_value(self):
        value = '12_06_2018_20_30'
        parsed_value = self._parser.parse(value)
        expected_result = datetime(2018, 12, 6, 20, 30)
        self.assertEqual(expected_result, parsed_value)

    def test_good_output_value_with_milliseconds(self):
        value = '2018-11-12T21:31:42.341025'
        parsed_value = self._parser.parse(value)
        expected_result = datetime(2018, 11, 12, 21, 31, 42, 341025)
        self.assertEqual(expected_result, parsed_value)

    def test_good_output_value_without_milliseconds(self):
        value = '2018-11-12T21:31:42'
        parsed_value = self._parser.parse(value)
        expected_result = datetime(2018, 11, 12, 21, 31, 42)
        self.assertEqual(expected_result, parsed_value)

    def test_bad_input_value(self):
        value = '2_11_30_40'
        self.assertRaises(ValueError, self._parser.parse, value)

    def test_bad_output_value(self):
        value = '2018-11-12T21:31'
        self.assertRaises(ValueError, self._parser.parse, value)

    def test_bad_input_value_imitating_good_value(self):
        value = '12_32_2018_20_30'
        self.assertRaises(ValueError, self._parser.parse, value)
