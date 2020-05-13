
import unittest
from mock import Mock

from foundations_events.producers.jobs.queue_job import QueueJob


class TestProducerQueueJob(unittest.TestCase):

    def setUp(self):
        from foundations_internal.foundations_job import FoundationsJob
        from faker import Faker

        self.route_name = None
        self.message = None

        self._foundations_context = FoundationsJob()
        self._foundations_context.job_id = 'some_project'
        self._router = Mock()
        self._router.push_message.side_effect = self._push_message
        self._producer = QueueJob(self._router, self._foundations_context)
        self._faker = Faker()

    def test_push_message_sends_queue_job_message_to_correct_channel(self):
        self._producer.push_message()
        self.assertEqual('queue_job', self.route_name)

    def test_push_message_sends_queue_job_message_with_job_id(self):
        job_id = self._make_string_uuid()
        self._foundations_context.job_id = job_id
        self._producer.push_message()
        self.assertEqual(job_id, self.message['job_id'])

    def test_push_message_send_queue_job_message_with_project_name(self):
        project_name = self._faker.name()
        self._foundations_context.project_name = project_name
        self._producer.push_message()
        self.assertEqual(project_name, self.message['project_name'])

    def test_push_message_send_queue_job_message_with_job_parameters(self):
        run_data = self._make_run_data()
        self._foundations_context.provenance.job_run_data = run_data
        self._producer.push_message()
        self.assertEqual(run_data, self.message['job_parameters'])

    def test_push_message_send_queue_job_message_with_user_name(self):
        user_name = self._faker.name()
        self._foundations_context.user_name = user_name
        self._producer.push_message()
        self.assertEqual(user_name, self.message['user_name'])

    def test_push_message_send_queue_job_message_with_annotations(self):
        annotations = self._faker.name()
        self._foundations_context.provenance.annotations = annotations
        self._producer.push_message()
        self.assertEqual(annotations, self.message['annotations'])

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
