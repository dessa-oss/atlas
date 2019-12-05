"""
 (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from mock import Mock
from foundations_spec.helpers.partial_callable_mock import PartialCallableMock


class TestPartialCallableMock(unittest.TestCase):

    def setUp(self):
        from faker import Faker

        self.faker = Faker()
        self.mock = PartialCallableMock()

    def test_is_mock(self):
        self.assertIsInstance(self.mock, Mock)

    def test_raises_exception_if_called_with_incorrect_params(self):
        param = self.faker.sentence()
        self.mock()

        with self.assertRaises(AssertionError) as error_context:
            self.mock.assert_called_with_partial(param)

        expected_message = "Expected call: mock('{}')\nActual call: mock()".format(param)
        self.assertIn(expected_message, error_context.exception.args)

    def test_raises_exception_if_called_with_incorrect_keywords_args(self):
        param = self.faker.sentence()
        self.mock()

        with self.assertRaises(AssertionError) as error_context:
            self.mock.assert_called_with_partial(hello=param)

        expected_message = "Expected call: mock(hello='{}')\nActual call: mock()".format(param)
        self.assertIn(expected_message, error_context.exception.args)

    def test_raises_exception_if_called_with_partial_out_of_order(self):
        param = self.faker.sentence()
        param_2 = self.faker.sentence()
        self.mock(param_2, param)

        with self.assertRaises(AssertionError) as error_context:
            self.mock.assert_called_with_partial(param, param_2)

        expected_message = "Expected call: mock('{}', '{}')\nActual call: mock('{}', '{}')".format(
            param, 
            param_2, 
            param_2, 
            param
        )
        self.assertIn(expected_message, error_context.exception.args)

    def test_raises_exception_if_not_called(self):
        param = self.faker.sentence()

        with self.assertRaises(AssertionError) as error_context:
            self.mock.assert_called_with_partial(param)

        expected_message = "Expected call: mock('{}')\nNot called".format(param)
        self.assertIn(expected_message, error_context.exception.args)

    def test_does_not_raise_when_called_properly(self):
        param = self.faker.sentence()
        self.mock(param)
        self.mock.assert_called_with_partial(param)

    def test_does_not_raise_when_called_partially(self):
        param = self.faker.sentence()
        param_2 = self.faker.sentence()

        self.mock(param, param_2)
        self.mock.assert_called_with_partial(param)
