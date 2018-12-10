"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

from foundations_contrib.option import Option


class TestOption(unittest.TestCase):
    def test_option_with_none(self):
        from foundations_contrib.nothing import Nothing

        self.assertEqual(Nothing(), Option(None))

    def test_option_with_nothing(self):
        from foundations_contrib.nothing import Nothing

        self.assertEqual(Nothing(), Option(Nothing()))

    def test_option_with_something(self):
        from foundations_contrib.something import Something

        self.assertEqual(Something(55), Option(Something(55)))

    def test_option_with_anything_else(self):
        from foundations_contrib.something import Something

        self.assertEqual(Something("asdfasdfasdf"), Option("asdfasdfasdf"))
