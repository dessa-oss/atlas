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
        from foundations.global_state import message_router
        from foundations.global_state import config_manager
        from foundations_internal.pipeline_context import PipelineContext
        from foundations_internal.pipeline import Pipeline
        from slackclient import SlackClient
        import faker
        import os

        self._redis = redis_connection
        self._redis.flushall()
        self._faker = faker.Faker()

        self._pipeline_context = PipelineContext()

        self._project_name = self._str_random_uuid()
        self._pipeline_context.provenance.project_name = self._project_name

        self._job_id = self._str_random_uuid()
        self._pipeline_context.file_name = self._job_id

        self._user = self._random_name()
        self._pipeline_context.provenance.user_name = self._user

        self._pipeline = Pipeline(self._pipeline_context)

        self._message_router = message_router

        self._slack_client = SlackClient(os.environ['FOUNDATIONS_TESTING_SLACK_TOKEN'])
        self._testing_channel_id = config_manager['job_notification_channel_id']

    def test_queue_job_consumers(self):
        from foundations.utils import byte_string
        from foundations_contrib.models.project_listing import ProjectListing
        from foundations_contrib.producers.jobs.queue_job import QueueJob
        from time import time
        import json
        import pickle

        def callback(random_input_data):
            pass

        stage = self._pipeline.stage(callback, 37)

        expected_job_parameters = {'random_job_data': self._str_random_uuid()}
        expected_argument = {'name': 'random_input_data',
                             'value': {'type': 'constant', 'value': 37}}
        expected_input_parameters = [
            {'argument': expected_argument, 'stage_uuid': stage.uuid()}
        ]
        self._pipeline_context.provenance.job_run_data = expected_job_parameters
    
        QueueJob(self._message_router, self._pipeline_context).push_message()
        current_time = time()

        parameter_key = 'projects:{}:job_parameter_names'.format(
            self._project_name)
        job_parameter_names = self._redis.smembers(parameter_key)
        self.assertEqual(set([b'random_job_data']), job_parameter_names)
        
        input_parameter_key = self._input_parameter_key(self._project_name)
        input_parameter_names = self._redis.smembers(input_parameter_key)
        self.assertEqual(set([b'random_input_data']), input_parameter_names)
        
        stage_time_key = self._stage_time(self._project_name)
        stage_time = self._redis.zrange(stage_time_key, 0, -1)
        self.assertEqual(b'21aad1de62dcd003b4d28909bd2add8431fceec7', stage_time[0])
        
        queued_job_key = 'project:{}:jobs:queued'.format(self._project_name)
        queued_jobs = self._redis.smembers(queued_job_key)
        self.assertEqual(set([byte_string(self._job_id)]), queued_jobs)

        global_queued_job_key = 'projects:global:jobs:queued'.format(self._project_name)
        global_queued_jobs = self._redis.smembers(global_queued_job_key)
        self.assertEqual(set([byte_string(self._job_id)]), global_queued_jobs)

        job_parameters_key = 'jobs:{}:parameters'.format(self._job_id)
        job_parameters = self._get_and_deserialize(job_parameters_key)
        self.assertEqual(expected_job_parameters, job_parameters)

        job_state_key = 'jobs:{}:state'.format(self._job_id)
        state = self._redis.get(job_state_key)
        self.assertEqual(b'queued', state)

        job_project_key = 'jobs:{}:project'.format(self._job_id)
        job_project_name = self._redis.get(job_project_key)
        self.assertEqual(byte_string(self._project_name), job_project_name)

        tracked_projects = ProjectListing.list_projects(self._redis)
        project_listing = tracked_projects[0]
        self.assertEqual(self._project_name, project_listing['name'])
        self.assertTrue(current_time - project_listing['created_at'] < 0.5)

        job_user_key = 'jobs:{}:user'.format(self._job_id)
        job_user = self._redis.get(job_user_key)
        self.assertEqual(byte_string(self._user), job_user)

        creation_time_key = 'jobs:{}:creation_time'.format(self._job_id)
        string_creation_time = self._redis.get(creation_time_key)
        creation_time = float(string_creation_time.decode())
        self.assertTrue(current_time - creation_time < 0.5)

        input_parameters_key = 'jobs:{}:input_parameters'.format(self._job_id)
        input_parameters = self._get_and_deserialize(input_parameters_key)
        self.assertEqual(expected_input_parameters, input_parameters)

        notification = self._slack_message_for_job()
        self.assertIsNotNone(notification)
        self.assertIn('Queued', notification)

    def _input_parameter_key(self, project_name):
        return 'projects:{}:input_parameter_names'.format(project_name)
    
    def _stage_time(self, project_name):
        return 'projects:{}:stage_time'.format(project_name)

    def test_running_job_consumers(self):
        from foundations.global_state import message_router
        from foundations.utils import byte_string
        from foundations_contrib.producers.jobs.run_job import RunJob
        from time import time

        queued_job_key = 'project:{}:jobs:queued'.format(self._project_name)
        self._redis.sadd(queued_job_key, self._job_id)

        global_queued_job_key = 'projects:global:jobs:queued'
        self._redis.sadd(global_queued_job_key, self._job_id)

        current_time = time()
        RunJob(self._message_router, self._pipeline_context).push_message()

        queued_jobs = self._redis.smembers(queued_job_key)
        self.assertEqual(set(), queued_jobs)

        global_queued_jobs = self._redis.smembers(global_queued_job_key)
        self.assertEqual(set(), global_queued_jobs)

        running_jobs_key = 'project:{}:jobs:running'.format(self._project_name)
        running_and_completed_jobs = self._redis.smembers(running_jobs_key)
        expected_jobs = set([byte_string(self._job_id)])
        self.assertEqual(expected_jobs, running_and_completed_jobs)

        job_state_key = 'jobs:{}:state'.format(self._job_id)
        state = self._redis.get(job_state_key)
        self.assertEqual(b'running', state)

        start_time_key = 'jobs:{}:start_time'.format(self._job_id)
        string_start_time = self._redis.get(start_time_key)
        start_time = float(string_start_time.decode())
        self.assertTrue(current_time - start_time < 0.1)

        notification = self._slack_message_for_job()
        self.assertIsNotNone(notification)
        self.assertIn('Running', notification)

    def test_completed_job_consumers(self):
        from foundations.global_state import message_router
        from foundations.utils import byte_string
        from time import time

        project_name = self._faker.name()

        message = {
            'job_id': self._job_id,
            'project_name': project_name
        }
        message_router.push_message('complete_job', message)
        current_time = time()

        state = self._redis.get('jobs:{}:state'.format(self._job_id))
        self.assertEqual(b'completed', state)

        completed_time_key = 'jobs:{}:completed_time'.format(self._job_id)
        string_completed_time = self._redis.get(completed_time_key)
        completed_time = float(string_completed_time.decode())
        self.assertTrue(current_time - completed_time < 0.5)

        notification = self._slack_message_for_job()
        self.assertIsNotNone(notification)
        self.assertIn('Completed', notification)

        completed_jobs_key = 'projects:global:jobs:completed'
        running_and_completed_jobs = self._redis.smembers(completed_jobs_key)
        expected_jobs = set([byte_string(self._job_id)])
        self.assertEqual(expected_jobs, running_and_completed_jobs)

    def test_failed_job_consumers(self):
        from foundations.global_state import message_router
        from time import time

        project_name = self._faker.name()
        expected_input_parameters = {'broken_data': self._random_name()}

        message = {
            'job_id': self._job_id,
            'error_information': expected_input_parameters,
            'project_name': project_name
        }
        message_router.push_message('fail_job', message)
        current_time = time()

        state = self._redis.get('jobs:{}:state'.format(self._job_id))
        self.assertEqual(b'failed', state)

        error_information_key = 'jobs:{}:error_information'.format(self._job_id)
        state = self._get_and_deserialize(error_information_key)
        self.assertEqual(expected_input_parameters, state)

        completed_time_key = 'jobs:{}:completed_time'.format(self._job_id)
        string_completed_time = self._redis.get(completed_time_key)
        completed_time = float(string_completed_time.decode())
        self.assertTrue(current_time - completed_time < 0.5)

        notification = self._slack_message_for_job()
        self.assertIsNotNone(notification)
        self.assertIn('Failed', notification)

    def test_job_metric_consumers(self):
        from foundations.global_state import message_router
        from foundations_internal.fast_serializer import deserialize
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

        job_metrics_key = 'jobs:{}:metrics'.format(job_id)
        job_metrics = self._redis.lrange(job_metrics_key, 0, -1)
        job_metrics = [deserialize(data) for data in job_metrics]
        first_job_metric = list(job_metrics)[0]

        self.assertTrue(current_time - first_job_metric[0] < 0.5)
        self.assertEqual(key, first_job_metric[1])
        self.assertEqual(value, first_job_metric[2])

        project_metrics_key = 'project:{}:metrics'.format(project_name)
        project_metric_name = self._redis.smembers(project_metrics_key)
        self.assertEqual(project_metric_name, set([byte_string(key)]))

    def _get_and_deserialize(self, key):
        from foundations_internal.foundations_serializer import deserialize

        serialized_data = self._redis.get(key)
        return deserialize(serialized_data)

    def _random_name(self):
        return self._faker.name()

    def _str_random_uuid(self):
        import uuid
        return str(uuid.uuid4())

    def _slack_message_for_job(self):
        import time

        notification_messages = self._slack_client.api_call('conversations.history', channel=self._testing_channel_id, limit=20)['messages']
        notification_messages = [message['text'] for message in notification_messages]
        for message in notification_messages:
            if self._job_id in message:
                return message
        return None