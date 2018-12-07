"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest, fakeredis, json
from mock import Mock

from foundations_contrib.format_input_parameters import FormatInputParameters

class TestFormatInputParameters(unittest.TestCase):
    
    def setUp(self):
        self._redis = fakeredis.FakeStrictRedis()
        self._redis.flushdb()
    
    def _load_input_parameter_name_data(self, project_name, data):
        self._redis.sadd('projects:{}:input_parameter_names'.format(project_name), data)
    
    # def test_fetch_input_parameter_name_data_from_redis(self):
    #     project_name = 'apple'
    #     redis_mock = Mock()
    #     input_param = [{'argument':{'name': 'ab', 'value': 'hi'}, 'stage_uuid': 'asdf'}]
    #     FormatInputParameters(project_name, input_param, Mock).format_input_parameters()
    #     redis_mock.assert_called_with('projects:apple:input_parameter_names')
    
    def test_get_stage_rank(self):
        project_name = 'apple'
        data = json.dumps({'parameter_name': 'something', 'stage_uuid': 'asdf', 'time': 1234})
        self._load_input_parameter_name_data(project_name, data)
        input_param = [{'argument':{'name': 'ab', 'value': 'hi'}, 'stage_uuid': 'asdf'}]
        expected = {'asdf': 0}
        result = FormatInputParameters(project_name, input_param, self._redis)._get_stage_rank()
        self.assertEqual(expected, result)
    
    def test_format_input_parameters_one_constant_parameter(self):
        project_name = 'banana'
        stage_uuid = 'gorilla'
        data = json.dumps({'parameter_name': 'something', 'stage_uuid': stage_uuid, 'time': 1234})
        self._load_input_parameter_name_data(project_name, data)
        input_param = [{'argument':{'name': 'ab', 'value': {'value':'hi', 'type': 'constant'}}, 'stage_uuid': stage_uuid}]
        expected = [{'name': 'ab-0',
                    'value': 'hi',
                    'type': 'string',
                    'source': 'constant'}]
        result = FormatInputParameters(project_name, input_param, self._redis).format_input_parameters()
        self.assertDictEqual(expected[0], result[0])

