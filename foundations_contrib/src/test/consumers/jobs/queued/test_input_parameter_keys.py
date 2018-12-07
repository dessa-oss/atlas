"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest, json
from mock import Mock, patch, call

from foundations_contrib.consumers.jobs.queued.input_parameter_keys import InputParameterKeys


class TestInputParameterKeys(unittest.TestCase):

    def setUp(self):
        self._redis = Mock()
        self._consumer = InputParameterKeys(self._redis)

    @patch('time.time')
    def test_call_saved_run_data_keys(self, mock_time):
        mock_time.return_value = 123
        input_parameters = [{'argument': {'name': 'number_of_neurons', 'value': {'type': 'constant', 'value': 777}}, 'stage_uuid': 'stage1'}]
        self._consumer.call({'project_name': 'here be dragons',
                             'input_parameters': input_parameters}, None, None)
        expected_value = {'parameter_name': 'number_of_neurons',
                          'stage_uuid': 'stage1',
                          'time': 123}
        self._redis.sadd.assert_called_with('projects:here be dragons:input_parameter_names', json.dumps(expected_value))

    @patch('time.time')
    def test_call_saved_run_data_keys_different_keys(self, mock_time):
        mock_time.return_value = 123
        input_parameters = [
            {'argument': {'name': 'hidden_layers', 'value': {'type': 'constant', 'value': 777}}, 'stage_uuid': 'stage1'}]
        self._consumer.call({'project_name': 'here be dragons',
                             'input_parameters': input_parameters}, None, None)
        expected_value = {'parameter_name': 'hidden_layers',
                    'stage_uuid': 'stage1',
                    'time': 123}
        self._redis.sadd.assert_called_with(
            'projects:here be dragons:input_parameter_names', json.dumps(expected_value))

    @patch('time.time')
    def test_call_saved_run_data_keys_multiple_keys(self, mock_time):
        mock_time.return_value = 123
        input_parameters = [
            {'argument': {'name': 'shown_layers', 'value': {'type': 'constant', 'value': 777}},
                'stage_uuid': 'stage1'},
            {'argument': {'name': 'neurons', 'value': {'type': 'constant', 'value': 777}}, 'stage_uuid': 'stage1'},
        ]
        self._consumer.call({'project_name': 'here be dragons',
                             'input_parameters': input_parameters}, None, None)
        expected_value_1 = {'parameter_name': 'shown_layers',
            'stage_uuid': 'stage1',
            'time': 123}
        expected_value_2 = {'parameter_name': 'neurons',
            'stage_uuid': 'stage1',
            'time': 123}
        self._redis.sadd.assert_any_call(
            'projects:here be dragons:input_parameter_names', json.dumps(expected_value_1))
        self._redis.sadd.assert_any_call(
            'projects:here be dragons:input_parameter_names', json.dumps(expected_value_2))

    @patch('time.time')
    def test_call_saved_run_data_keys_different_project_name(self, mock_time):
        mock_time.return_value = 123
        input_parameters = [{'argument': {'name': 'hidden_layers', 'value': {'type': 'constant', 'value': 777}}, 'stage_uuid': 'stage1'}]
        self._consumer.call({'project_name': 'here be sheep',
                             'input_parameters': input_parameters}, None, None)
        expected_value_1 = {'parameter_name': 'hidden_layers',
            'stage_uuid': 'stage1',
            'time': 123}
        self._redis.sadd.assert_called_with(
            'projects:here be sheep:input_parameter_names', json.dumps(expected_value_1))
    
    @patch('time.time')
    def test_call_saved_run_data_stage_argument(self, mock_time):
        mock_time.return_value = 123
        input_parameters = [{'argument': {'name': 'hidden_layers', 'value': {'type': 'stage', 'stage_uuid': 'stage2'}}, 'stage_uuid': 'stage1'}]
        self._consumer.call({'project_name': 'here be sheep',
                             'input_parameters': input_parameters}, None, None)
        expected_value_1 = {'parameter_name': 'hidden_layers',
            'stage_uuid': 'stage1',
            'time': 123}
        expected_value_2 = {'parameter_name': 'no_param_stage',
            'stage_uuid': 'stage2',
            'time': 123}
        call_1 = call('projects:here be sheep:input_parameter_names', json.dumps(expected_value_1))
        call_2 = call('projects:here be sheep:input_parameter_names', json.dumps(expected_value_2))
        self._redis.sadd.assert_has_calls( [call_1, call_2], any_order = True)
