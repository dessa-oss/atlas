from vcat.stage_cache_for_middleware import StageCacheForMiddleware


class CacheMiddleware(object):

    def __init__(self, stage_config, stage_context, stage_uuid):
        self._stage_config = stage_config
        self._stage_context = stage_context
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
            self._log().debug('Fetched stage %s data from cache', self._stage_uuid)
            self._stage_context.used_cache = True
            return cached_result

        self._log().debug('Stage %s data not in cache', self._stage_uuid)
        result = callback(args, kwargs)
        return stage_cache.submit_cache(result)

    def _log(self):
        from vcat.global_state import log_manager
        return log_manager.get_logger(__name__)