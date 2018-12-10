"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_contrib.consumers.jobs.queued.input_parameter_keys import InputParameterKeys


class TestInputParameterKeys(unittest.TestCase):

    def setUp(self):
        self._redis = Mock()
        self._consumer = InputParameterKeys(self._redis)

    def test_call_saved_run_data_keys(self):
        input_parameters = [{'argument': {
            'name': 'number_of_neurons', 'value': 3434}, 'stage_uuid': 'stage1'}]
        self._consumer.call({'project_name': 'here be dragons',
                             'input_parameters': input_parameters}, None, None)
        self._redis.sadd.assert_called_with(
            'projects:here be dragons:input_parameter_names', 'number_of_neurons')

    def test_call_saved_run_data_keys_different_keys(self):
        input_parameters = [
            {'argument': {'name': 'hidden_layers', 'value': 7777}, 'stage_uuid': 'stage1'}]
        self._consumer.call({'project_name': 'here be dragons',
                             'input_parameters': input_parameters}, None, None)
        self._redis.sadd.assert_called_with(
            'projects:here be dragons:input_parameter_names', 'hidden_layers')

    def test_call_saved_run_data_keys_multiple_keys(self):
        input_parameters = [
            {'argument': {'name': 'shown_layers', 'value': 7777},
                'stage_uuid': 'stage1'},
            {'argument': {'name': 'neurons', 'value': 33}, 'stage_uuid': 'stage1'},
        ]
        self._consumer.call({'project_name': 'here be dragons',
                             'input_parameters': input_parameters}, None, None)
        self._redis.sadd.assert_any_call(
            'projects:here be dragons:input_parameter_names', 'shown_layers')
        self._redis.sadd.assert_any_call(
            'projects:here be dragons:input_parameter_names', 'neurons')

    def test_call_saved_run_data_keys_different_project_name(self):
        input_parameters = [
            {'argument': {'name': 'hidden_layers', 'value': 7777}, 'stage_uuid': 'stage1'}]
        self._consumer.call({'project_name': 'here be sheep',
                             'input_parameters': input_parameters}, None, None)
        self._redis.sadd.assert_called_with('projects:here be sheep:input_parameter_names', 'hidden_layers')
