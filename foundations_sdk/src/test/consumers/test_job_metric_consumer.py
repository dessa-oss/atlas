"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations.consumers.job_metric_consumer import JobMetricConsumer


class TestJobMetricConsumer(unittest.TestCase):

    def setUp(self):
        self._redis = Mock()
        self._consumer = JobMetricConsumer(self._redis)

    def test_call_method(self):
        from foundations.fast_serializer import serialize
        self._consumer.call(
            {'key': 'key1', 'value': 'value1', 'job_id': 123}, None, None)
        self._redis.set.assert_called_with(
            'job:123', serialize((None, 'key1', 'value1')))

    def test_call_method_different_values(self):
        from foundations.fast_serializer import serialize
        key = 'key2'
        value = 'value2'
        job_id = 19283
        timestamp = 1245
        self._consumer.call({'key': key, 'value': value,
                             'job_id': job_id}, timestamp, None)
        self._redis.set.assert_called_with(
            'job:19283', serialize((timestamp, key, value)))
