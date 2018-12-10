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

    def default_cache_enabled(self):
        from foundations.global_state import config_manager
        return config_manager.config().get('default_cache_enabled', False)

    def _load(self):
        from foundations.global_state import config_manager
        from foundations_contrib.null_cache_backend import NullCacheBackend
        from foundations_internal.cache import Cache

        cache_backend = config_manager.reflect_instance(
            'cache', 'cache', lambda: NullCacheBackend())
        self._cache = Cache(cache_backend)
