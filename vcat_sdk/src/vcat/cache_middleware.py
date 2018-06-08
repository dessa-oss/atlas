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

        cached_result = self._time(True, stage_cache.fetch_cache)
        if cached_result is not None:
            self._log().debug('Fetched stage %s data from cache', self._stage_uuid)
            self._stage_context.used_cache = True
            return cached_result

        self._log().debug('Stage %s data not in cache', self._stage_uuid)
        result = callback(args, kwargs)
        return self._time(False, lambda: stage_cache.submit_cache(result))

    def _time(self, is_read, callback):
        import time

        start_time = time.time()
        return_value = callback()
        end_time = time.time()
        delta_time = end_time - start_time

        if is_read:
            self._stage_context.cache_read_time = delta_time
        else:
            self._stage_context.cache_write_time = delta_time

        return return_value

    def _log(self):
        from vcat.global_state import log_manager
        return log_manager.get_logger(__name__)
