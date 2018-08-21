"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class StageCache(object):

    def __init__(self, pipeline_context, stage, stage_config, live_arguments):
        from foundations.cache_name_generator import CacheNameGenerator

        self._pipeline_context = pipeline_context
        self._stage_config = stage_config
        self._cache_name = CacheNameGenerator(stage, live_arguments).hash()

    def cache_name(self):
        return self._cache_name

    def fetch_option(self):
        from foundations.global_state import cache_manager
        from foundations.nothing import Nothing

        if self._allow_caching():
            return cache_manager.cache().get_option(self._cache_name)

        return Nothing()

    def submit(self, value):
        from foundations.global_state import cache_manager

        if self._allow_caching():
            return cache_manager.cache().set(self._cache_name, value, {'job_uuid': self._pipeline_context.file_name})

        return value

    def _allow_caching(self):
        return self._stage_config.allow_caching()
