"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from fakeredis import FakeRedis

from foundations_model_package.redis_actions import *

class TestRedisActions(Spec):

    @let
    def job_id(self):
        return self.faker.uuid4()

    @set_up
    def set_up(self):
        self.redis = self.patch('foundations_contrib.global_state.redis_connection', FakeRedis())

    @tear_down
    def tear_down(self):
        self.redis.flushall()

    def test_indicate_model_ran_increments_appropriate_key_in_redis(self):
        indicate_model_ran_to_redis(self.job_id)
        self.assertEqual(b'1', self.redis.get(f'models:{self.job_id}:served'))

    def test_indicate_model_ran_twice_increments_appropriate_key_in_redis_twice(self):
        indicate_model_ran_to_redis(self.job_id)
        indicate_model_ran_to_redis(self.job_id)
        self.assertEqual(b'2', self.redis.get(f'models:{self.job_id}:served'))