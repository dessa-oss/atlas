"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations.nothing import Nothing

class TestNothing(unittest.TestCase):
    def test_map(self):
        nothing = Nothing()
        self.assertEqual(nothing.map(lambda x: x + 1), Nothing())

    def test_is_present(self):
        nothing = Nothing()
        self.assertFalse(nothing.is_present())

    def test_get(self):
        nothing = Nothing()
        try:
            nothing.get()
            self.fail("Should not be able to #get Nothing")
        except ValueError as err:
            self.assertEqual("Tried #get on Nothing", str(err))

    def test_get_or_else(self):
        nothing = Nothing()
        self.assertEqual(nothing.get_or_else("hey there"), "hey there")

    def test_eq_nothing_and_nothing(self):
        self.assertEqual(Nothing(), Nothing())

    def test_eq_nothing_and_anything_else(self):
        from foundations.something import Something

        self.assertNotEqual(Nothing(), Something(235))
        self.assertNotEqual(Nothing(), "asdf")
        self.assertNotEqual(Nothing(), {"dict": 11})

    def test_fallback_returns_nothing(self):
        nothing = Nothing()
        self.assertEqual(Nothing(), nothing.fallback(lambda: Nothing()))

    def test_fallback_returns_something(self):
        from foundations.something import Something

        nothing = Nothing()
        self.assertEqual(Something(5), nothing.fallback(lambda: Something(5)))

    def test_fallback_returns_none(self):
        nothing = Nothing()
        self.assertEqual(Nothing(), nothing.fallback(lambda: None))

    def test_fallback_returns_something_else(self):
        from foundations.something import Something

        nothing = Nothing()
        self.assertEqual(Something(77), nothing.fallback(lambda: 77))