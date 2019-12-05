"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


import unittest

from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers import *

class TestLetMixinInheritence(unittest.TestCase):

    class SpecWithLet(object):
        @let
        def thing(self):
            return 'some stuff'

    class SpecWithLetTwo(object):
        @let
        def thing2(self):
            return 'some other stuff'

    class SpecWithMultiInheritedLet(Spec, SpecWithLet, SpecWithLetTwo):
        pass

    def setUp(self):
        self.SpecWithMultiInheritedLet.setUpClass()
        self.spec_with_multi_inherited_let = self.SpecWithMultiInheritedLet()
        self.spec_with_multi_inherited_let.setUp()

    def tearDown(self):
        self.spec_with_multi_inherited_let.tearDown()
        self.SpecWithMultiInheritedLet.tearDownClass()

    def test_supports_multiple_inheritence(self):
        self.assertEqual('some stuff', self.spec_with_multi_inherited_let.thing)
        self.assertEqual('some other stuff', self.spec_with_multi_inherited_let.thing2)
        