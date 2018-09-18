"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_rest_api.models.property_model import PropertyModel


class TestPropertyModel(unittest.TestCase):

    class Mock(PropertyModel):
        my_property = PropertyModel.define_property()

    class MockTwo(PropertyModel):
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
        mock = self.MockTwo()
        mock.my_different_property = 14
        self.assertEqual(14, mock.my_different_property)
