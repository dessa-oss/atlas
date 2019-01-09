"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
import fakeredis
import json
from mock import MagicMock

from foundations_contrib.input_parameter_formatter import InputParameterFormatter


class TestInputParameterFormatter(unittest.TestCase):

    def test_format_input_parameters_one_constant_parameter(self):
        stage_uuid = 'gorilla'
        stage_rank = {'gorilla': 1}
        input_param = [{'argument': {'name': 'owl', 'value': {
            'value': 'red', 'type': 'constant'}}, 'stage_uuid': stage_uuid}]
        job_param = {}
        expected = [{'name': 'owl-1',
                     'value': 'red',
                     'type': 'string',
                     'source': 'constant'}]
        result = InputParameterFormatter(
            input_param, job_param,  stage_rank).format_input_parameters()
        self.assertDictEqual(expected[0], result[0])

    def test_format_input_parameters_one_constant_parameter_different_type(self):
        stage_uuid = 'gorilla'
        stage_rank = {'gorilla': 1}
        input_param = [{'argument': {'name': 'ab', 'value': {
            'value': 123, 'type': 'constant'}}, 'stage_uuid': stage_uuid}]
        job_param = {}
        expected = [{'name': 'ab-1',
                     'value': 123,
                     'type': 'number',
                     'source': 'constant'}]
        result = InputParameterFormatter(
            input_param, job_param,  stage_rank).format_input_parameters()
        self.assertDictEqual(expected[0], result[0])

    def test_format_input_parameters_one_dynamic_parameter(self):
        stage_uuid = 'gorilla'
        stage_rank = {'gorilla': 1}
        input_param = [{'argument': {'name': 'ab', 'value': {
            'name': 'hi', 'type': 'dynamic'}}, 'stage_uuid': stage_uuid}]
        job_param = {'hi': 'bye'}
        expected = [{'name': 'ab-1',
                     'value': 'bye',
                     'type': 'string',
                     'source': 'placeholder'}]
        result = InputParameterFormatter(
            input_param, job_param, stage_rank).format_input_parameters()
        self.assertDictEqual(expected[0], result[0])

    def test_format_input_parameters_one_stage_parameter(self):
        stage_uuid = 'gorilla'
        stage_rank = {'gorilla': 1}
        input_param = [{'argument': {'name': 'ab', 'value': {
            'stage_name': 'hi', 'type': 'stage', 'stage_uuid': stage_uuid}}, 'stage_uuid': stage_uuid}]
        expected = [{'name': 'ab-1',
                     'value': 'hi-1',
                     'type': 'string',
                     'source': 'stage'}]
        result = InputParameterFormatter(
            input_param, {},  stage_rank).format_input_parameters()
        self.assertDictEqual(expected[0], result[0])

    def test_format_input_parameters_two_stages(self):
        stage_uuid_1 = 'gorilla'
        stage_uuid_2 = 'ape'
        stage_rank = {stage_uuid_2: 1, stage_uuid_1: 2}

        input_param = [{'argument': {'name': 'ab', 'value': {'value': 'hi', 'type': 'constant'}}, 'stage_uuid': stage_uuid_1},
                       {'argument': {'name': 'ab', 'value': {'value': 'bye', 'type': 'constant'}}, 'stage_uuid': stage_uuid_2}]
        expected = [{'name': 'ab-2',
                     'value': 'hi',
                     'type': 'string',
                     'source': 'constant'},
                    {'name': 'ab-1',
                     'value': 'bye',
                     'type': 'string',
                     'source': 'constant'},
                    ]
        result = InputParameterFormatter(
            input_param, {}, stage_rank).format_input_parameters()
        self.assertListEqual(expected, result)

    def test_format_input_parameter_adds_stages_when_stage_time_empty(self):
        stage_uuid_1 = 'gorilla'
        stage_uuid_2 = 'ape'

        input_param = [{'argument': {'name': 'ab', 'value': {
            'value': 'hi', 'type': 'constant'}}, 'stage_uuid': stage_uuid_1}]
        expected = [{'name': 'ab-1',
                     'value': 'hi',
                     'type': 'string',
                     'source': 'constant'}
                    ]
        result = InputParameterFormatter(
            input_param, {}, {}).format_input_parameters()
        self.assertListEqual(expected, result)

    def test_format_input_parameter_adds_stages_when_stage_time_empty_but_stage_time(self):
        stage_uuid_1 = 'gorilla'
        stage_uuid_2 = 'ape'
        stage_rank = {stage_uuid_1: 1}

        input_param = [{'argument': {'name': 'ab', 'value': {
            'value': 'hi', 'type': 'constant'}}, 'stage_uuid': stage_uuid_2}]
        expected = [{'name': 'ab-2',
                     'value': 'hi',
                     'type': 'string',
                     'source': 'constant'}
                    ]
        result = InputParameterFormatter(
            input_param, {}, stage_rank).format_input_parameters()
        self.assertListEqual(expected, result)

    def test_format_input_parameter_adds_stages_when_one_empty_argument_one_stage_time_argument(self):
        stage_uuid_1 = 'gorilla'
        stage_uuid_2 = 'ape'

        stage_rank = {stage_uuid_1: 1}

        input_param = [{'argument': {'name': 'ab', 'value': {'value': 'hi', 'type': 'constant'}}, 'stage_uuid': stage_uuid_1},
                       {'argument': {'name': 'ab', 'value': {'value': 'bye', 'type': 'constant'}}, 'stage_uuid': stage_uuid_2}]
        expected = [{'name': 'ab-1',
                     'value': 'hi',
                     'type': 'string',
                     'source': 'constant'},
                    {'name': 'ab-2',
                     'value': 'bye',
                     'type': 'string',
                     'source': 'constant'},
                    ]
        result = InputParameterFormatter(
            input_param, {}, stage_rank).format_input_parameters()
        self.assertListEqual(expected, result)

    def test_format_input_parameters_one_unknown_type(self):
        stage_uuid = 'gorilla'
        stage_rank = {'gorilla': 1}
        input_param = [{'argument': {'name': 'ab', 'value': {
            'value': {}, 'type': 'constant'}}, 'stage_uuid': stage_uuid}]
        expected = [{'name': 'ab-1',
                     'value': 'dict',
                     'type': 'string',
                     'source': 'constant'}]
        result = InputParameterFormatter(
            input_param, {},  stage_rank).format_input_parameters()
        self.assertDictEqual(expected[0], result[0])

    def test_format_input_parameters_one_unknown_type_different_type(self):
        stage_uuid = 'gorilla'
        stage_rank = {'gorilla': 1}
        input_param = [{'argument': {'name': 'ab', 'value': {
            'value': [{}], 'type': 'constant'}}, 'stage_uuid': stage_uuid}]
        expected = [{'name': 'ab-1',
                     'value': 'list',
                     'type': 'string',
                     'source': 'constant'}]
        result = InputParameterFormatter(
            input_param, {},  stage_rank).format_input_parameters()
        self.assertListEqual(expected, result)

    def test_format_input_parameters_input_parameter_array(self):
        stage_uuid = 'gorilla'
        stage_rank = {'gorilla': 1}
        input_param = [{'argument': {'name': 'ab', 'value': {
            'value': ['some_data'], 'type': 'constant'}}, 'stage_uuid': stage_uuid}]
        expected = [{'name': 'ab-1',
                     'value': ['some_data'],
                     'type': 'array string',
                     'source': 'constant'}]
        result = InputParameterFormatter(
            input_param, {},  stage_rank).format_input_parameters()
        self.assertListEqual(expected, result)

    def test_format_input_parameters_input_parameter_array_number(self):
        stage_uuid = 'gorilla'
        stage_rank = {'gorilla': 1}
        input_param = [{'argument': {'name': 'ab', 'value': {
            'value': [5], 'type': 'constant'}}, 'stage_uuid': stage_uuid}]
        expected = [{'name': 'ab-1',
                     'value': [5],
                     'type': 'array number',
                     'source': 'constant'}]
        result = InputParameterFormatter(
            input_param, {},  stage_rank).format_input_parameters()
        self.assertListEqual(expected, result)

    def test_format_input_parameters_input_parameter_array_bool(self):
        stage_uuid = 'gorilla'
        stage_rank = {'gorilla': 1}
        input_param = [{'argument': {'name': 'ab', 'value': {
            'value': True, 'type': 'constant'}}, 'stage_uuid': stage_uuid}]
        expected = [{'name': 'ab-1',
                     'value': True,
                     'type': 'bool',
                     'source': 'constant'}]
        result = InputParameterFormatter(
            input_param, {},  stage_rank).format_input_parameters()
        self.assertListEqual(expected, result)

    def test_format_input_parameters_two_stages_filter_split_at_stage(self):
        stage_uuid_1 = 'gorilla'
        stage_uuid_2 = 'ape'
        data_1 = json.dumps({'stage_uuid': stage_uuid_1, 'time': 1234})
        data_2 = json.dumps({'stage_uuid': stage_uuid_2, 'time': 1300})
        data_2_5 = json.dumps(
            {'parameter_name': 'blah', 'stage_uuid': stage_uuid_2, 'time': 1200})
        stage_rank = {'gorilla': 1, 'ape': 2}
        input_param = [
            {
                'argument': {
                    'name': 'ab',
                    'value': {
                        'value': 'split_at-1',
                        'type': 'constant'
                    }
                },
                'stage_uuid': stage_uuid_1
            },
            {
                'argument': {
                    'name': 'ab',
                    'value': {
                        'value': 'bye',
                        'type': 'constant'
                    }
                },
                'stage_uuid': stage_uuid_2
            }
        ]
        expected = [
            {
                'name': 'ab-2',
                'value': 'bye',
                'type': 'string',
                'source': 'constant'
            }
        ]

        result = InputParameterFormatter(
            input_param,
            {},
            stage_rank
        ).format_input_parameters()
        self.assertListEqual(expected, result)

    def test_format_input_parameters_list(self):
        stage_uuid = 'gorilla'
        stage_rank = {'gorilla': 1}
        input_param = [{'argument': {'name': 'owl', 'value': {
            'parameters': [{'type': 'constant', 'value': 'red'}], 'type': 'list'}}, 'stage_uuid': stage_uuid}]
        job_param = {}
        expected = [{'name': 'owl-1',
                     'value': ['red'],
                     'type': 'array string',
                     'source': 'list'}]
        result = InputParameterFormatter(
            input_param, job_param,  stage_rank).format_input_parameters()
        self.assertDictEqual(expected[0], result[0])

    def test_format_input_parameters_list_multiple_parameters(self):
        stage_uuid = 'gorilla'
        stage_rank = {'gorilla': 1}
        input_param = [
            {
                'argument': {
                    'name': 'owl',
                    'value': {
                        'parameters': [
                            {
                                'type': 'constant',
                                'value': 'red'
                            }, {
                                'stage_name': 'hi',
                                'type': 'stage',
                                'stage_uuid': stage_uuid
                            }
                        ],
                        'type': 'list'
                    }
                },
                'stage_uuid': stage_uuid
            }
        ]
        job_param = {}
        expected = [
            {
                'name': 'owl-1',
                'value': ['red', 'hi-1'],
                'type': 'array string',
                'source': 'list'
            }
        ]
        result = InputParameterFormatter(
            input_param, job_param,  stage_rank).format_input_parameters()
        self.assertDictEqual(expected[0], result[0])
