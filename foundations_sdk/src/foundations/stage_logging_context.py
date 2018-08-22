"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class StageLoggingContext(object):

    class ChangeLogger(object):

        def __init__(self, context, logger):
            self._context = context
            self._logger = logger
            self._previous_logger = None

        def __enter__(self):
            self._previous_logger = self._context._logger
            self._context._logger = self._logger

        def __exit__(self, exception_type, exception_value, traceback):
            self._context._logger = self._previous_logger

    def __init__(self, logger):
        self._logger = logger

    def log_metric(self, key, value):
        self._logger.log_metric(key, value)

    def change_logger(self, new_logger):
        return self.ChangeLogger(self, new_logger)
