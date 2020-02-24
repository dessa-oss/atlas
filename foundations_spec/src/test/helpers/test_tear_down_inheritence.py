
import unittest

from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers import *

from mock import MagicMock

class TestTearDownInheritence(unittest.TestCase):

    class MockSpecBase(Spec):
        @tear_down
        def tear_down(self):
            self.called = True
    class MockSpec(MockSpecBase):
        pass

    def setUp(self):
        self.MockSpec.setUpClass()
        self.spec = self.MockSpec()
        self.spec.setUp()
        self.spec.tearDown()
        self.MockSpec.tearDownClass()

    def test_calls_parent_tear_down(self):
        self.assertTrue(self.spec.called)

