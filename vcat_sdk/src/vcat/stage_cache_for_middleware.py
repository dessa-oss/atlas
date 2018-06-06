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

    def fetch_cache(self):
        from vcat.global_state import cache_manager

        if self._allow_caching:
            return cache_manager.cache().get(self._cache_name)
        else:
            return None

    def submit_cache(self, value):
        from vcat.global_state import cache_manager
        return cache_manager.cache().set(self._cache_name, value)

    def _auto_cache_name(self):
        from sys import version_info
        from vcat.argument_hasher import ArgumentHasher
        from vcat.utils import merged_uuids

        hasher = ArgumentHasher(self._new_args, self._new_kwargs)
        argument_hash = hasher.make_hash()

        upstream_hash = self._result_hash(self._upstream_result)
        version_hash = self._result_hash(version_info.major)

        return merged_uuids([argument_hash, upstream_hash, version_hash, self._stage_uuid])

    def _result_hash(self, result):
        from vcat.utils import make_uuid

        return make_uuid(result, self._result_hash)

    def _log(self):
        from vcat.global_state import log_manager
        return log_manager.get_logger(__name__)
