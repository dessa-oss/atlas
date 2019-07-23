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

        self._make_log_directory()
        self._load_logger_configuration()
        self._loggers = {}

    def _load_logger_configuration(self):
        import yaml
        import logging.config
        import foundations_contrib

        with open(f'{foundations_contrib.root()}/resources/logging/handlers.yaml', 'r') as file:
            config = yaml.load(file.read())
        config['handlers']['system'] = {'class': 'logging.FileHandler', 'formatter': 'simple', 'filename': f'{self._log_path()}/system.log', 'level': 'DEBUG'}
        config['root']['handlers'].append('system')
        logging.config.dictConfig(config)

    def _log_path(self):
        import os.path
        return os.path.expanduser('~/.foundations/logs')
    
    def _make_log_directory(self):
        import os
        os.makedirs(self._log_path(), exist_ok=True)

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
