"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_contrib.null_cache_backend import NullCacheBackend


class TestNullCacheBackend(unittest.TestCase):
    def setUp(self):
        self.backend = NullCacheBackend()

    def test_round_trip(self):
        self.backend.set("asdf", "asdf", {"asdf": "asdf"}, asdf=222)
        data = self.backend.get("asdf")
        metadata = self.backend.get_metadata("asdf")
        self.assertIsNone(data)
        self.assertIsNone(metadata)
