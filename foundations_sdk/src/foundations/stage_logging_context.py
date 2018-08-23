"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class StageLoggingContext(object):
    """Global context to be used across foundations

    Arguments:
        logger {StageLogger} -- Initial logger to be used
    """

    class ChangeLogger(object):
        """Internal support class for managing state

        Arguments:
            context {StageLoggingContext} -- The owning context
            logger {StageLogger} -- The stage logger used to update the context
        """

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
        """Logs a named metric to the internal logger

        Arguments:
            key {str} -- name of the metric
            value {object} -- value of the metric
        """

        from foundations.utils import is_string

        if not is_string(key):
            raise ValueError('Invalid metric name `{}`'.format(key))

        self._logger.log_metric(key, value)

    def change_logger(self, new_logger):
        """Changes the current logging backend for the context
        and resets it when when the with block goes out of scope

        Arguments:
            new_logger {StageLogger} -- new logger to use

        Returns:
            ChangeLogger -- the internal mechanism for changing the logger
        """

        return self.ChangeLogger(self, new_logger)
