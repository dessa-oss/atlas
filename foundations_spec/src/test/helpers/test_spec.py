"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers import *

class TestSpec(unittest.TestCase):

    class MockSpec(Spec):
        pass

    def setUp(self):
        self.MockSpec.setUpClass()
        self.spec = self.MockSpec()

    def tearDown(self):
        self.spec.tearDown()
        self.MockSpec.tearDownClass()
    
    def test_has_faker(self):
        import faker

        self.spec.setUp()
        self.assertIsInstance(self.spec.faker, faker.generator.Generator)
