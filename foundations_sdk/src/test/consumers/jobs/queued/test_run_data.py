"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations.consumers.jobs.queued.run_data import RunData

class TestRunData(unittest.TestCase):

    
    
    def setUp(self):
        import json

        self._redis = Mock()
        self._serializer = Mock()
        self._serializer.dumps.side_effect = json.dumps
        self._consumer = RunData(self._redis, self._serializer)
 
    def test_call_saved_json_job_run_data(self):
        self._consumer.call({'job_id': 'my really big net', 'job_parameters': {'number_of_layers': 123}}, None, None)
        self._redis.set.assert_called_with('jobs:my really big net:parameters', '{"number_of_layers": 123}')

    def test_call_saved_json_job_run_data_different_job(self):
        self._consumer.call({'job_id': 'my really massive net', 'job_parameters': {'number_of_layers': 123}}, None, None)
        self._redis.set.assert_called_with('jobs:my really massive net:parameters', '{"number_of_layers": 123}')

    def test_call_saved_json_job_run_data_different_run_data(self):
        self._consumer.call({'job_id': 'my really massive net', 'job_parameters': {'neurons_per_layer': 99}}, None, None)
        self._redis.set.assert_called_with('jobs:my really massive net:parameters', '{"neurons_per_layer": 99}')

    def test_call_saved_json_job_run_data_different_serializer(self):
        import yaml

        self._serializer.dumps.side_effect = lambda value: yaml.dump(value, default_flow_style=False)
    
        self._consumer.call({'job_id': 'my really big net', 'job_parameters': {'number_of_layers': 123}}, None, None)
        self._redis.set.assert_called_with('jobs:my really big net:parameters', 'number_of_layers: 123\n')
