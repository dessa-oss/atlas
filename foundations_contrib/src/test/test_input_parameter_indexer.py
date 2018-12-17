"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest, fakeredis
from mock import Mock, patch, call

from foundations_contrib.input_parameter_indexer import InputParameterIndexer
from foundations_contrib.input_parameter_formatter import InputParameterFormatter

class TestInputParameterIndexer(unittest.TestCase):
    
    def setUp(self):
        from foundations.global_state import redis_connection
        self._redis = redis_connection

        
    def _zadd_to_redis(self, project_name, timestamp, key):
        self._redis.execute_command('ZADD', 'projects:{}:{}'.format(project_name, 'stage_time'), 'NX', timestamp, key)

    def _del_from_redis(self, project_name):
        self._redis.delete('projects:{}:stage_time'.format(project_name))


    @patch.object(InputParameterFormatter, 'format_input_parameters')
    @patch('foundations_contrib.input_parameter_formatter.InputParameterFormatter')
    def test_index_input_parameters_indexes_single_job_one_stage(self, mock_formatter, mock):
        project_name = 'noel'
        jobs_data = [{'input_params': {'name': 'hi'}, 'job_parameters': {}}]
        mock.return_value = {'name': 'hi-0'}
        self._zadd_to_redis(project_name, 1234, 'joyeux')

        InputParameterIndexer.index_input_parameters(project_name, jobs_data)
        
        mock_formatter.assert_called_with({'name': 'hi'}, {}, {b'joyeux': 0})
        self._del_from_redis(project_name)
    
    @patch.object(InputParameterFormatter, 'format_input_parameters')
    @patch('foundations_contrib.input_parameter_formatter.InputParameterFormatter')
    def test_index_input_parameters_indexes_single_job_multiple_stage(self, mock_formatter, mock):
        project_name = 'noel'
        jobs_data = [{'input_params': {'name': 'hi'}, 'job_parameters': {}}]
        mock.return_value = {'name': 'hi-0'}
        self._zadd_to_redis(project_name, 1234, 'joyeux')
        self._zadd_to_redis(project_name, 1304, 'happy')
        self._zadd_to_redis(project_name, 1534, 'merry')

        InputParameterIndexer.index_input_parameters(project_name, jobs_data)

        mock_formatter.assert_called_with({'name': 'hi'}, {}, {b'joyeux': 0, b'happy': 1, b'merry': 2})
        self._del_from_redis(project_name)
    
    @patch.object(InputParameterFormatter, 'format_input_parameters')
    @patch('foundations_contrib.input_parameter_formatter.InputParameterFormatter')
    def test_index_input_parameters_indexes_single_job_handles_duplicates(self, mock_formatter, mock):
        project_name = 'noel'
        jobs_data = [{'input_params': {'name': 'hi'}, 'job_parameters': {}}]
        mock.return_value = {'name': 'hi-0'}
        self._zadd_to_redis(project_name, 1234, 'joyeux')
        self._zadd_to_redis(project_name, 1500, 'joyeux')
        self._zadd_to_redis(project_name, 1534, 'merry')

        InputParameterIndexer.index_input_parameters(project_name, jobs_data)

        mock_formatter.assert_called_with({'name': 'hi'}, {}, {b'joyeux': 0, b'merry': 1})
        self._del_from_redis(project_name)
    
    @patch.object(InputParameterFormatter, 'format_input_parameters')
    @patch('foundations_contrib.input_parameter_formatter.InputParameterFormatter')
    def test_index_input_parameters_indexes_multiple_jobs(self, mock_formatter, mock):
        project_name = 'noel'
        jobs_data = [{'input_params': {'name': 'hi'}, 'job_parameters': {}},
                    {'input_params': {'name': 'bye'}, 'job_parameters': {}}]
        mock.return_value = {'name': 'hi-0'}
        self._zadd_to_redis(project_name, 1234, 'joyeux')

        InputParameterIndexer.index_input_parameters(project_name, jobs_data)

        call_1 = call({'name': 'hi'}, {}, {b'joyeux': 0})
        input_param_call = call().format_input_parameters()
        call_2 = call({'name': 'bye'}, {}, {b'joyeux': 0})
        mock_formatter.assert_has_calls([call_1, input_param_call, call_2, input_param_call])
        self._del_from_redis(project_name)