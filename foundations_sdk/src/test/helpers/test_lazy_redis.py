"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock
from foundations.helpers.lazy_redis import LazyRedis

class TestLazyRedis(unittest.TestCase):

    class MockObject(object):
        def __init__(self):
            self.value = 5
    
    def setUp(self):
        pass
    
    def test_get_attr_returns_attribute(self):
        lazy_redis = LazyRedis(self._callback)
        self.assertEqual(lazy_redis.value, 5)
    
    def test_get_attr_raises_attribute_error(self):
        lazy_redis = LazyRedis(self._callback)
        with self.assertRaises(AttributeError) as context:
            lazy_redis.redis
        self.assertIn("'MockObject' object has no attribute 'redis'", context.exception.args)

    
    def _callback(self):
        return self.MockObject()
