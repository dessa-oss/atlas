"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations.consumers.jobs.failed.error_data import ErrorData

class TestErrorData(unittest.TestCase):

    def setUp(self):
        import json

        self._redis = Mock()
        self._serializer = Mock()
        self._serializer.dumps.side_effect = json.dumps
        self._consumer = ErrorData(self._redis, self._serializer)
 
    def test_call_saved_json_job_error_data(self):
        self._consumer.call({'job_id': 'my really big net', 'error_information': {'exception_type': 'The really bad kind'}}, None, None)
        self._redis.set.assert_called_with('jobs:my really big net:error_information', '{"exception_type": "The really bad kind"}')

    def test_call_saved_json_job_error_data_different_job(self):
        self._consumer.call({'job_id': 'my really massive net', 'error_information': {'exception_type': 'The really bad kind'}}, None, None)
        self._redis.set.assert_called_with('jobs:my really massive net:error_information', '{"exception_type": "The really bad kind"}')

    def test_call_saved_json_job_error_data_different_error_data(self):
        self._consumer.call({'job_id': 'my really massive net', 'error_information': {'trace': 'A really long trace'}}, None, None)
        self._redis.set.assert_called_with('jobs:my really massive net:error_information', '{"trace": "A really long trace"}')

    def test_call_saved_json_job_error_data_different_serializer(self):
        import yaml

        self._serializer.dumps.side_effect = lambda value: yaml.dump(value, default_flow_style=False)
    
        self._consumer.call({'job_id': 'my really big net', 'error_information': {'exception_type': 'The really bad kind'}}, None, None)
        self._redis.set.assert_called_with('jobs:my really big net:error_information', 'exception_type: The really bad kind\n')
