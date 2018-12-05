"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock
from foundations_contrib.helpers.lazy_redis import LazyRedis


class TestLazyRedis(unittest.TestCase):

    class MockObject(object):
        def __init__(self):
            self.value = 5
            self.name = 'mock'

    def setUp(self):
        pass

    def test_get_attr_returns_attribute_value(self):
        lazy_redis = LazyRedis(self._callback)
        self.assertEqual(lazy_redis.value, 5)

    def test_get_attr_returns_attribute_name(self):
        lazy_redis = LazyRedis(self._callback)
        self.assertEqual(lazy_redis.name, 'mock')

    def test_get_attr_raises_attribute_error(self):
        lazy_redis = LazyRedis(self._callback)
        with self.assertRaises(AttributeError) as context:
            lazy_redis.redis
        self.assertIn("'MockObject' object has no attribute 'redis'",
                      context.exception.args)

    def test_get_attr_raises_attribute_error_different_attribute(self):
        lazy_redis = LazyRedis(self._callback)
        with self.assertRaises(AttributeError) as context:
            lazy_redis.potato
        self.assertIn("'MockObject' object has no attribute 'potato'",
                      context.exception.args)

    def _callback(self):
        return self.MockObject()
