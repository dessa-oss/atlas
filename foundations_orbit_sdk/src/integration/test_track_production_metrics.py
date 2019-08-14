"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestTrackProductionMetrics(Spec):

    @set_up
    def set_up(self):
        from foundations_contrib.global_state import redis_connection

        self._redis = redis_connection
        self._redis.flushall()

    @skip('not implemented')
    def test_track_production_metrics_stores_metrics_in_redis(self):
        self._track_some_metrics('october')
        self._track_some_metrics('january')

        production_metrics_from_redis = self._redis.hgetall(f'models:{self.job_id}:production_metrics')
        production_metrics = {metric_name.decode(): pickle.loads(serialized_metrics) for metric_name, serialized_metrics in production_metrics_from_redis.items()}

        production_metrics['MSE'].sort(key=lambda entry: entry[0])

        expected_production_metrics = {
            'roc_auc': [('october', 66), ('january', 66)],
            'MSE': [('january', 1), ('january_again', 2), ('october', 1), ('october_again', 2)]
        }

        self.assertEqual(expected_production_metrics, production_metrics)

    def _track_some_metrics(self, eval_period):
        from foundations_orbit import track_production_metrics

        track_production_metrics('roc_auc', {eval_period: 66})
        track_production_metrics('MSE', {eval_period: 1, f'{eval_period}_again': 2})