"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers import *

from mock import MagicMock

class TestSpec(unittest.TestCase):

    class MockSpec(Spec):
        pass

    def setUp(self):
        self.MockSpec.setUpClass()
        self.spec = self.MockSpec()

        self._skip_tear_down = False

    def tearDown(self):
        if not self._skip_tear_down:
            self.spec.tearDown()
            self.MockSpec.tearDownClass()
    
    def test_has_faker(self):
        import faker

        self.spec.setUp()
        self.assertIsInstance(self.spec.faker, faker.generator.Generator)

    def test_calls_set_up_methods(self):
        mock = MagicMock()
        
        self.MockSpec.set_up = set_up(lambda spec_self: mock())
        self.spec.setUp()
        mock.assert_called()

    def test_calls_set_up_methods_mutiple_methods(self):
        mock = MagicMock()
        mock2 = MagicMock()
        
        self.MockSpec.set_up = set_up(lambda spec_self: mock())
        self.MockSpec.set_up_2 = set_up(lambda spec_self: mock2())
        self.spec.setUp()
        mock2.assert_called()

    def test_calls_tear_down_methods(self):
        mock = MagicMock()
        
        self.MockSpec.tear_down = tear_down(lambda spec_self: mock())
        self.spec.tearDown()
        mock.assert_called()

    def test_calls_tear_down_methods_mutiple_methods(self):
        mock = MagicMock()
        mock2 = MagicMock()
        
        self.MockSpec.tear_down = tear_down(lambda spec_self: mock())
        self.MockSpec.tear_down_2 = tear_down(lambda spec_self: mock2())
        self.spec.tearDown()
        mock2.assert_called()

    def test_calls_set_up_class_methods(self):
        mock = MagicMock()
        
        self.MockSpec.set_up_class = set_up_class(lambda spec_self: mock())
        self.spec.setUpClass()
        mock.assert_called()

    def test_calls_set_up_methods_mutiple_methods(self):
        mock = MagicMock()
        mock2 = MagicMock()
        
        self.MockSpec.set_up_class = set_up_class(lambda spec_self: mock())
        self.MockSpec.set_up_class_2 = set_up_class(lambda spec_self: mock2())
        self.spec.setUpClass()
        mock2.assert_called()
    
    def test_calls_tear_down_class_methods(self):
        self._skip_tear_down = True

        mock = MagicMock()
        
        self.MockSpec.tear_down_class = tear_down_class(lambda spec_self: mock())
        self.spec.tearDownClass()
        mock.assert_called()

    def test_calls_tear_down_class_methods_mutiple_methods(self):
        self._skip_tear_down = True

        mock = MagicMock()
        mock2 = MagicMock()
        
        self.MockSpec.tear_down_class = tear_down_class(lambda spec_self: mock())
        self.MockSpec.tear_down_class_2 = tear_down_class(lambda spec_self: mock2())
        self.spec.tearDownClass()
        mock2.assert_called()