"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class CacheManager(object):

    def __init__(self):
        self._cache = None

    def cache(self):
        if self._cache is None:
            self._load()
        return self._cache

    def _load(self):
        from vcat.global_state import config_manager
        from vcat.null_cache_backend import NullCacheBackend
        from vcat.cache import Cache

        cache_backend = config_manager.reflect_instance(
            'cache', 'cache', lambda: NullCacheBackend())
        self._cache = Cache(cache_backend)
