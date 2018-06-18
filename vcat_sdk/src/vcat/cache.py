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
        from vcat.serializer import deserialize

        return deserialize(self._cache_backend.get(key))

    def get_binary(self, key):
        return self._cache_backend.get(key)

    def set(self, key, value):
        from vcat.serializer import serialize

        self._cache_backend.set(key, serialize(value))
        return value

    def set_binary(self, key, serialized_value):
        self._cache_backend.set(key, serialized_value)
        return serialized_value

    def get_or_set(self, key, value):
        return self.get(key) or self.set(key, value)

    def get_or_set_callback(self, key, callback):
        return self.get(key) or self.set(key, callback())
