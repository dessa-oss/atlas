"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock


class TestJobDataProducers(unittest.TestCase):

    def setUp(self):
        from foundations.global_state import redis_connection

        self._redis = redis_connection
        self._redis.flushall()

    def test_produces_completed_job_data(self):
        from foundations import create_stage
        from foundations import Hyperparameter
        from foundations import log_metric
        from foundations.global_state import foundations_context
        from foundations.fast_serializer import deserialize
        from time import time

        @create_stage
        def dummy_data():
            return 999

        @create_stage
        def function(some_argument, some_placeholder, some_stage):
            log_metric('hello', 1)
            log_metric('hello', 2)
            log_metric('world', 3)
            return 5

        provenance = foundations_context.pipeline_context().provenance
        provenance.project_name = 'project_with_successful_jobs'

        stage = function(
            999,
            some_placeholder=Hyperparameter('some_run_data'),
            some_stage=dummy_data()
        )
        deployment = stage.run(some_run_data=777, job_name='successful_job')
        deployment.wait_for_deployment_to_complete()
        current_time = time()

        serialized_metrics = self._redis.lrange(
            'job:successful_job:metrics', 0, -1)
        metrics = [deserialize(data) for data in serialized_metrics]
        metric_1, metric_2, metric_3 = metrics

        self.assertTrue(current_time - metric_1[0] < 1)
        self.assertTrue(current_time - metric_2[0] < 1)
        self.assertTrue(current_time - metric_3[0] < 1)

        self.assertEqual('hello', metric_1[1])
        self.assertEqual('hello', metric_2[1])
        self.assertEqual('world', metric_3[1])

        self.assertEqual(1, metric_1[2])
        self.assertEqual(2, metric_2[2])
        self.assertEqual(3, metric_3[2])

        metric_keys = self._redis.smembers(
            'project:project_with_successful_jobs:metrics')
        metric_keys = set([data.decode() for data in metric_keys])
        self.assertEqual(set(['hello', 'world']), metric_keys)

        state = self._redis.get('jobs:successful_job:state').decode()
        self.assertEqual('completed', state)

        completed_time = self._redis.get('jobs:successful_job:completed_time').decode()
        completed_time = float(completed_time)
        self.assertTrue(current_time - completed_time < 1)

        start_time = self._redis.get('jobs:successful_job:start_time').decode()
        start_time = float(start_time)
        self.assertTrue(current_time - start_time > 0.25)
        self.assertTrue(current_time - start_time < 10)

        running_jobs = self._redis.smembers('project:project_with_successful_jobs:jobs:running')
        running_jobs = set([data.decode() for data in running_jobs])
        self.assertEqual(set(['successful_job']), running_jobs)

    def test_produces_failed_job_data(self):
        from foundations import create_stage
        import json

        @create_stage
        def function():
            raise Exception('I died!')

        stage = function()
        deployment = stage.run(job_name='failed_job')
        deployment.wait_for_deployment_to_complete()

        state = self._redis.get('jobs:failed_job:state').decode()
        self.assertEqual('Error', state)

        serialized_error_information = self._redis.get('jobs:failed_job:error_information')
        error_information = json.loads(serialized_error_information)

        self.assertEqual("<class 'Exception'>", error_information['type']) 
        self.assertEqual('I died!', error_information['exception'])
        self.assertIsNotNone(error_information['traceback'])