"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_internal.testing.helpers import *

def let_fake_redis():
    @let
    def _callback(self):
        from fakeredis import FakeRedis
        redis = FakeRedis()
        redis.flushall()
        return redis
    return _callback