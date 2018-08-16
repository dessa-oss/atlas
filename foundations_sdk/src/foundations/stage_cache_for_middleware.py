"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class StageCacheForMiddleware(object):

    def __init__(self, allow_caching, cache_name, stage_uuid, new_args, new_kwargs, fetch_upstream_result_callback):
        self._allow_caching = allow_caching
        self._cache_name = cache_name
        self._stage_uuid = stage_uuid
        self._upstream_result = None
        self._new_args = new_args
        self._new_kwargs = new_kwargs

        if self._allow_caching:
            if self._cache_name is None:
                self._upstream_result = fetch_upstream_result_callback()
                self._cache_name = self._auto_cache_name()

        self._log().debug('Stage %s cache name is %s', stage_uuid, repr(self._cache_name))

    def cache_name(self):
        return self._cache_name

    def fetch_cache(self):
        return self.fetch_cache_option().get_or_else(None)

    def fetch_cache_option(self):
        from foundations.global_state import cache_manager
        from foundations.nothing import Nothing

        if self._allow_caching:
            return cache_manager.cache().get_option(self._cache_name)
        else:
            return Nothing

    def submit_cache(self, value):
        from foundations.global_state import cache_manager
        return cache_manager.cache().set(self._cache_name, value)

    def _auto_cache_name(self):
        from sys import version_info
        from foundations.argument_hasher import ArgumentHasher
        from foundations.utils import merged_uuids

        hasher = ArgumentHasher(self._new_args, self._new_kwargs)
        argument_hash = hasher.make_hash()

        upstream_hash = self._result_hash(self._upstream_result)
        version_hash = self._result_hash(version_info.major)

        return merged_uuids([argument_hash, upstream_hash, version_hash, self._stage_uuid])

    def _result_hash(self, result):
        from foundations.utils import make_uuid

        return make_uuid(result, self._result_hash)

    def _log(self):
        from foundations.global_state import log_manager
        return log_manager.get_logger(__name__)
