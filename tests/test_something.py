"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from vcat.something import Something

class TestSomething(unittest.TestCase):
    def test_map(self):
        something = Something("asdfasdf")
        self.assertEqual(something.map(lambda x: len(x)), Something(8))

    def test_is_present(self):
        something = Something("yo")
        self.assertTrue(something.is_present())

    def test_get(self):
        something = Something(45)
        self.assertEqual(something.get(), 45)

    def test_get_or_else(self):
        something = Something(1234)
        self.assertEqual(something.get_or_else("hey there"), 1234)

    def test_eq_something_and_same_thing(self):
        self.assertEqual(Something(432), Something(432))

    def test_eq_something_and_something_else(self):
        self.assertNotEqual(Something(432), Something(431))

    def test_eq_something_and_anything_else(self):
        from vcat.nothing import Nothing

        self.assertNotEqual(Something(252343), Nothing())
        self.assertNotEqual(Something("asdf"), "asdf")
        self.assertNotEqual(Something(22), {"dict": 22})

    def test_fallback_returns_nothing(self):
        from vcat.nothing import Nothing

        something = Something("asdf")
        self.assertEqual(Something("asdf"), something.fallback(lambda: Nothing()))

    def test_fallback_returns_something(self):
        something = Something(5)
        self.assertEqual(Something(5), something.fallback(lambda: Something(5)))

    def test_fallback_returns_none(self):
        something = Something({"dict": 44})
        self.assertEqual(Something({"dict": 44}), something.fallback(lambda: None))

    def test_fallback_returns_something_else(self):
        something = Something(77)
        self.assertEqual(Something(77), something.fallback(lambda: 88))