"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_spec.helpers.mock_mixin import MockMixin
from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers import let_now

class TestLetNowMixin(unittest.TestCase):

    class MockSpec(Spec):
        pass

    def setUp(self):
        from faker import Faker

        self.faker = Faker()
        self.spec = self.MockSpec()

    def tearDown(self):
        self.spec.tearDown()
        self.MockSpec.tearDownClass()

    def test_makes_attributes_accessible(self):
        value = self.faker.sentence()
        self.MockSpec.fake_attribute = let_now(lambda spec_self: value)
        
        self.MockSpec.setUpClass()
        self.spec.setUp()
        self.assertEqual(value, self.spec.__dict__['fake_attribute'])

    def test_makes_attributes_accessible_multiple_attributes(self):
        value = self.faker.sentence()
        self.MockSpec.fake_attribute = let_now(lambda spec_self: value)

        value_two = self.faker.sentence()
        self.MockSpec.fake_attribute_two = let_now(lambda spec_self: value_two)
        
        self.MockSpec.setUpClass()
        self.spec.setUp()
        self.assertEqual(value_two, self.spec.__dict__['fake_attribute_two'])