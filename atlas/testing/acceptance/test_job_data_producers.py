
from foundations_spec import *
from mock import Mock
from acceptance.mixins.run_local_job import RunLocalJob


class TestJobDataProducers(Spec, RunLocalJob):

    @let
    def user_name(self):
        from getpass import getuser
        return getuser()

    @set_up
    def set_up(self):
        from acceptance.cleanup import cleanup
        from foundations.global_state import redis_connection

        cleanup()
        self._redis = redis_connection
        self._redis.delete('foundations_testing_job_id')

    def test_produces_proper_data(self):
        from foundations_contrib.job_data_redis import JobDataRedis

        self._deploy_job_file('acceptance/fixtures/job_data_production', entrypoint='success.py')
        all_job_data = JobDataRedis.get_all_jobs_data('job_data_production', self._redis)

        job_data = [data for data in all_job_data if data['job_id'] == self.job_id][0]
        self.assertEqual('job_data_production', job_data['project_name'])
        self.assertEqual(self.user_name, job_data['user'])
        self.assertEqual('completed', job_data['status'])
        self.assertTrue(isinstance(job_data['start_time'], float))
        self.assertTrue(isinstance(job_data['completed_time'], float))
        self.assertGreater(len(job_data['output_metrics']), 0)

    def test_produces_completed_job_data(self):
        from foundations_internal.fast_serializer import deserialize
        from time import time

        self._deploy_job_file('acceptance/fixtures/job_data_production', entrypoint='success.py')
        current_time = time()

        serialized_metrics = self._redis.lrange(
            f'jobs:{self.job_id}:metrics', 0, -1)
        metrics = [deserialize(data) for data in serialized_metrics]
        metric_1, metric_2, metric_3 = metrics

        self.assertTrue(current_time - metric_1[0] < 2)
        self.assertTrue(current_time - metric_2[0] < 2)
        self.assertTrue(current_time - metric_3[0] < 2)

        self.assertEqual('hello', metric_1[1])
        self.assertEqual('hello', metric_2[1])
        self.assertEqual('world', metric_3[1])

        self.assertEqual(1, metric_1[2])
        self.assertEqual(2, metric_2[2])
        self.assertEqual(3, metric_3[2])

        metric_keys = self._redis.smembers(
            'project:job_data_production:metrics')
        metric_keys = set([data.decode() for data in metric_keys])
        self.assertEqual({'hello', 'world'}, metric_keys)

        state = self._redis.get(f'jobs:{self.job_id}:state').decode()
        self.assertEqual('completed', state)

        project_name = self._redis.get(f'jobs:{self.job_id}:project').decode()
        self.assertEqual('job_data_production', project_name)

        user_name = self._redis.get(f'jobs:{self.job_id}:user').decode()
        self.assertEqual(self.user_name, user_name)

        completed_time = self._redis.get(
            f'jobs:{self.job_id}:completed_time').decode()
        completed_time = float(completed_time)
        self.assertTrue(current_time - completed_time < 2)

        start_time = self._redis.get(f'jobs:{self.job_id}:start_time').decode()
        start_time = float(start_time)
        self.assertTrue(current_time - start_time > 0.01)
        self.assertTrue(current_time - start_time < 10)

        creation_time = self._redis.get(
            f'jobs:{self.job_id}:creation_time').decode()
        creation_time = float(creation_time)
        self.assertTrue(current_time - creation_time > 0.01)
        self.assertTrue(current_time - creation_time < 120)

        running_jobs = self._redis.smembers(
            'project:job_data_production:jobs:running')
        running_jobs = set([data.decode() for data in running_jobs])
        self.assertIn(self.job_id, running_jobs)
        
    def test_produces_failed_job_data(self):
        self._deploy_job_file('acceptance/fixtures/job_data_production', entrypoint='fail.py')

        state = self._redis.get(f'jobs:{self.job_id}:state').decode()
        self.assertEqual('failed', state)

        serialized_error_information = self._redis.get(
            f'jobs:{self.job_id}:error_information')
        error_information = self._foundations_deserialize(serialized_error_information)

        self.assertEqual("<class 'Exception'>", error_information['type'])

        self.assertEqual('', error_information['exception'])
        self.assertIsNotNone(error_information['traceback'])

    def _foundations_deserialize(self, serialized_value):
        from foundations_internal.foundations_serializer import deserialize
        return deserialize(serialized_value)