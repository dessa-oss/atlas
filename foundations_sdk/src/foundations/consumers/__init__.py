"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
import redis 

from foundations.global_state import message_router
from foundations.consumers.job_metric_consumer import JobMetricConsumer
from foundations.consumers.job_metric_name_consumer import JobMetricNameConsumer


class MagicRedis(object):

    def __init__(self):
        self._redis_connection = None

    def __getattr__(self, name):
        conn = self._redis()
        inner = getattr(conn, name)
        if inner:
            return inner

        raise AttributeError('NOOPE')            

    def _redis(self):
        if self._redis_connection is None:
            self._redis_connection = self._make_redis()
        return self._redis_connection

    def _make_redis(self):
        import redis
        return redis.Redis()

_redis = MagicRedis()
message_router.add_listener(JobMetricConsumer(_redis), 'stage_log_middleware')
message_router.add_listener(JobMetricNameConsumer(_redis), 'stage_log_middleware')