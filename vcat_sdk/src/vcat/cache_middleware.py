from vcat.stage_cache_for_middleware import StageCacheForMiddleware


class CacheMiddleware(object):
    def __init__(self, allow_caching, cache_name, stage_uuid):
        self._allow_caching = allow_caching
        self._cache_name = cache_name
        self._stage_uuid = stage_uuid

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        stage_cache = StageCacheForMiddleware(
            self._allow_caching, 
            self._cache_name, 
            self._stage_uuid,
            args,
            kwargs,
            upstream_result_callback
        )
        
        cached_result = stage_cache.fetch_cache()
        if cached_result is not None:
            return cached_result

        return callback(args, kwargs)
