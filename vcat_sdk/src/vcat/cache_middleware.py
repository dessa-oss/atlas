"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat.stage_cache_for_middleware import StageCacheForMiddleware


class CacheMiddleware(object):

    def __init__(self, stage_config, stage_context, stage_uuid):
        self._stage_config = stage_config
        self._stage_context = stage_context
        self._stage_uuid = stage_uuid

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        if self._stage_config.allow_caching():
            stage_cache = StageCacheForMiddleware(
                self._stage_config.allow_caching(),
                self._stage_config.cache_name(),
                self._stage_uuid,
                args,
                kwargs,
                upstream_result_callback
            )

            self._stage_context.cache_name = stage_cache.cache_name()

            cached_result = self._time(True, stage_cache.fetch_cache)
            if cached_result is not None:
                self._log().debug('Fetched stage %s data from cache', self._stage_uuid)
                self._stage_context.used_cache = True
                return cached_result

            self._log().debug('Stage %s data not in cache', self._stage_uuid)
            result = callback(args, kwargs)
            return self._time(False, lambda: stage_cache.submit_cache(result))
        else:
            self._log().debug('Cache disabled for stage %s', self._stage_uuid)
            return callback(args, kwargs)

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
