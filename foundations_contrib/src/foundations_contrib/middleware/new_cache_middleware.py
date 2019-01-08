"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.middleware.basic_stage_middleware import BasicStageMiddleware


class NewCacheMiddleware(BasicStageMiddleware):

    def __init__(self, cache_implementation, pipeline_context, stage_config, stage_context, stage):
        self._cache_implementation = cache_implementation
        super(NewCacheMiddleware, self).__init__(
            pipeline_context, stage_config, stage_context, stage)

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        stage_cache = self._cache_implementation(
            self._pipeline_context, self._stage, self._stage_config, args)
        self._stage_context.cache_uuid = stage_cache.cache_name()

        cached_value = stage_cache.fetch_option()
        if cached_value.is_present():
            self._stage_context.used_cache = True
            return cached_value.get()

        result = callback(args, kwargs)
        stage_cache.submit(result)

        return result
