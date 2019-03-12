"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_spec.helpers.conditional_return import ConditionalReturn

class TestConditionalReturn(unittest.TestCase):

    def setUp(self):
        from faker import Faker
        
        self.faker = Faker()
        self.conditional_return = ConditionalReturn()

    def test_is_instance_of_mock(self):
        self.assertTrue(isinstance(self.conditional_return, Mock))
        
    def test_returns_value_when_no_params(self):
        mock = Mock()
        self.conditional_return.return_when(mock)
        self.assertEqual(mock, self.conditional_return())

    def test_fails_if_invalid_params_provided(self):
        fake_param = 'hello world'
        fake_param_2 = 5
        
        mock = Mock()
        self.conditional_return.return_when(mock, fake_param, fake_param_2)

        with self.assertRaises(AssertionError) as error_context:
            self.conditional_return()

        expected_message = """Mock called with unexpected arguments ((), {})
Supported arguments:
 (('hello world', 5), {})"""
        self.assertIn(expected_message, error_context.exception.args)

    def test_returns_value_if_params(self):
        fake_param = self.faker.sentence()
        fake_param_2 = self.faker.sentence() 
        
        mock = Mock()
        self.conditional_return.return_when(mock, fake_param, fake_param_2)
        self.assertEqual(mock, self.conditional_return(fake_param, fake_param_2))

    def test_mock_assertions_are_supported(self):
        mock = Mock()
        self.conditional_return.return_when(mock)
        self.conditional_return()
        self.conditional_return.assert_called()

    def test_mock_assertions_are_supported_with_params(self):
        fake_param = self.faker.sentence()

        mock = Mock()
        self.conditional_return.return_when(mock, fake_param)
        self.conditional_return(fake_param)
        self.conditional_return.assert_called_with(fake_param)

    def test_clear_params(self):
        fake_param = self.faker.sentence()
         
        mock = Mock()
        self.conditional_return.return_when(mock, fake_param)
        self.conditional_return.clear()

        with self.assertRaises(AssertionError):
            self.conditional_return(fake_param)
