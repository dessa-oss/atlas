"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations.log_manager import LogManager


class TestLogManager(unittest.TestCase):
  
    def test_logger_with_empty_config(self):
        from foundations.config_manager import ConfigManager

        config_manager = ConfigManager()
        
        log_manager = LogManager(config_manager)
        self.assertEqual({}, config_manager.config())
    

    def test_logger_returns_string(self):
        
        from foundations.config_manager import ConfigManager

        config_manager = ConfigManager()
        config_manager.config()['foo'] = 'bar'
        log_manager = LogManager(config_manager)
        log_manager.get_logger('namespaced_log_levels')
        self.assertEqual({'foo': 'bar'}, config_manager.config())

    def test_logger_with_dictionary(self):
        
        from foundations.config_manager import ConfigManager

        config_manager = ConfigManager()
        log_manager = LogManager(config_manager)
        config_manager['namespaced_log_levels'] = { 'foundations_gcp.gcp_bucket': 'DEBUG' }
        log_manager.get_logger('namespaced_log_levels')
        self.assertEqual({'foundations_gcp.gcp_bucket': 'DEBUG'}, config_manager.config()['namespaced_log_levels'])