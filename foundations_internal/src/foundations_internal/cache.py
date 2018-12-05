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
        return self.get_binary_option(key).map(self._safe_deserialize)

    def get_metadata_option(self, key):
        return self.get_metadata_binary_option(key).map(self._safe_deserialize)

    def get_binary(self, key):
        return self.get_binary_option(key).get_or_else(None)

    def get_binary_option(self, key):
        from foundations_contrib.option import Option

        result = self._cache_backend.get(key)
        if result is None:
            self._log().debug('Cache miss for key: %s', key)
        return Option(result)

    def get_metadata_binary(self, key):
        return self.get_metadata_binary_option(key).get_or_else(None)

    def get_metadata_binary_option(self, key):
        from foundations_contrib.option import Option

        result = self._cache_backend.get_metadata(key)
        if result is None:
            self._log().debug('Cache miss for key: %s', key)
        return Option(result)

    def set(self, key, value, metadata={}, **flags):
        from foundations_internal.fast_serializer import serialize

        self.set_binary(key, serialize(value), serialize(metadata), **flags)
        return value

    def set_binary(self, key, serialized_value, serialized_metadata, **flags):
        self._cache_backend.set(key, serialized_value,
                                serialized_metadata, **flags)
        return serialized_value

    def get_or_set(self, key, value, metadata, **flags):
        def _set():
            from foundations_contrib.something import Something

            self.set(key, value, metadata, **flags)
            return Something(value)

        return self.get_option(key).fallback(_set).get()

    def get_or_set_callback(self, key, metadata, callback, **flags):
        def _set():
            from foundations_contrib.something import Something

            value = callback()
            self.set(key, value, metadata, **flags)
            return Something(value)

        return self.get_option(key).fallback(_set).get()

    def get_or_set_binary(self, key, value, metadata, **flags):
        def _set_binary():
            from foundations_contrib.something import Something

            self.set_binary(key, value, metadata, **flags)
            return Something(value)

        return self.get_option(key).fallback(_set_binary).get()

    def get_or_set_binary_callback(self, key, metadata, callback, **flags):
        def _set_binary():
            from foundations_contrib.something import Something

            value = callback()
            self.set_binary(key, value, metadata, **flags)
            return Something(value)

        return self.get_option(key).fallback(_set_binary).get()

    def _log(self):
        from foundations.global_state import log_manager
        return log_manager.get_logger(__name__)

    def _safe_deserialize(self, data):
        from foundations_internal.fast_serializer import deserialize

        try:
            return deserialize(data)
        except:
            return None
