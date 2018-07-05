"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat.stage_cache_for_middleware import StageCacheForMiddleware


class CacheMiddleware(object):

    def __init__(self, stage_config, stage_context, stage):
        self._stage_config = stage_config
        self._stage_context = stage_context
        self._stage = stage

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        if self._stage_config.allow_caching():
            stage_cache = StageCacheForMiddleware(
                self._stage_config.allow_caching(),
                self._stage_config.cache_name(),
                self._stage.uuid(),
                args,
                kwargs,
                upstream_result_callback
            )

            self._stage_context.cache_name = stage_cache.cache_name()

            cached_result = self._time(True, stage_cache.fetch_cache_option)
            if cached_result.is_present():
                self._log().debug('Fetched stage %s (%s) data from cache in %d ms', self._uuid(), self._name(), self._cache_read_time())
                self._stage_context.used_cache = True
                return cached_result.get()

            self._log().debug('Stage %s (%s) data not in cache', self._uuid(), self._name())
            result = callback(args, kwargs)

            if cached_result.is_present():
                return result
            else:
                return self._time(False, lambda: stage_cache.submit_cache(result))
        else:
            self._log().debug('Cache disabled for stage %s (%s)', self._uuid(), self._name())
            return callback(args, kwargs)

    def _uuid(self):
        return self._stage.uuid()

    def _name(self):
        return self._stage.function_name()

    def _cache_read_time(self):
        return self._stage_context.cache_read_time

    def _cache_write_time(self):
        return self._stage_context.cache_write_time

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
