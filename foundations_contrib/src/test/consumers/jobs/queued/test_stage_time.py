"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest, json
from mock import Mock, patch, call

from foundations_contrib.consumers.jobs.queued.stage_time import StageTime


class TestStageTime(unittest.TestCase):

    def setUp(self):
        self._redis = Mock()
        self._consumer = StageTime(self._redis)

    def test_call_saved_run_data_keys(self):
        stage_uuids = ['stage_1']
        self._consumer.call({'project_name': 'here be dragons',
                             'input_parameters': {}, 'stage_uuids': stage_uuids}, None, None)
        self._redis.execute_command.assert_called_with('ZADD', 'projects:here be dragons:stage_time', 'NX', None, 'stage_1')

    def test_call_saved_run_data_keys_different_keys(self):
        stage_uuids = ['pineapple']
        self._consumer.call({'project_name': 'here be dragons',
                             'input_parameters': {}, 'stage_uuids': stage_uuids}, 123, None)
        self._redis.execute_command.assert_called_with('ZADD', 'projects:here be dragons:stage_time', 'NX', 123, 'pineapple')

    def test_call_saved_run_data_keys_multiple_keys(self):
        stage_uuids = ['pineapple', 'passionfruit']
        self._consumer.call({'project_name': 'here be dragons',
                             'input_parameters': {}, 'stage_uuids': stage_uuids}, 123, None)
        call_1 = call('ZADD', 'projects:here be dragons:stage_time', 'NX', 123, 'pineapple')
        call_2 = call('ZADD', 'projects:here be dragons:stage_time', 'NX', 123, 'passionfruit')
        self._redis.execute_command.assert_has_calls([call_1, call_2])

    def test_call_saved_run_data_keys_different_project_name(self):
        stage_uuids = ['grapes']
        self._consumer.call({'project_name': 'here be sheep',
                             'input_parameters': {}, 'stage_uuids': stage_uuids}, 777, None)
        self._redis.execute_command.assert_called_with('ZADD', 'projects:here be sheep:stage_time', 'NX', 777, 'grapes')