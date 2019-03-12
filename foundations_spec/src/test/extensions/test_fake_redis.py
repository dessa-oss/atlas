"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_spec.extensions import let_fake_redis

class TestFakeRedis(unittest.TestCase):
    
    def test_is_a_let(self):
        from foundations_spec.helpers import let

        fake_redis = let_fake_redis()
        self.assertTrue(isinstance(fake_redis, let))

    def test_returns_a_fake_redis(self):
        from fakeredis import FakeRedis

        fake_redis = let_fake_redis()(self)
        self.assertTrue(isinstance(fake_redis, FakeRedis))

    def test_redis_flush_between_instances(self):
        fake_redis = let_fake_redis()(self)
        fake_redis.set('hello', 'world') 

        fake_redis_2 = let_fake_redis()(self)

        self.assertEqual(0, len(fake_redis_2.keys('*')))