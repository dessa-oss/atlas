"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class RedisConnector(object):
    """Acts as a callback for the LazyRedis class,
    allowing it to be called directly without knowledge of
    how configuring a Redis url works

    Arguments:
        config_manager {ConfigManager} -- A provider for the Redis connection string
        connection_callback {callable} -- Callback to provide the connection string to
    """

    def __init__(self, config_manager, connection_callback):
        self._config_manager = config_manager
        self._connection_callback = connection_callback

    def __call__(self):
        """Returns the result of the callback, given a connection string

        Returns:
            object -- The return value of the evaluated callback
        """

        if self._is_redis_configured():
            connection_string = self._config_manager['redis_url']
            return self._connection_callback(connection_string)
        else:
            return self._connection_callback('redis://localhost:6379')

    def _is_redis_configured(self):
        return 'redis_url' in self._config_manager.config()
