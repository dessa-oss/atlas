"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock


class TestConsumers(unittest.TestCase):

    def setUp(self):
        from foundations.global_state import redis_connection
        import faker

        self._redis = redis_connection
        self._redis.flushall()
        self._faker = faker.Faker()

    def test_queue_job_consumers(self):
        from foundations.global_state import message_router
        from foundations.utils import byte_string
        from time import time

        project_name = self._str_random_uuid()
        job_id = self._str_random_uuid()
        expected_job_parameters = {'random_job_data': self._str_random_uuid()}
        expected_input_parameters = {
            'random_input_data': self._str_random_uuid()
        }
        user = self._random_name()

        message = {
            'project_name': project_name,
            'job_id': job_id,
            'job_parameters': expected_job_parameters,
            'input_parameters': expected_input_parameters,
            'user': user,
        }
        message_router.push_message('queue_job', message)
        current_time = time()

        parameter_key = 'projects:{}:job_parameter_names'.format(project_name)
        job_parameter_names = self._redis.smembers(parameter_key)
        self.assertEqual(set([b'random_job_data']), job_parameter_names)

        input_parameter_key = self._input_parameter_key(project_name)
        input_parameter_names = self._redis.smembers(input_parameter_key)
        self.assertEqual(set([b'random_input_data']), input_parameter_names)

        queued_job_key = 'project:{}:jobs:queued'.format(project_name)
        queued_jobs = self._redis.smembers(queued_job_key)
        self.assertEqual(set([byte_string(job_id)]), queued_jobs)

        job_parameters_key = 'jobs:{}:parameters'.format(job_id)
        job_parameters = self._get_and_deserialize(job_parameters_key)
        self.assertEqual(expected_job_parameters, job_parameters)

        job_state_key = 'jobs:{}:state'.format(job_id)
        state = self._redis.get(job_state_key)
        self.assertEqual(b'queued', state)

        job_project_key = 'jobs:{}:project'.format(job_id)
        job_project_name = self._redis.get(job_project_key)
        self.assertEqual(byte_string(project_name), job_project_name)

        job_user_key = 'jobs:{}:user'.format(job_id)
        job_user = self._redis.get(job_user_key)
        self.assertEqual(byte_string(user), job_user)

        creation_time_key = 'jobs:{}:creation_time'.format(job_id)
        string_creation_time = self._redis.get(creation_time_key)
        creation_time = float(string_creation_time.decode())
        self.assertTrue(current_time - creation_time < 0.1)

        input_parameters_key = 'jobs:{}:input_parameters'.format(job_id)
        input_parameters = self._get_and_deserialize(input_parameters_key)
        self.assertEqual(expected_input_parameters, input_parameters)

    def _input_parameter_key(self, project_name):
        return 'projects:{}:input_parameter_names'.format(project_name)

    def test_running_job_consumers(self):
        from foundations.global_state import message_router
        from foundations.utils import byte_string
        from time import time

        project_name = self._str_random_uuid()
        job_id = self._str_random_uuid()

        message = {
            'project_name': project_name,
            'job_id': job_id
        }
        message_router.push_message('run_job', message)
        current_time = time()

        running_jobs_key = 'project:{}:jobs:running'.format(project_name)
        running_and_completed_jobs = self._redis.smembers(running_jobs_key)
        expected_jobs = set([byte_string(job_id)])
        self.assertEqual(expected_jobs, running_and_completed_jobs)

        job_state_key = 'jobs:{}:state'.format(job_id)
        state = self._redis.get(job_state_key)
        self.assertEqual(b'running', state)

        start_time_key = 'jobs:{}:start_time'.format(job_id)
        string_start_time = self._redis.get(start_time_key)
        start_time = float(string_start_time.decode())
        self.assertTrue(current_time - start_time < 0.1)

    def test_completed_job_consumers(self):
        from foundations.global_state import message_router
        from time import time

        project_name = self._str_random_uuid()
        job_id = self._str_random_uuid()

        message = {
            'project_name': project_name,
            'job_id': job_id
        }
        message_router.push_message('complete_job', message)
        current_time = time()

        state = self._redis.get('jobs:{}:state'.format(job_id))
        self.assertEqual(b'completed', state)

        completed_time_key = 'jobs:{}:completed_time'.format(job_id)
        string_completed_time = self._redis.get(completed_time_key)
        completed_time = float(string_completed_time.decode())
        self.assertTrue(current_time - completed_time < 0.1)

    def test_failed_job_consumers(self):
        from foundations.global_state import message_router
        from time import time

        project_name = self._str_random_uuid()
        job_id = self._str_random_uuid()
        expected_input_parameters = {'broken_data': self._random_name()}

        message = {
            'project_name': project_name,
            'job_id': job_id,
            'error_information': expected_input_parameters
        }
        message_router.push_message('fail_job', message)
        current_time = time()

        state = self._redis.get('jobs:{}:state'.format(job_id))
        self.assertEqual(b'Error', state)

        error_information_key = 'jobs:{}:error_information'.format(job_id)
        state = self._get_and_deserialize(error_information_key)
        self.assertEqual(expected_input_parameters, state)

        completed_time_key = 'jobs:{}:completed_time'.format(job_id)
        string_completed_time = self._redis.get(completed_time_key)
        completed_time = float(string_completed_time.decode())
        self.assertTrue(current_time - completed_time < 0.1)

    def test_job_metric_consumers(self):
        from foundations.global_state import message_router
        from foundations.fast_serializer import deserialize
        from foundations.utils import byte_string
        from time import time

        project_name = self._str_random_uuid()
        job_id = self._str_random_uuid()
        key = 'best_metric_ever'
        value = 42

        message = {
            'project_name': project_name,
            'job_id': job_id,
            'key': key,
            'value': value
        }

        message_router.push_message('job_metrics', message)
        current_time = time()

        job_metrics_key = 'job:{}:metrics'.format(job_id)
        job_metrics = self._redis.get(job_metrics_key)
        job_metrics = deserialize(job_metrics)

        self.assertTrue(current_time - job_metrics[0] < 0.1)
        self.assertEqual(key, job_metrics[1])
        self.assertEqual(value, job_metrics[2])

        project_metrics_key = 'project:{}:metrics'.format(project_name)
        project_metric_name = self._redis.smembers(project_metrics_key)
        self.assertEqual(project_metric_name, set([byte_string(key)]))

    def _get_and_deserialize(self, key):
        import json

        serialized_data = self._redis.get(key)
        return json.loads(serialized_data)

    def _random_name(self):
        return self._faker.name()

    def _str_random_uuid(self):
        import uuid
        return str(uuid.uuid4())
