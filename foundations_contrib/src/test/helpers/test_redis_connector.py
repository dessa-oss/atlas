"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock


class TestRedisConnector(unittest.TestCase):

    def setUp(self):
        from foundations_contrib.helpers.redis_connector import RedisConnector
        from foundations.config_manager import ConfigManager

        self._config_manager = ConfigManager()
        self._connection_callback = Mock()
        self._connection = Mock()
        self._connection_callback.return_value = self._connection
        self._connector = RedisConnector(
            self._config_manager, self._connection_callback)

    def test_call_calls_callback_with_connection_string_missing(self):
        self._connector()
        self._connection_callback.assert_called_once_with(
            'redis://localhost:6379')

    def test_call_returns_result_of_callback(self):
        result = self._connector()
        self.assertEqual(self._connection, result)

    def test_call_calls_callback_with_connection_string(self):
        self._config_manager['redis_url'] = 'redis://lou:7733'
        self._connector()
        self._connection_callback.assert_called_once_with('redis://lou:7733')

    def test_call_calls_callback_with_connection_string_different_connection(self):
        self._config_manager['redis_url'] = 'redis://feifei:9733'
        self._connector()
        self._connection_callback.assert_called_once_with(
            'redis://feifei:9733')

    def test_call_returns_result_of_callback_with_connection_string(self):
        self._config_manager['redis_url'] = 'redis://feifei:9733'
        result = self._connector()
        self.assertEqual(self._connection, result)
