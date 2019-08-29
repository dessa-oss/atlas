"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_orbit_rest_api.production_metrics import all_production_metrics

class TestProductionMetrics(Spec):
    
    @let_now
    def redis_connection(self):
        import fakeredis
        return self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())

    @tear_down
    def tear_down(self):
        self.redis_connection.flushall()

    @let
    def job_id(self):
        return self.faker.uuid4()

    def test_all_production_metrics_returns_empty_dictionary_if_job_not_in_redis(self):
        self.assertEqual({}, all_production_metrics(self.job_id))