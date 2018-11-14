"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations.consumers.jobs.queued.run_data_keys import RunDataKeys

class TestRunDataKeys(unittest.TestCase):
    
    def setUp(self):
        self._redis = Mock()
        self._consumer = RunDataKeys(self._redis)

    def test_call_saved_run_data_keys(self):
        self._consumer.call({'project_name': 'here be dragons', 'job_parameters': {'number_of_neurons': 3434}}, None, None)
        self._redis.sadd.assert_called_with('projects:here be dragons:job_parameter_names', 'number_of_neurons')

    def test_call_saved_run_data_keys_different_keys(self):
        self._consumer.call({'project_name': 'here be dragons', 'job_parameters': {'hidden_layers': 7777}}, None, None)
        self._redis.sadd.assert_called_with('projects:here be dragons:job_parameter_names', 'hidden_layers')

    def test_call_saved_run_data_keys_multiple_keys(self):
        self._consumer.call({'project_name': 'here be dragons', 'job_parameters': {'shown_layers': 7777, 'neurons': 33}}, None, None)
        self._redis.sadd.assert_any_call('projects:here be dragons:job_parameter_names', 'shown_layers')
        self._redis.sadd.assert_any_call('projects:here be dragons:job_parameter_names', 'neurons')

    def test_call_saved_run_data_keys_different_project_name(self):
        self._consumer.call({'project_name': 'here be sheep', 'job_parameters': {'hidden_layers': 7777}}, None, None)
        self._redis.sadd.assert_called_with('projects:here be sheep:job_parameter_names', 'hidden_layers')