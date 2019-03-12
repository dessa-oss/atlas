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

    class SpecWithLetTwo(Spec):
        @let
        def thing(self):
            return 'some stuff'

    class SpecWithLetThree(Spec):
        @let
        def thing(self):
            return 'some stuff'

    class SpecWithLetFour(Spec):
        @let
        def thing2(self):
            return 'some other stuff'

    class SpecWithInheritedLet(SpecWithLetTwo):
        pass

    class SpecWithMultiInheritedLet(SpecWithLetThree, SpecWithLetFour):
        pass

    def setUp(self):
        self.SpecWithLet.setUpClass()
        self.spec_with_let = self.SpecWithLet()
        self.spec_with_let.setUp()

        self.SpecWithInheritedLet.setUpClass()
        self.spec_with_inherited_let = self.SpecWithInheritedLet()
        self.spec_with_inherited_let.setUp()

        self.SpecWithMultiInheritedLet.setUpClass()
        self.spec_with_multi_inherited_let = self.SpecWithMultiInheritedLet()
        self.spec_with_multi_inherited_let.setUp()

    def tearDown(self):
        self.spec_with_let.tearDown()
        self.SpecWithLet.setUpClass()

        self.spec_with_inherited_let.tearDown()
        self.SpecWithInheritedLet.setUpClass()

        self.spec_with_multi_inherited_let.tearDown()
        self.SpecWithMultiInheritedLet.tearDownClass()

    def test_has_value(self):
        self.assertEqual('some stuff', self.spec_with_let.thing)

    def test_does_not_have_value_when_not_accessed(self):
        self.assertNotIn('thing', self.spec_with_let.__dict__)

    def test_not_set_multiple_times(self):
        current_value = self.spec_with_let.random_data
        self.assertEqual(current_value, self.spec_with_let.random_data)

    def test_supports_inheritence(self):
        self.assertEqual('some stuff', self.spec_with_inherited_let.thing)

    def test_supports_multiple_inheritence(self):
        self.assertEqual('some stuff', self.spec_with_multi_inherited_let.thing)
        self.assertEqual('some other stuff', self.spec_with_multi_inherited_let.thing2)
        