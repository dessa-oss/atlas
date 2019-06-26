"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from foundations_contrib.log_manager import LogManager


class TestLogManager(unittest.TestCase):

    def setUp(self):
        from foundations.config_manager import ConfigManager
        self.config_manager = ConfigManager()
        
  
    def test_logger_return_logging_type(self):
        import logging
        
        log_manager = LogManager(self.config_manager)
        result_logger = log_manager.get_logger('namespaced_log_levels')
        self.assertTrue(isinstance(result_logger, logging.Logger))
    

    def test_logger_returns_log_level_info(self):
        import logging

        log_manager = LogManager(self.config_manager)
        result_logger = log_manager.get_logger('namespaced_log_levels')
        self.assertEqual(logging.INFO, result_logger.level)
    

    def test_logger_return_log_level_override(self):
        import logging

        self.config_manager['log_level'] = 'DEBUG'
        log_manager = LogManager(self.config_manager)
        result_logger = log_manager.get_logger('namespaced_log_levels')
        self.assertEqual(logging.DEBUG, result_logger.level)

    def test_logger_return_namespace_override(self):
        import logging

        self.config_manager['namespaced_log_levels'] = {'a': 'DEBUG'}
        log_manager = LogManager(self.config_manager)
        result_logger = log_manager.get_logger('a')
        self.assertEqual(logging.DEBUG, result_logger.level)

    def test_logger_return_namespace_override_does_not_match(self):
        import logging

        self.config_manager['namespaced_log_levels'] = {'a': 'DEBUG'}
        log_manager = LogManager(self.config_manager)
        result_logger = log_manager.get_logger('b')
        self.assertEqual(logging.INFO, result_logger.level)

    def test_logger_return_namespace_override_matches_with_longer_value(self):
        import logging

        self.config_manager['namespaced_log_levels'] = {'foundations': 'DEBUG'}
        log_manager = LogManager(self.config_manager)
        result_logger = log_manager.get_logger('foundations.config_manager')
        self.assertEqual(logging.DEBUG, result_logger.level)
    
    def test_logger_return_namespace_override_matches_with_longest_match(self):
        import logging

        self.config_manager['namespaced_log_levels'] = {'foundations': 'DEBUG', 'foundations.config_manager': 'ERROR'}
        log_manager = LogManager(self.config_manager)
        result_logger = log_manager.get_logger('foundations.config_manager')
        self.assertEqual(logging.ERROR, result_logger.level)

    def test_logger_return_when_clears_default_handlers(self):
        import logging

        log_manager = LogManager(self.config_manager)
        log_manager.get_logger('foundations.config_manager')
        root_logger = logging.getLogger()
        self.assertEqual(1, len(root_logger.handlers))

    def test_log_handler_return_format(self):
        import logging

        log_manager = LogManager(self.config_manager)
        log_manager.get_logger('foundations.config_manager')
        root_logger = logging.getLogger()
        log_handler = root_logger.handlers[0]
        formatter = log_handler.formatter
        self.assertEqual('%(asctime)s - %(name)s - %(levelname)s - %(message)s', formatter._fmt)

    def test_log_handler_return_stdout(self):
        import logging
        from sys import stdout

        log_manager = LogManager(self.config_manager)
        log_manager.get_logger('foundations.config_manager')
        root_logger = logging.getLogger()
        log_handler = root_logger.handlers[0]
        self.assertEqual(stdout, log_handler.stream)

    def test_logger_return_cached_logger(self):
        import logging
        
        log_manager = LogManager(self.config_manager)
        first_logger = log_manager.get_logger('namespaced_log_levels')
        second_logger = log_manager.get_logger('namespaced_log_levels')
        self.assertEqual(id(first_logger), id(second_logger))
    
    def test_logger_return_different_loggers(self):
        import logging
        
        log_manager = LogManager(self.config_manager)
        first_logger = log_manager.get_logger('namespaced_log_levels')
        second_logger = log_manager.get_logger('namespaced_log_levels_two')
        self.assertNotEqual(first_logger, second_logger)

    def test_foundations_not_running_warning_printed_false_by_default(self):
        log_manager = LogManager(self.config_manager)
        self.assertFalse(log_manager.foundations_not_running_warning_printed())

    def test_foundations_not_running_warning_printed_true_after_flag_set(self):
        log_manager = LogManager(self.config_manager)
        log_manager.set_foundations_not_running_warning_printed()
        self.assertTrue(log_manager.foundations_not_running_warning_printed())

    def test_foundations_not_running_warning_printed_false_after_flag_reset(self):
        log_manager = LogManager(self.config_manager)
        log_manager.set_foundations_not_running_warning_printed()
        log_manager.set_foundations_not_running_warning_printed(False)
        self.assertFalse(log_manager.foundations_not_running_warning_printed())