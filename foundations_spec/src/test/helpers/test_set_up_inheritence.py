
import unittest

from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers import *

from mock import MagicMock

class TestSetUpInheritence(unittest.TestCase):

    class MockSpecBase(Spec):
        @set_up
        def set_up(self):
            self.called = True
    class MockSpec(MockSpecBase):
        pass

    def setUp(self):
        self.MockSpec.setUpClass()
        self.spec = self.MockSpec()
        self.spec.setUp()

    def tearDown(self):
        self.spec.tearDown()
        self.MockSpec.tearDownClass()

    def test_calls_parent_set_up(self):
        self.assertTrue(self.spec.called)

