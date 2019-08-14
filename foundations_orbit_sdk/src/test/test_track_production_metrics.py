"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_orbit import track_production_metrics
import fakeredis
import pickle

class TestTrackProductionMetrics(Spec):

    mock_redis = let_patch_mock('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())
    mock_context = let_patch_instance('foundations_contrib.global_state.current_foundations_context')

    @let
    def job_id(self):
        return self.faker.uuid4()

    @set_up
    def set_up(self):
        self.mock_context.job_id.return_value = self.job_id

    @tear_down
    def tear_down(self):
        self.mock_redis.flushall()

    def test_track_production_metrics_can_track_empty_metric(self):
        track_production_metrics('some_key', {})
        production_metrics_from_redis = self.mock_redis.hgetall(f'models:{self.job_id}:production_metrics')
        production_metrics = {metric_name.decode(): pickle.loads(serialized_metrics) for metric_name, serialized_metrics in production_metrics_from_redis.items()}
        self.assertEqual({'some_key': []}, production_metrics)

    def test_track_production_metrics_with_nonexistent_job_id_throws_exception(self):
        self.mock_context.job_id.side_effect = ValueError()
    
        with self.assertRaises(RuntimeError) as error_context:
            track_production_metrics('some_key', {})
        
        self.assertIn('Job ID not set', error_context.exception.args)


