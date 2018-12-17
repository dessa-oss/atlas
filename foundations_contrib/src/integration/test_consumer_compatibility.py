"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock


class TestConsumerCompatibility(unittest.TestCase):

    def setUp(self):
        from foundations.global_state import redis_connection
        from uuid import uuid4

        self._redis = redis_connection
        self._uuid = str(uuid4())
    
    def test_can_load_json_input_parameters(self):
        from foundations_contrib.consumers.jobs.queued.input_parameters import InputParameters
        import json

        consumer = InputParameters(self._redis, json)
        consumer.call({'job_id': self._uuid, 'input_parameters': ['first param', 'second param']}, 0, {})

        self.assertEqual(['first param', 'second param'], self._get_redis_data(self._uuid)['input_params'])
        
    def _get_redis_data(self, job_id):
        from foundations_contrib.job_data_redis import JobDataRedis
        from foundations_contrib.redis_pipeline_wrapper import RedisPipelineWrapper

        async_redis = RedisPipelineWrapper(self._redis.pipeline())
        future = JobDataRedis(async_redis, job_id).get_job_data()
        async_redis.execute()

        return future.get()

