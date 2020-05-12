
import unittest
from mock import Mock

from foundations_events.producers.jobs.failed_job import FailedJob


class TestProducerFailedJob(unittest.TestCase):

    def setUp(self):
        from foundations_internal.foundations_context import FoundationsContext

        self.route_name = None
        self.message = None

        self._foundations_context = FoundationsContext()
        self._foundations_context.set_job_id('some_project')
        self._router = Mock()
        self._router.push_message.side_effect = self._push_message
        self._error_information = {'type': None,
                                   'exception': None, 'traceback': []}
        self._producer = FailedJob(
            self._router, self._foundations_context, self._error_information)

    def test_push_message_sends_fail_job_message_to_correct_channel(self):
        self._producer.push_message()
        self.assertEqual('fail_job', self.route_name)

    def test_push_message_sends_fail_job_message_with_job_id(self):
        self._foundations_context.set_job_id('my fantastic job')
        self._producer.push_message()
        self.assertEqual('my fantastic job', self.message['job_id'])

    def test_push_message_sends_fail_job_message_with_job_id_different_job(self):
        self._foundations_context.set_job_id('neural nets in space!')
        self._producer.push_message()
        self.assertEqual('neural nets in space!', self.message['job_id'])

    def test_push_message_sends_complete_job_message_with_project_name(self):
        self._foundations_context.set_project_name('my fantastic job')
        self._producer.push_message()
        self.assertDictContainsSubset({'project_name': 'my fantastic job'}, self.message)

    def test_push_message_sends_complete_job_message_with_project_name_different_job(self):
        self._foundations_context.set_project_name('neural nets in space!')
        self._producer.push_message()
        self.assertDictContainsSubset({'project_name': 'neural nets in space!'}, self.message)

    def test_push_message_sends_fail_job_message_with_error_information_error_type(self):
        self._error_information['type'] = 'Exception'
        self._producer.push_message()
        self.assertEqual(
            "'Exception'", self.message['error_information']['type'])

    def test_push_message_sends_fail_job_message_with_error_information_error_type_different_type(self):
        self._error_information['type'] = 'ValueError'
        self._producer.push_message()
        self.assertEqual(
            "'ValueError'", self.message['error_information']['type'])

    def test_push_message_sends_fail_job_message_with_error(self):
        self._error_information['exception'] = ValueError('it died')
        self._producer.push_message()
        self.assertEqual(
            'it died', self.message['error_information']['exception'])

    def test_push_message_sends_fail_job_message_with_error_different_error(self):
        self._error_information['exception'] = ValueError('it died again')
        self._producer.push_message()
        self.assertEqual(
            'it died again', self.message['error_information']['exception'])

    def test_push_message_sends_fail_job_message_with_traceback(self):
        frame = ('/path/to/file.py', 37, 'bad_function', None)

        self._error_information['traceback'] = [frame]
        self._producer.push_message()
        self.assertEqual(['  File "/path/to/file.py", line 37, in bad_function\n'],
                         self.message['error_information']['traceback'])

    def test_push_message_sends_fail_job_message_with_traceback_different_traceback(self):
        frame = ('/path/to/different/file.py', 71, 'really_bad_function', None)
        frame_two = ('/path/to/different/file_two.py', 711, 'it_borked', None)

        self._error_information['traceback'] = [frame, frame_two]
        self._producer.push_message()
        expected_traceback = [
            '  File "/path/to/different/file.py", line 71, in really_bad_function\n',
            '  File "/path/to/different/file_two.py", line 711, in it_borked\n'
        ]
        self.assertEqual(expected_traceback,
                         self.message['error_information']['traceback'])

    def _push_message(self, route_name, message):
        self.route_name = route_name
        self.message = message
