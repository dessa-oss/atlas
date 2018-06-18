"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

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