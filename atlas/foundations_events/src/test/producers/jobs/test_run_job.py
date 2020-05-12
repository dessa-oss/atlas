
import unittest
from mock import Mock

from foundations_events.producers.jobs.run_job import RunJob


class TestProducerRunJob(unittest.TestCase):

    def setUp(self):
        from foundations_internal.foundations_context import FoundationsContext

        self.route_name = None
        self.message = None

        self._foundations_context = FoundationsContext()
        self._foundations_context.job_id = 'some_project'
        self._router = Mock()
        self._router.push_message.side_effect = self._push_message
        self._producer = RunJob(self._router, self._foundations_context)

    def test_push_message_sends_run_job_message_to_correct_channel(self):
        self._producer.push_message()
        self.assertEqual('run_job', self.route_name)

    def test_push_message_sends_run_job_message_with_job_id(self):
        self._foundations_context.job_id = 'my fantastic job'
        self._foundations_context.project_name = 'this project'
        self._producer.push_message()
        self.assertEqual({'job_id': 'my fantastic job',
                          'project_name': 'this project',
                          'monitor_name': 'None'}, self.message)

    def test_push_message_sends_run_job_message_with_job_id_different_job_different_project(self):
        self._foundations_context.job_id = 'neural nets in space!'
        self._foundations_context.project_name = 'that project'
        self._producer.push_message()
        self.assertEqual({'job_id': 'neural nets in space!',
                          'project_name': 'that project',
                          'monitor_name': 'None'}, self.message)

    def _push_message(self, route_name, message):
        self.route_name = route_name
        self.message = message
