"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

from foundations_spec import *

from foundations_orbit_rest_api.v1.controllers import MonitorJobsController

class TestMonitorJobsController(Spec):

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
    def job_id_3(self):
        return f'{self.project_name}-{self.monitor_name}_{self.faker.random_int()}'

    @set_up
    def set_up(self):
        import fakeredis

        self._redis = self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())
        self._redis.flushall()

        self.controller = MonitorJobsController()

        self.controller.params = {
            'project_name': self.project_name,
            'monitor_name': self.monitor_name,
            'job_id': self.job_id
        }

    def _data_to_set(self):
        return [
            {
                'project': 'so',
                'job_id': self.job_id,
                'user': 'pairing',
                'start_time': 1571931153.0313132,
                'completed_time': 1571931153.6426458,
                'creation_time': 1571931153.0313132,
                'state': 'completed'
            }
            , {
                'project': 'so',
                'job_id': self.job_id_2,
                'user': 'pairing',
                'start_time': 1571931156.550436,
                'creation_time': 1571931156.550436,
                'state': 'running'
            },
            {
                'project': 'so',
                'job_id': self.job_id_3,
                'user': 'pairing',
                'start_time': 1501931156.550436,
                'creation_time': 1501931156.550436,
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
                'output_metrics': [],
                'status': 'running',
                'start_time': 1571931156.550436,
                'completed_time': None,
                'creation_time': 1571931156.550436,
                'tags': {}
            },
            {
                'project_name': 'so',
                'job_id': self.job_id_3,
                'user': 'pairing',
                'job_parameters': {},
                'output_metrics': [],
                'status': 'running',
                'start_time': 1501931156.550436,
                'completed_time': None,
                'creation_time': 1501931156.550436,
                'tags': {}
            },
            {
                'project_name': 'so',
                'job_id': self.job_id,
                'user': 'pairing',
                'job_parameters': {},
                'output_metrics': [],
                'status': 'completed',
                'start_time': 1571931153.0313132,
                'completed_time': 1571931153.6426458,
                'creation_time': 1571931153.0313132,
                'tags': {}
            },
        ]

    def test_index_returns_404_if_monitor_does_not_exist(self):
        response = self.controller.index()

        self.assertEqual(404, response.status())

    def test_index_returns_200_if_monitor_exists_in_redis(self):
        self._create_job_information_for_monitor(self.project_name, self.monitor_name, self._data_to_set())

        response = self.controller.index()

        self.assertEqual(200, response.status())

    def test_index_returns_monitor_jobs_payload_for_monitors_in_redis(self):
        self._create_job_information_for_monitor(self.project_name, self.monitor_name, self._data_to_set())
        
        actual_data = self.controller.index().as_json()
        actual_data = sorted(actual_data, key=lambda data: data['job_id'])

        expected_data = self._expected_data()
        expected_data = sorted(expected_data, key=lambda data: data['job_id'])

        self.assertEqual(expected_data, actual_data)

    def test_index_returns_resource_with_resource_name_monitors(self):
        self._create_job_information_for_monitor(self.project_name, self.monitor_name, self._data_to_set())

        result = self.controller.index()

        self.assertEqual('Monitors', result.resource_name())
    
    def test_delete_returns_resource_with_resource_name_monitors(self):
        result = self.controller.delete()

        self.assertEqual('Monitors', result.resource_name())

    def test_delete_returns_404_if_monitor_name_does_not_exist_redis(self):
        result = self.controller.delete()

        self.assertEqual(404, result.status())

    def test_delete_returns_200_if_monitor_name_exists_in_redis(self):
        self._create_job_information_for_monitor(self.project_name, self.monitor_name, self._data_to_set())

        result = self.controller.delete()

        self.assertEqual(200, result.status())

    def test_delete_returns_data_with_error_message_if_report_not_in_redis(self):
        response = self.controller.delete()

        expected_response_data = {
            'project_name': self.project_name,
            'monitor_name': self.monitor_name,
            'job_id': self.job_id,
            'error': 'does not exist'
        }

        self.assertEqual(expected_response_data, response.as_json())

    def test_delete_removes_job_from_job_list_in_redis(self):
        import time

        self._create_job_information_for_monitor(self.project_name, self.monitor_name, self._data_to_set())

        result = self.controller.delete()
        result.evaluate()

        self.controller.params = {
            'project_name': self.project_name,
            'monitor_name': self.monitor_name,
        }

        jobs_list = self.controller.index().as_json()

        expected_result = self._expected_data()

        index_to_delete = 0
        for index, result in enumerate(expected_result):
            if result['job_id'] == self.job_id:
                index_to_delete = index
                break

        del expected_result[index_to_delete]

        self.assertEqual(expected_result, jobs_list)
    
    def test_get_job_returns_results_in_ascending_order(self):
        import time
        self._create_job_information_for_monitor(self.project_name, self.monitor_name, self._data_to_set())

        self.controller.params = {
            'project_name': self.project_name,
            'monitor_name': self.monitor_name,
            # 'sort': 'asc'
        }

        jobs_list = self.controller.index().as_json()

        expected_result = self._expected_data()
        # expected_result.reverse()

        self.assertEqual(expected_result, jobs_list)

    def _create_job_information_for_monitor(self, project_name, monitor_name, job_data):
        for job_listing in job_data:
            job_id = job_listing.pop('job_id')
            self._redis.sadd(f'projects:{project_name}:monitors:{monitor_name}:jobs', job_id)
            for job_key, job_value in job_listing.items():
                self._redis.set(f'jobs:{job_id}:{job_key}', job_value)

