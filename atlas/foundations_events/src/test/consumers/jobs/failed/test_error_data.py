
import unittest
from mock import Mock

from foundations_events.consumers.jobs.failed.error_data import ErrorData


class TestErrorData(unittest.TestCase):

    def setUp(self):
        import json

        self._redis = Mock()
        self._serializer = Mock()
        self._serializer.dumps.side_effect = json.dumps
        self._consumer = ErrorData(self._redis, self._serializer)

    def test_call_saved_json_job_error_data(self):
        input_data = {'job_id': 'my really big net',
                      'error_information': {'exception_type': 'The really bad kind'}
                      }
        self._consumer.call(input_data, None, None)
        self._redis.set.assert_called_with('jobs:my really big net:error_information', '{"exception_type": "The really bad kind"}')

    def test_call_saved_json_job_error_data_different_job(self):
        input_data = {'job_id': 'my really massive net',
                      'error_information': {'exception_type': 'The really bad kind'}
                      }
        self._consumer.call(input_data, None, None)
        self._redis.set.assert_called_with('jobs:my really massive net:error_information', '{"exception_type": "The really bad kind"}')

    def test_call_saved_json_job_error_data_different_error_data(self):
        input_data = {'job_id': 'my really massive net',
                      'error_information': {'trace': 'A really long trace'}
                      }
        self._consumer.call(input_data, None, None)
        self._redis.set.assert_called_with('jobs:my really massive net:error_information', '{"trace": "A really long trace"}')

    def test_call_saved_json_job_error_data_different_serializer(self):
        import yaml

        self._serializer.dumps.side_effect = lambda value: yaml.dump(
            value, default_flow_style=False)

        input_data = {'job_id': 'my really big net',
                'error_information': {'exception_type': 'The really bad kind'}
                }

        self._consumer.call(input_data, None, None)
        self._redis.set.assert_called_with('jobs:my really big net:error_information', 'exception_type: The really bad kind\n')
