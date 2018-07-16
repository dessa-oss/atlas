"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class Cache(object):

    def __init__(self, cache_backend):
        self._cache_backend = cache_backend

    def get(self, key):
        return self.get_option(key).get_or_else(None)

    def get_option(self, key):
        from foundations.fast_serializer import deserialize
        return self.get_binary_option(key).map(deserialize)

    def get_binary(self, key):
        return self.get_binary_option(key).get_or_else(None)

    def get_binary_option(self, key):
        from foundations.option import Option

        result = self._cache_backend.get(key)
        if result is None:
            self._log().debug('Cache miss for key: %s', key)
        return Option(result)

    def set(self, key, value):
        from foundations.fast_serializer import serialize

        self._cache_backend.set(key, serialize(value))
        return value

    def set_binary(self, key, serialized_value):
        self._cache_backend.set(key, serialized_value)
        return serialized_value

    def get_or_set(self, key, value):
        def _set():
            from foundations.something import Something

            self.set(key, value)
            return Something(value)

        return self.get_option(key).fallback(_set).get()

    def get_or_set_callback(self, key, callback):
        def _set():
            from foundations.something import Something

            value = callback()
            self.set(key, value)
            return Something(value)

        return self.get_option(key).fallback(_set).get()

    def get_or_set_binary(self, key, value):
        def _set_binary():
            from foundations.something import Something

            self.set_binary(key, value)
            return Something(value)

        return self.get_option(key).fallback(_set_binary).get()

    def get_or_set_binary_callback(self, key, callback):
        def _set_binary():
            from foundations.something import Something

            value = callback()
            self.set_binary(key, value)
            return Something(value)

        return self.get_option(key).fallback(_set_binary).get()

    def _log(self):
        from foundations.global_state import log_manager
        return log_manager.get_logger(__name__)
