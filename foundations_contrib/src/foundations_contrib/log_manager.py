"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import logging

class LogManager(object):

    def __init__(self, config):
        self._loggers = None
        self._config_manager = config
        self._foundations_not_running_warning_printed = False

    def get_logger(self, name):
        if self._loggers is None:
            self._load()

        if not name in self._loggers:
            self._add_logger(name)

        return self._loggers[name]

    def set_foundations_not_running_warning_printed(self, status=True):
        self._foundations_not_running_warning_printed = status

    def foundations_not_running_warning_printed(self):
        return self._foundations_not_running_warning_printed

    def _load(self):
        from sys import stdout
        
        logging.basicConfig(stream=stdout)
        logger = logging.getLogger()
        del logger.handlers[:]
        logger.addHandler(self._stdout_log_handler())

        self._loggers = {}

    def _stdout_log_handler(self):
        from sys import stdout

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_handler = logging.StreamHandler(stdout)
        log_handler.setFormatter(formatter)

        return log_handler

    def _add_logger(self, name):
        from logging import getLogger
        from logging import getLevelName

        new_logger = getLogger(name)
        log_level = self._find_log_level(name)
        if log_level is None:
            log_level = self._config_manager.config().get('log_level', 'INFO')
        
        new_logger.level = getLevelName(log_level)
        self._loggers[name] = new_logger

    def _find_log_level(self, name):

        longest_match = 0
        log_level = None
        log_levels = self._config_manager.config().get('namespaced_log_levels', {})
        for key, value in log_levels.items():
            if len(key) > longest_match and name.startswith(key):
                longest_match = len(key)
                log_level = value

        return log_level
