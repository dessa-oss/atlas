class StageCache(object):

    def __init__(self, allow_caching, cache_name, stage, filler_builder, filler_kwargs, fetch_upstream_result_callback):
        self._allow_caching = allow_caching
        self._cache_name = cache_name
        self._upstream_result = None
        self._stage = stage
        self._filler_builder = filler_builder
        self._filler_kwargs = filler_kwargs

        if self._allow_caching:
            if self._cache_name is None:
                self._upstream_result = fetch_upstream_result_callback()
                self._cache_name = self._auto_cache_name()

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
        from vcat.argument_hasher import ArgumentHasher
        from vcat.utils import merged_uuids

        new_args, new_kwargs = self._stage.fill_args_and_kwargs(
            self._filler_builder, **self._filler_kwargs)
        hasher = ArgumentHasher(new_args, new_kwargs)
        argument_hash = hasher.make_hash()

        upstream_hash = self._result_hash(self._upstream_result)

        return merged_uuids([argument_hash, upstream_hash, self._stage.uuid()])

    def _result_hash(self, result):
        from vcat.utils import make_uuid

        return make_uuid(result, self._result_hash)
