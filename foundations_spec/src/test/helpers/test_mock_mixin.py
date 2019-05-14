"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_spec.helpers.mock_mixin import MockMixin

class TestMockMixin(unittest.TestCase):

    def setUp(self):
        self._mixin = MockMixin()
        self._do_tear_down = True

    def tearDown(self):
        if self._do_tear_down:
            self._mixin._mock_tear_down()
    
    def test_patch_returns_mock(self):
        from mock import Mock

        mock = self._mixin.patch('os.environ')
        self.assertTrue(isinstance(mock, Mock))

    def test_patches_functionality_with_mock(self):
        import os

        mock = self._mixin.patch('os.environ')
        self.assertEqual(mock, os.environ)

    def test_patches_with_given_value(self):
        import os
        from mock import Mock

        my_specific_mock = Mock()
        mock = self._mixin.patch('os.environ', my_specific_mock)
        self.assertEqual(my_specific_mock, mock)

    def test_unpatches_when_teared_down(self):
        import os

        mock = self._mixin.patch('os.environ')
        self._mixin._mock_tear_down()

        self._do_tear_down = False
        self.assertNotEqual(mock, os.environ)

    def test_unpatches_when_teared_down_multiple_patches(self):
        import os
        import sys

        mock = self._mixin.patch('os.environ')
        mock_2 = self._mixin.patch('sys.modules')
        self._mixin._mock_tear_down()

        self._do_tear_down = False
        self.assertNotEqual(mock, os.environ)
        self.assertNotEqual(mock_2, sys.modules)

    def test_unpatches_when_teared_down_multiple_patches_on_same_object(self):
        import os

        original_environment = os.environ

        mock = self._mixin.patch('os.environ')
        mock_2 = self._mixin.patch('os.environ')
        self._mixin._mock_tear_down()

        self._do_tear_down = False
        self.assertEqual(original_environment, os.environ)