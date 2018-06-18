import unittest

from vcat.compat import compat_raise

class DummyException(Exception):
    def __init__(self, test_val):
        super(DummyException, self).__init__(test_val)

class TestCompat(unittest.TestCase):
    def test_compat_raise(self):
        try:
            compat_raise(DummyException, "test_value")
        except DummyException as e:
            self.assertEqual(str(e), "test_value")
        except Exception as e:
            self.fail("Did not properly throw exception")