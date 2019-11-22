"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_orbit_rest_api.v1.models.monitor import Monitor

class TestMonitor(Spec):

    @let_now
    def redis_connection(self):
        import fakeredis
        return self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def monitor_name(self):
        return self.faker.word()
    
    @let
    def job_id(self):
        return f'{self.project_name}-{self.monitor_name}_{self.faker.random_int()}'

    @let
    def job_id_2(self):
        return f'{self.project_name}-{self.monitor_name}_{self.faker.random_int()}'

    @let
    def nonexistent_job_id(self):
        return self.faker.word()

    @set_up
    def set_up(self):
        self.redis_connection.flushall()

    def _data_to_set(self):
        return [
            {
                'project': 'so',
                'job_id': self.job_id,
                'user': 'pairing',
                'start_time': 1571931153.0313132,
                'completed_time': 1571931153.6426458,
                'state': 'completed'
            }
            , {
                'project': 'so',
                'job_id': self.job_id_2,
                'user': 'pairing',
                'start_time': 1571931156.550436,
                'state': 'running'
            }
        ]

    def _expected_data(self):
        return [
            {
                'project_name': 'so',
                'job_id': self.job_id_2,
                'user': 'pairing',
                'job_parameters': {},
                'input_params': [],
                'output_metrics': [],
                'status': 'running',
                'start_time': 1571931156.550436,
                'completed_time': None,
                'tags': {}
            },
            {
                'project_name': 'so',
                'job_id': self.job_id,
                'user': 'pairing',
                'job_parameters': {},
                'input_params': [],
                'output_metrics': [],
                'status': 'completed',
                'start_time': 1571931153.0313132,
                'completed_time': 1571931153.6426458,
                'tags': {}
            }
        ]
    
    def test_jobs_ids_from_monitors_dictionary_returns_none_if_monitor_does_not_exist(self):
        promise = Monitor.job_ids_from_monitors_dictionary(self.project_name, self.monitor_name, 'desc')
        self.assertEqual(None, promise.evaluate())

    def test_jobs_ids_from_monitors_dictionary_returns_data_from_redis(self):
        self._create_job_information_for_monitor(self.project_name, self.monitor_name, self._data_to_set())

        promise = Monitor.job_ids_from_monitors_dictionary(self.project_name, self.monitor_name, 'desc')

        expected_result = self._expected_data()
        expected_result = sorted(expected_result, key=lambda data: data['job_id'])
        result = promise.evaluate()
        result = sorted(result, key=lambda data: data['job_id'])
        
        self.assertEqual(expected_result, result)

    def test_delete_job_from_monitors_dictionary_removes_job_from_redis(self):
        self._create_job_information_for_monitor(self.project_name, self.monitor_name, self._data_to_set())

        delete_promise = Monitor.delete_job(self.project_name, self.monitor_name, self.job_id)
        delete_promise.evaluate()

        promise = Monitor.job_ids_from_monitors_dictionary(self.project_name, self.monitor_name, 'desc')

        expected_result = self._expected_data()
        index_to_delete = 0
        for index, result in enumerate(expected_result):
            if result['job_id'] == self.job_id:
                index_to_delete = index
                break

        del expected_result[index_to_delete]

        self.assertEqual(expected_result, promise.evaluate())

    def test_delete_job_from_monitors_dictionary_return_deleted_job_id(self):
        self._create_job_information_for_monitor(self.project_name, self.monitor_name, self._data_to_set())

        promise = Monitor.delete_job(self.project_name, self.monitor_name, self.job_id)
        self.assertEqual(self.job_id, promise.evaluate())

    def test_delete_job_from_monitor_dictionary_returns_none_if_monitor_does_not_exist(self):
        promise = Monitor.delete_job(self.project_name, self.monitor_name, self.job_id)
        self.assertIsNone(promise.evaluate())

    def test_delete_job_from_monitor_dictionary_returns_none_if_job_does_not_exist(self):
        self._create_job_information_for_monitor(self.project_name, self.monitor_name, self._data_to_set())

        promise = Monitor.delete_job(self.project_name, self.monitor_name, self.nonexistent_job_id)
        self.assertIsNone(promise.evaluate())

    def _create_job_information_for_monitor(self, project_name, monitor_name, job_data):
        for job_listing in job_data:
            job_id = job_listing.pop('job_id')
            self.redis_connection.sadd(f'projects:{self.project_name}:monitors:{self.monitor_name}:jobs', job_id)
            for job_key, job_value in job_listing.items():
                self.redis_connection.set(f'jobs:{job_id}:{job_key}', job_value)
