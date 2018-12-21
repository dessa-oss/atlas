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

    def __init__(self, config_manager, connection_callback, environment):
        self._config = config_manager.config()
        self._connection_callback = connection_callback
        self._environment = environment

    def __call__(self):
        """Returns the result of the callback, given a connection string

        Returns:
            object -- The return value of the evaluated callback
        """

        connection_with_password = self._build_connection_string()
        return self._connection_callback(connection_with_password)


    def _get_connection_string(self):
        return self._config.get('redis_url', 'redis://localhost:6379')

    def _get_password(self):
        return self._environment.get('FOUNDATIONS_REDIS_PASSWORD', '')

    def _build_connection_string(self):
        split_connection_string = self._get_connection_string().split('//')
        scheme = split_connection_string[0]
        host_with_port = split_connection_string[1]
        return scheme + '//:' + self._get_password() + '@' + host_with_port