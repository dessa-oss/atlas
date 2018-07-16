"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class MiddlewareManager(object):

    class NamedMiddleware(object):

        def __init__(self, name, callback):
            self.name = name
            self.callback = callback

    def __init__(self):
        self._initial_middleware = None
        self._stage_middleware = None

    def initial_middleware(self):
        if self._initial_middleware is None:
            self._initial_middleware = []

        return self._initial_middleware

    def stage_middleware(self):
        if self._stage_middleware is None:
            self._stage_middleware = [
                self._make_middleware(
                    'Redundant', MiddlewareManager._create_redundant_middleware),
                self._make_middleware(
                    'Error', MiddlewareManager._create_error_middleware),
                self._make_middleware(
                    'StageOutput', MiddlewareManager._create_stage_output_middleware),
                self._make_middleware(
                    'StageLog', MiddlewareManager._create_stage_log_middleware),
                self._make_middleware(
                    'ArugmentFiller', MiddlewareManager._create_argument_filler_middleware),
                self._make_middleware(
                    'Cache', MiddlewareManager._create_cache_middleware),
                self._make_middleware(
                    'UpstreamResult', MiddlewareManager._create_upstream_result_middleware),
                self._make_middleware(
                    'ContextAware', MiddlewareManager._create_context_aware_middleware),
                self._make_middleware(
                    'TimeStage', MiddlewareManager._create_time_stage_middleware),
                self._make_middleware(
                    'StageLogging', MiddlewareManager._create_stage_logging_middleware)
            ]
            self._load_configured_stage_middleware()

        return self._stage_middleware

    def append_initial(self, name, middleware_callback):
        middleware = self._make_middleware(name, middleware_callback)
        self.initial_middleware().append(middleware)

    def add_initial_middleware_before(self, before, name, middleware_callback):
        previous_index = self._find_middleware_index(
            self.initial_middleware(), before)
        middleware = self._make_middleware(name, middleware_callback)
        self.initial_middleware().insert(previous_index, middleware)

    def append_stage(self, name, middleware_callback):
        middleware = self._make_middleware(name, middleware_callback)
        self.stage_middleware().append(middleware)

    def add_stage_middleware_before(self, before, name, middleware_callback):
        previous_index = self._find_middleware_index(
            self.stage_middleware(), before)
        middleware = self._make_middleware(name, middleware_callback)
        self.stage_middleware().insert(previous_index, middleware)

    def _load_configured_stage_middleware(self):
        from foundations.global_state import config_manager

        configured_middleware = config_manager.config().get('stage_middleware', [])
        for middleware_config in configured_middleware:
            self._log().debug('Loading configured stage middleware {}'.format(middleware_config))

            middleware = self._make_middleware(middleware_config['name'], middleware_config['constructor'])
            if 'insert_before' in middleware_config:
                previous_index = self._find_middleware_index(self._stage_middleware, middleware_config['insert_before'])
                self._stage_middleware.insert(previous_index, middleware)
            else:
                self._stage_middleware.append(middleware)

    def _find_middleware_index(self, middleware, name):
        for index, value in enumerate(middleware):
            if value.name == name:
                return index
        raise ValueError(
            'Previous middleware `{}` does not exist'.format(name))

    def _make_middleware(self, name, callback):
        return MiddlewareManager.NamedMiddleware(name, callback)

    def _log(self):
        from foundations.global_state import log_manager
        return log_manager.get_logger(__name__)

    @staticmethod
    def _create_redundant_middleware(pipeline_context, stage_config, stage_context, stage):
        from foundations.redundant_execution_middleware import RedundantExecutionMiddleware
        return RedundantExecutionMiddleware(stage)

    @staticmethod
    def _create_error_middleware(pipeline_context, stage_config, stage_context, stage):
        from foundations.error_middleware import ErrorMiddleware
        return ErrorMiddleware(stage_context)

    @staticmethod
    def _create_stage_output_middleware(pipeline_context, stage_config, stage_context, stage):
        from foundations.stage_output_middleware import StageOutputMiddleware
        return StageOutputMiddleware(pipeline_context, stage_config, stage.uuid(), stage_context)

    @staticmethod
    def _create_stage_log_middleware(pipeline_context, stage_config, stage_context, stage):
        from foundations.stage_log_middleware import StageLogMiddleware
        return StageLogMiddleware(stage_context)

    @staticmethod
    def _create_argument_filler_middleware(pipeline_context, stage_config, stage_context, stage):
        from foundations.argument_filler_middleware import ArgumentFillerMiddleware
        return ArgumentFillerMiddleware(stage)

    @staticmethod
    def _create_cache_middleware(pipeline_context, stage_config, stage_context, stage):
        from foundations.cache_middleware import CacheMiddleware
        return CacheMiddleware(stage_config, stage_context, stage)

    @staticmethod
    def _create_upstream_result_middleware(pipeline_context, stage_config, stage_context, stage):
        from foundations.upstream_result_middleware import UpstreamResultMiddleware
        return UpstreamResultMiddleware()

    @staticmethod
    def _create_context_aware_middleware(pipeline_context, stage_config, stage_context, stage):
        from foundations.context_aware_middleware import ContextAwareMiddleware
        return ContextAwareMiddleware(stage_context, stage)

    @staticmethod
    def _create_time_stage_middleware(pipeline_context, stage_config, stage_context, stage):
        from foundations.time_stage_middleware import TimeStageMiddleware
        return TimeStageMiddleware(stage_context, stage)

    @staticmethod
    def _create_stage_logging_middleware(pipeline_context, stage_config, stage_context, stage):
        from foundations.stage_logging_middleware import StageLoggingMiddleware
        return StageLoggingMiddleware(stage)
