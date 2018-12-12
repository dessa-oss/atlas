"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 12 2018
"""
import unittest
from foundations_rest_api.filters.parsers import ElapsedTimeParser


class TestElapsedTimeParser(unittest.TestCase):

    def setUp(self):
        self._parser = ElapsedTimeParser()

    def test_random_value(self):
        value = 'attack'
        parsed_value = self._parser.parse(value)
        self.assertIsNone(parsed_value)

    def test_good_input_value(self):
        value = '2_11_30_40'
        parsed_value = self._parser.parse(value)
        expected_result = (2, 11, 30, 40)
        self.assertEqual(expected_result, parsed_value)

    def test_good_output_value(self):
        value = '4d20h10m15s'
        parsed_value = self._parser.parse(value)
        expected_result = (4, 20, 10, 15)
        self.assertEqual(expected_result, parsed_value)

    def test_bad_input_value(self):
        value = '2_11_30'
        parsed_value = self._parser.parse(value)
        self.assertIsNone(parsed_value)

    def test_bad_output_value(self):
        value = '4d10m15s'
        parsed_value = self._parser.parse(value)
        self.assertIsNone(parsed_value)

    def test_bad_input_value_imitating_good_value(self):
        value = '2_11_30.2_40'
        self.assertRaises(ValueError, self._parser.parse, value)
