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
        expected_input_parameters = {'random_input_data': self._str_random_uuid()}
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

        job_parameter_names = self._redis.smembers('projects:{}:job_parameter_names'.format(project_name))
        self.assertEqual(set([b'random_job_data']), job_parameter_names)

        input_parameter_names = self._redis.smembers('projects:{}:input_parameter_names'.format(project_name))
        self.assertEqual(set([b'random_input_data']), input_parameter_names)

        queued_jobs = self._redis.smembers('project:{}:jobs:queued'.format(project_name))
        self.assertEqual(set([byte_string(job_id)]), queued_jobs)

        job_parameters = self._get_and_deserialize('jobs:{}:parameters'.format(job_id))
        self.assertEqual(expected_job_parameters, job_parameters)

        state = self._redis.get('jobs:{}:state'.format(job_id))
        self.assertEqual(b'queued', state)

        job_project_name = self._redis.get('jobs:{}:project'.format(job_id))
        self.assertEqual(byte_string(project_name), job_project_name)

        job_user = self._redis.get('jobs:{}:user'.format(job_id))
        self.assertEqual(byte_string(user), job_user)

        string_creation_time = self._redis.get('jobs:{}:creation_time'.format(job_id))
        creation_time = float(string_creation_time.decode())
        self.assertTrue(current_time - creation_time < 0.1)
        
        input_parameters = self._get_and_deserialize('jobs:{}:input_parameters'.format(job_id))
        self.assertEqual(expected_input_parameters, input_parameters)

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

        running_and_completed_jobs = self._redis.smembers('project:{}:jobs:running'.format(project_name))
        self.assertEqual(set([byte_string(job_id)]), running_and_completed_jobs)

        state = self._redis.get('jobs:{}:state'.format(job_id))
        self.assertEqual(b'running', state)

        string_start_time = self._redis.get('jobs:{}:start_time'.format(job_id))
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

        string_completed_time = self._redis.get('jobs:{}:completed_time'.format(job_id))
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

        state = self._get_and_deserialize('jobs:{}:error_information'.format(job_id))
        self.assertEqual(expected_input_parameters, state)

        string_completed_time = self._redis.get('jobs:{}:completed_time'.format(job_id))
        completed_time = float(string_completed_time.decode())
        self.assertTrue(current_time - completed_time < 0.1)

    def _get_and_deserialize(self, key):
        import json
        
        serialized_data = self._redis.get(key)
        return json.loads(serialized_data)
    
    def _random_name(self):
        return self._faker.name()

    def _str_random_uuid(self):
        import uuid
        return str(uuid.uuid4())
