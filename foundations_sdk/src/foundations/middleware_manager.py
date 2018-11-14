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

    def __init__(self, config_manager):
        self._stage_middleware = None
        self._config_manager = config_manager

    def stage_middleware(self):
        if self._stage_middleware is None:
            self._set_initial_middleware()
            self._load_configured_stage_middleware()

        return self._stage_middleware

    def append_stage(self, name, middleware_callback):
        middleware = self._make_middleware(name, middleware_callback)
        self.stage_middleware().append(middleware)

    def add_stage_middleware_before(self, before, name, middleware_callback):
        previous_index = self._find_middleware_index(
            self.stage_middleware(), before)
        middleware = self._make_middleware(name, middleware_callback)
        self.stage_middleware().insert(previous_index, middleware)

    def _set_initial_middleware(self):
        from foundations.middleware.argument_middleware import ArgumentMiddleware
        from foundations.middleware.argument_filling_middleware import ArgumentFillingMiddleware
        from foundations.middleware.new_stage_log_middleware import NewStageLogMiddleware
        from foundations.middleware.metric_log_middleware import MetricLogMiddleware

        self._stage_middleware = []
        self._append_middleware(
            'Redundant', MiddlewareManager._create_redundant_middleware)
        self._append_middleware(
            'ExceptionHook', MiddlewareManager._create_exception_hook_middleware)
        self._append_middleware(
            'Error', MiddlewareManager._create_error_middleware)
        self._append_middleware(
            'StageOutput', MiddlewareManager._create_stage_output_middleware)
        self._append_middleware(
            'UpstreamResult', MiddlewareManager._create_upstream_result_middleware)
        self._append_middleware('Argument', ArgumentMiddleware)
        self._append_middleware(
            'NewCache', MiddlewareManager._create_new_cache_middleware)
        self._append_middleware('ArgumentFilling', ArgumentFillingMiddleware)
        self._append_middleware(
            'ContextAware', MiddlewareManager._create_context_aware_middleware)
        self._append_middleware(
            'TimeStage', MiddlewareManager._create_time_stage_middleware)
        self._append_middleware(
            'StageLogging', MiddlewareManager._create_stage_logging_middleware)
        self._append_middleware('MetricLog', MetricLogMiddleware)
        self._append_middleware(
            'NewStageLog', NewStageLogMiddleware)

    def _append_middleware(self, name, callback):
        middleware = self._make_middleware(name, callback)
        self._stage_middleware.append(middleware)

    def _load_configured_stage_middleware(self):
        configured_middleware = self._config_manager.config().get('stage_middleware', [])
        for middleware_config in configured_middleware:
            self._log().debug('Loading configured stage middleware {}'.format(middleware_config))

            middleware = self._make_middleware(
                middleware_config['name'], middleware_config['constructor'])
            if 'insert_before' in middleware_config:
                previous_index = self._find_middleware_index(
                    self._stage_middleware, middleware_config['insert_before'])
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
        from foundations.middleware.redundant_execution_middleware import RedundantExecutionMiddleware
        return RedundantExecutionMiddleware(stage)

    @staticmethod
    def _create_error_middleware(pipeline_context, stage_config, stage_context, stage):
        from foundations.middleware.error_middleware import ErrorMiddleware
        return ErrorMiddleware(stage_context)

    @staticmethod
    def _create_stage_output_middleware(pipeline_context, stage_config, stage_context, stage):
        from foundations.middleware.stage_output_middleware import StageOutputMiddleware
        return StageOutputMiddleware(stage_config, stage_context)

    @staticmethod
    def _create_new_cache_middleware(pipeline_context, stage_config, stage_context, stage):
        from foundations.middleware.new_cache_middleware import NewCacheMiddleware
        from foundations.stage_cache import StageCache

        return NewCacheMiddleware(StageCache, pipeline_context, stage_config, stage_context, stage)

    @staticmethod
    def _create_upstream_result_middleware(pipeline_context, stage_config, stage_context, stage):
        from foundations.middleware.upstream_result_middleware import UpstreamResultMiddleware
        return UpstreamResultMiddleware()

    @staticmethod
    def _create_context_aware_middleware(pipeline_context, stage_config, stage_context, stage):
        from foundations.middleware.context_aware_middleware import ContextAwareMiddleware
        return ContextAwareMiddleware(stage_context, stage)

    @staticmethod
    def _create_time_stage_middleware(pipeline_context, stage_config, stage_context, stage):
        from foundations.middleware.time_stage_middleware import TimeStageMiddleware
        return TimeStageMiddleware(stage_context, stage)

    @staticmethod
    def _create_stage_logging_middleware(pipeline_context, stage_config, stage_context, stage):
        from foundations.middleware.stage_logging_middleware import StageLoggingMiddleware
        return StageLoggingMiddleware(stage)

    @staticmethod
    def _create_exception_hook_middleware(pipeline_context, stage_config, stage_context, stage):
        from foundations.middleware.exception_hook_middleware import ExceptionHookMiddleware
        return ExceptionHookMiddleware()
