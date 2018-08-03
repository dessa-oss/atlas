"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class LogManager(object):

    def __init__(self):
        self._loggers = None

    def get_logger(self, name):
        if self._loggers is None:
            self._load()

        if not name in self._loggers:
            self._add_logger(name)

        return self._loggers[name]

    def _load(self):
        from foundations.global_state import config_manager
        import logging
        from sys import stdout

        log_level = config_manager.config().get('log_level', 'INFO')
        log_level = logging.getLevelName(log_level)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_handler = logging.StreamHandler(stdout)
        log_handler.setFormatter(formatter)
        logging.basicConfig(stream=stdout, level=log_level)
        logger = logging.getLogger()
        del logger.handlers[:]
        logger.addHandler(log_handler)

        self._loggers = {}

    def _add_logger(self, name):
        from logging import getLogger
        from logging import getLevelName

        new_logger = getLogger(name)

        log_level = self._find_log_level(name)
        if log_level is not None:
            new_logger.level = getLevelName(log_level)

        self._loggers[name] = new_logger

    def _find_log_level(self, name):
        from foundations.global_state import config_manager

        longest_match = 0
        log_level = None

        log_levels = config_manager.config().get('namespaced_log_levels', {})
        for key, value in log_levels.items():
            if len(key) > longest_match and name.startswith(key):
                longest_match = len(key)
                log_level = value

        return log_level
