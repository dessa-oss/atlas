"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


import unittest

from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers import *

class TestLetMixin(unittest.TestCase):

    class SpecWithLet(Spec):
        @let
        def thing(self):
            return 'some stuff'
        @let
        def random_data(self):
            return self.faker.sha256()

    def setUp(self):
        self.SpecWithLet.setUpClass()
        self.spec_with_let = self.SpecWithLet()
        self.spec_with_let.setUp()

    def tearDown(self):
        self.spec_with_let.tearDown()
        self.SpecWithLet.tearDownClass()

    def test_has_value(self):
        self.assertEqual('some stuff', self.spec_with_let.thing)

    def test_does_not_have_value_when_not_accessed(self):
        self.assertNotIn('thing', self.spec_with_let.__dict__)

    def test_not_set_multiple_times(self):
        current_value = self.spec_with_let.random_data
        self.assertEqual(current_value, self.spec_with_let.random_data)