"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_contrib.log_manager import LogManager
import logging

class TestLogManager(Spec):

    @set_up
    def set_up(self):
        from foundations.config_manager import ConfigManager
        self.config_manager = ConfigManager()

    @let
    def log_manager(self):
        return LogManager(self.config_manager)
        
    @let
    def result_logger(self):
        return self.log_manager.get_logger('namespaced_log_levels')

    @let
    def root_logger(self):
        return logging.getLogger()

    @let
    def log_handler(self):
        return self.root_logger.handlers[0]
  
    def test_logger_return_logging_type(self):
        self.assertTrue(isinstance(self.result_logger, logging.Logger))

    def test_logger_returns_log_level_info(self):
        self.assertEqual(logging.INFO, self.result_logger.level)

    def test_logger_return_log_level_override(self):
        self.config_manager['log_level'] = 'DEBUG'
        self.assertEqual(logging.DEBUG, self.result_logger.level)

    def test_logger_return_namespace_override(self):
        self.config_manager['namespaced_log_levels'] = {'a': 'DEBUG'}
        result_logger = self.log_manager.get_logger('a')
        self.assertEqual(logging.DEBUG, result_logger.level)

    def test_logger_return_namespace_override_does_not_match(self):
        self.config_manager['namespaced_log_levels'] = {'a': 'DEBUG'}
        result_logger = self.log_manager.get_logger('b')
        self.assertEqual(logging.INFO, result_logger.level)

    def test_logger_return_namespace_override_matches_with_longer_value(self):
        self.config_manager['namespaced_log_levels'] = {'foundations': 'DEBUG'}
        result_logger = self.log_manager.get_logger('foundations.config_manager')
        self.assertEqual(logging.DEBUG, result_logger.level)
    
    def test_logger_return_namespace_override_matches_with_longest_match(self):
        self.config_manager['namespaced_log_levels'] = {'foundations': 'DEBUG', 'foundations.config_manager': 'ERROR'}
        result_logger = self.log_manager.get_logger('foundations.config_manager')
        self.assertEqual(logging.ERROR, result_logger.level)

    def test_logger_return_when_clears_default_handlers(self):
        self.log_manager.get_logger('foundations.config_manager')
        self.assertEqual(1, len(self.root_logger.handlers))

    def test_log_handler_return_format(self):
        self.log_manager.get_logger('foundations.config_manager')
        formatter = self.log_handler.formatter
        self.assertEqual('%(asctime)s - %(name)s - %(levelname)s - %(message)s', formatter._fmt)

    def test_log_handler_return_stdout(self):
        from sys import stdout

        self.log_manager.get_logger('foundations.config_manager')
        self.assertEqual(stdout, self.log_handler.stream)

    def test_logger_return_cached_logger(self):
        first_logger = self.log_manager.get_logger('namespaced_log_levels')
        second_logger = self.log_manager.get_logger('namespaced_log_levels')
        self.assertEqual(id(first_logger), id(second_logger))
    
    def test_logger_return_different_loggers(self):
        first_logger = self.log_manager.get_logger('namespaced_log_levels')
        second_logger = self.log_manager.get_logger('namespaced_log_levels_two')
        self.assertNotEqual(first_logger, second_logger)

    def test_foundations_not_running_warning_printed_false_by_default(self):
        self.assertFalse(self.log_manager.foundations_not_running_warning_printed())

    def test_foundations_not_running_warning_printed_true_after_flag_set(self):
        self.log_manager.set_foundations_not_running_warning_printed()
        self.assertTrue(self.log_manager.foundations_not_running_warning_printed())

    def test_foundations_not_running_warning_printed_false_after_flag_reset(self):
        self.log_manager.set_foundations_not_running_warning_printed()
        self.log_manager.set_foundations_not_running_warning_printed(False)
        self.assertFalse(self.log_manager.foundations_not_running_warning_printed())