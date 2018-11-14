"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations.global_state import message_router
from foundations.consumers.job_metric_consumer import JobMetricConsumer
from foundations.consumers.job_metric_name_consumer import JobMetricNameConsumer


def _create_redis_instance_and_add_consumers():
    import redis
    from foundations.helpers.lazy_redis import LazyRedis
    _redis = LazyRedis(redis.Redis)

    message_router.add_listener(
        JobMetricConsumer(_redis), 'job_metrics')
    message_router.add_listener(
        JobMetricNameConsumer(_redis), 'job_metrics')


_create_redis_instance_and_add_consumers()
