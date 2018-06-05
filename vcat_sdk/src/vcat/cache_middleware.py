from vcat.stage_cache_for_middleware import StageCacheForMiddleware


class CacheMiddleware(object):

    def __init__(self, stage_config, stage_uuid):
        self._stage_config = stage_config
        self._stage_uuid = stage_uuid

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        stage_cache = StageCacheForMiddleware(
            self._stage_config.allow_caching(),
            self._stage_config.cache_name(),
            self._stage_uuid,
            args,
            kwargs,
            upstream_result_callback
        )

        cached_result = stage_cache.fetch_cache()
        if cached_result is not None:
            return cached_result

        return callback(args, kwargs)
