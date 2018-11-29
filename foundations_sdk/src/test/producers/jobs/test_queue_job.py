"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations.producers.jobs.queue_job import QueueJob
from foundations.stage_hierarchy import StageHierarchyEntry


class TestProducerQueueJob(unittest.TestCase):

    def setUp(self):
        from foundations.pipeline_context import PipelineContext
        from faker import Faker

        self.route_name = None
        self.message = None

        self._pipeline_context = PipelineContext()
        self._router = Mock()
        self._router.push_message.side_effect = self._push_message
        self._producer = QueueJob(self._router, self._pipeline_context)
        self._faker = Faker()
        self._stage_hierarchy = self._pipeline_context.provenance.stage_hierarchy

    def test_push_message_sends_queue_job_message_to_correct_channel(self):
        self._producer.push_message()
        self.assertEqual('queue_job', self.route_name)

    def test_push_message_sends_queue_job_message_with_job_id(self):
        job_id = self._make_string_uuid()
        self._pipeline_context.file_name = job_id
        self._producer.push_message()
        self.assertEqual(job_id, self.message['job_id'])

    def test_push_message_send_queue_job_message_with_project_name(self):
        project_name = self._faker.name()
        self._pipeline_context.provenance.project_name = project_name
        self._producer.push_message()
        self.assertEqual(project_name, self.message['project_name'])

    def test_push_message_send_queue_job_message_with_job_parameters(self):
        run_data = self._make_run_data()
        self._pipeline_context.provenance.job_run_data = run_data
        self._producer.push_message()
        self.assertEqual(run_data, self.message['job_parameters'])

    def test_push_message_send_queue_job_message_with_user_name(self):
        user_name = self._faker.name()
        self._pipeline_context.provenance.user_name = user_name
        self._producer.push_message()
        self.assertEqual(user_name, self.message['user_name'])

    def test_push_message_send_queue_job_message_with_empty_stage_arg(self):
        stage_id = self._make_string_uuid()

        mock_entry = Mock()
        self._stage_hierarchy.entries = {stage_id: mock_entry}
        mock_entry.stage_args = []

        self._producer.push_message()
        self.assertEqual([], self.message['input_parameters'])

    def test_push_message_send_queue_job_message_with_numeric_arg(self):
        stage_id = self._make_string_uuid()
        argument = self._make_random_arg()

        mock_entry = Mock()
        self._stage_hierarchy.entries = {stage_id: mock_entry}
        mock_entry.stage_args = [argument]

        self._producer.push_message()
        expected_value = {'argument': argument, 'stage_uuid': stage_id}
        self.assertEqual([expected_value], self.message['input_parameters'])

    def test_push_message_send_queue_job_message_with_multiple_numeric_arg(self):
        stage_id = self._make_string_uuid()

        mock_entry = Mock()
        self._stage_hierarchy.entries = {stage_id: mock_entry}
        argument = self._make_random_arg()
        argument2 = self._make_random_arg()
        mock_entry.stage_args = [argument, argument2]

        self._producer.push_message()
        expected_value = {'argument': argument, 'stage_uuid': stage_id}
        expected_value2 = {'argument': argument2, 'stage_uuid': stage_id}
        self.assertEqual([expected_value, expected_value2],
                         self.message['input_parameters'])

    def _make_random_arg(self):
        import random
        return random.randint(1, 100)

    def _make_string_uuid(self):
        import uuid
        return str(uuid.uuid4())

    def _make_run_data(self):
        fake_dict = {}
        fake_value = self._faker.address()
        fake_key = self._faker.name()
        fake_dict[fake_key] = fake_value
        return fake_dict

    def _callback(self, initial):
        pass

    def _push_message(self, route_name, message):
        self.route_name = route_name
        self.message = message
