"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_contrib.models.property_model import PropertyModel


class TestPropertyModel(unittest.TestCase):

    class Mock(PropertyModel):
        my_property = PropertyModel.define_property()
        my_other_property = PropertyModel.define_property()

    class MockTwo(PropertyModel):
        my_different_property = PropertyModel.define_property()

    class MockThree(PropertyModel):
        my_different_property = PropertyModel.define_property()

    def test_defines_property(self):
        mock = self.Mock()
        mock.my_property = 5
        self.assertEqual(5, mock.my_property)

    def test_defines_property_different_value(self):
        mock = self.Mock()
        mock.my_property = 14
        self.assertEqual(14, mock.my_property)

    def test_defines_property_different_property(self):
        mock = self.Mock()
        mock.my_other_property = 14
        self.assertEqual(14, mock.my_other_property)

    def test_defines_property_different_property_no_conflict(self):
        mock = self.Mock()
        mock.my_property = 23
        mock.my_other_property = 14
        self.assertEqual(23, mock.my_property)

    def test_defines_property_different_class(self):
        mock = self.MockTwo()
        mock.my_different_property = 14
        self.assertEqual(14, mock.my_different_property)

    def test_equality_equals(self):
        mock = self.MockTwo(my_different_property=5)
        mock2 = self.MockTwo(my_different_property=5)
        self.assertEqual(mock, mock2)

    def test_equality_not_equal(self):
        mock = self.MockTwo(my_different_property=5)
        mock2 = self.MockTwo(my_different_property=7)
        self.assertNotEqual(mock, mock2)

    def test_equality_not_same_type(self):
        mock = self.MockTwo(my_different_property=5)
        mock2 = self.MockThree(my_different_property=5)
        self.assertNotEqual(mock, mock2)

    def test_inequality_equals(self):
        mock = self.MockTwo(my_different_property=5)
        mock2 = self.MockTwo(my_different_property=5)
        self.assertFalse(mock.__ne__(mock2))

    def test_inequality_not_equal(self):
        mock = self.MockTwo(my_different_property=5)
        mock2 = self.MockTwo(my_different_property=7)
        self.assertTrue(mock.__ne__(mock2))

    def test_inequality_not_same_type(self):
        mock = self.MockTwo(my_different_property=5)
        mock2 = self.MockThree(my_different_property=5)
        self.assertTrue(mock.__ne__(mock2))

    def test_attributes(self):
        mock = self.MockTwo(my_different_property=5)
        self.assertEqual({'my_different_property': 5}, mock.attributes)

    def test_attributes_different_class(self):
        mock = self.Mock(my_property=23, my_other_property=233)
        self.assertEqual({'my_property': 23, 'my_other_property': 233}, mock.attributes)

    def test_raises_error_on_invalid_property(self):
        with self.assertRaises(ValueError) as context:
            mock = self.Mock(bad_property=23)
        self.assertTrue('Invalid property `bad_property` given' in context.exception.args)

    def test_raises_error_on_invalid_property_different_property(self):
        with self.assertRaises(ValueError) as context:
            mock = self.Mock(bad_property_again=2323232323)
        self.assertTrue('Invalid property `bad_property_again` given' in context.exception.args)
