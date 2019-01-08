"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 12 2018
"""
import unittest
from foundations_rest_api.filters.parsers import StatusParser


class TestStatusParser(unittest.TestCase):

    def setUp(self):
        self._parser = StatusParser()

    def test_random_value(self):
        value = 'attack'
        parsed_value = self._parser.parse(value)
        self.assertIsNone(parsed_value)

    def test_randomcase_queued(self):
        value = 'qUEuEd'
        parsed_value = self._parser.parse(value)
        expected_result = 'QUEUED'
        self.assertEqual(expected_result, parsed_value)

    def test_randomcase_running(self):
        value = 'RUnNIng'
        parsed_value = self._parser.parse(value)
        expected_result = 'RUNNING'
        self.assertEqual(expected_result, parsed_value)

    def test_randomcase_completed(self):
        value = 'cOMPleTEd'
        parsed_value = self._parser.parse(value)
        expected_result = 'COMPLETED'
        self.assertEqual(expected_result, parsed_value)

    def test_randomcase_failed(self):
        value = 'faiLED'
        parsed_value = self._parser.parse(value)
        expected_result = 'FAILED'
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
