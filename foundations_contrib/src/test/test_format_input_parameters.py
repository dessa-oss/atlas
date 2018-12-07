"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest, fakeredis, json
from mock import MagicMock

from foundations_contrib.format_input_parameters import FormatInputParameters

class TestFormatInputParameters(unittest.TestCase):
    
    def setUp(self):
        self._redis = fakeredis.FakeStrictRedis()
        self._redis.flushdb()
    
    def _load_input_parameter_name_data(self, project_name, data):
        self._redis.sadd('projects:{}:input_parameter_names'.format(project_name), data)

    def test_get_stage_rank(self):
        project_name = 'apple'
        data = json.dumps({'parameter_name': 'something', 'stage_uuid': 'asdf', 'time': 1234})
        self._load_input_parameter_name_data(project_name, data)
        input_param = [{'argument':{'name': 'ab', 'value': 'hi'}, 'stage_uuid': 'asdf'}]
        expected = {'asdf': 0}
        result = FormatInputParameters(project_name, input_param, {}, self._redis)._get_stage_rank()
        self.assertEqual(expected, result)
    
    def test_format_input_parameters_one_constant_parameter(self):
        project_name = 'banana'
        stage_uuid = 'gorilla'
        data = json.dumps({'parameter_name': 'something', 'stage_uuid': stage_uuid, 'time': 1234})
        self._load_input_parameter_name_data(project_name, data)
        input_param = [{'argument':{'name': 'owl', 'value': {'value':'red', 'type': 'constant'}}, 'stage_uuid': stage_uuid}]
        job_param = {}
        expected = [{'name': 'owl-0',
                    'value': 'red',
                    'type': 'string',
                    'source': 'constant'}]
        result = FormatInputParameters(project_name, input_param, job_param,  self._redis).format_input_parameters()
        self.assertDictEqual(expected[0], result[0])
    
    def test_format_input_parameters_one_constant_parameter_different_type(self):
        project_name = 'banana'
        stage_uuid = 'gorilla'
        data = json.dumps({'parameter_name': 'something', 'stage_uuid': stage_uuid, 'time': 1234})
        self._load_input_parameter_name_data(project_name, data)
        input_param = [{'argument':{'name': 'ab', 'value': {'value': 123, 'type': 'constant'}}, 'stage_uuid': stage_uuid}]
        job_param = {}
        expected = [{'name': 'ab-0',
                    'value': 123,
                    'type': 'number',
                    'source': 'constant'}]
        result = FormatInputParameters(project_name, input_param, job_param,  self._redis).format_input_parameters()
        self.assertDictEqual(expected[0], result[0])
    
    def test_format_input_parameters_one_dynamic_parameter(self):
        project_name = 'banana'
        stage_uuid = 'gorilla'
        data = json.dumps({'parameter_name': 'something', 'stage_uuid': stage_uuid, 'time': 1234})
        self._load_input_parameter_name_data(project_name, data)
        input_param = [{'argument':{'name': 'ab', 'value': {'name':'hi', 'type': 'dynamic'}}, 'stage_uuid': stage_uuid}]
        job_param = {'hi': 'bye'}
        expected = [{'name': 'ab-0',
                    'value': 'bye',
                    'type': 'string',
                    'source': 'placeholder'}]
        result = FormatInputParameters(project_name, input_param, job_param, self._redis).format_input_parameters()
        self.assertDictEqual(expected[0], result[0])

    def test_format_input_parameters_one_stage_parameter(self):
        project_name = 'banana'
        stage_uuid = 'gorilla'
        data = json.dumps({'parameter_name': 'something', 'stage_uuid': stage_uuid, 'time': 1234})
        self._load_input_parameter_name_data(project_name, data)
        input_param = [{'argument':{'name': 'ab', 'value': {'stage_name':'hi', 'type': 'stage', 'stage_uuid': stage_uuid}}, 'stage_uuid': stage_uuid}]
        expected = [{'name': 'ab-0',
                    'value': 'hi-0',
                    'type': 'string',
                    'source': 'stage'}]
        result = FormatInputParameters(project_name, input_param,{},  self._redis).format_input_parameters()
        self.assertDictEqual(expected[0], result[0])
    
    def test_format_input_parameters_two_stages(self):
        project_name = 'banana'
        stage_uuid_1 = 'gorilla'
        stage_uuid_2 = 'ape'
        data_1 = json.dumps({'parameter_name': 'something', 'stage_uuid': stage_uuid_1, 'time': 1234})
        data_2 = json.dumps({'parameter_name': 'something', 'stage_uuid': stage_uuid_2, 'time': 1300})
        data_2_5 = json.dumps({'parameter_name': 'blah', 'stage_uuid': stage_uuid_2, 'time': 1200})
        self._load_input_parameter_name_data(project_name, data_1)
        self._load_input_parameter_name_data(project_name, data_2)
        self._load_input_parameter_name_data(project_name, data_2_5)
        input_param = [{'argument':{'name': 'ab', 'value': {'value':'hi', 'type': 'constant'}}, 'stage_uuid': stage_uuid_1},
                        {'argument':{'name': 'ab', 'value': {'value':'bye', 'type': 'constant'}}, 'stage_uuid': stage_uuid_2}]
        expected = [{'name': 'ab-1',
                    'value': 'hi',
                    'type': 'string',
                    'source': 'constant'},
                    {'name': 'ab-0',
                    'value': 'bye',
                    'type': 'string',
                    'source': 'constant'},
                    ]
        result = FormatInputParameters(project_name, input_param, {}, self._redis).format_input_parameters()
        self.assertListEqual(expected, result)
    
    def test_format_input_parameters_two_stages_same_time(self):
        project_name = 'banana'
        stage_uuid_1 = 'gorilla'
        stage_uuid_2 = 'ape'
        data_1 = json.dumps({'parameter_name': 'something', 'stage_uuid': stage_uuid_1, 'time': 1200})
        data_2 = json.dumps({'parameter_name': 'something', 'stage_uuid': stage_uuid_2, 'time': 1300})
        data_2_5 = json.dumps({'parameter_name': 'blah', 'stage_uuid': stage_uuid_2, 'time': 1200})
        self._load_input_parameter_name_data(project_name, data_1)
        self._load_input_parameter_name_data(project_name, data_2)
        self._load_input_parameter_name_data(project_name, data_2_5)
        input_param = [{'argument':{'name': 'ab', 'value': {'value':'hi', 'type': 'constant'}}, 'stage_uuid': stage_uuid_1},
                        {'argument':{'name': 'ab', 'value': {'value':'bye', 'type': 'constant'}}, 'stage_uuid': stage_uuid_2}]
        expected = [{'name': 'ab-1',
                    'value': 'hi',
                    'type': 'string',
                    'source': 'constant'},
                    {'name': 'ab-0',
                    'value': 'bye',
                    'type': 'string',
                    'source': 'constant'},
                    ]
        result = FormatInputParameters(project_name, input_param, {}, self._redis).format_input_parameters()
        self.assertListEqual(expected, result)

