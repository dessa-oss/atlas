"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class TimeStageMiddleware(object):

    def __init__(self, stage_context, stage):
        self._stage_context = stage_context
        self._stage = stage

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        def timed_callback():
            return callback(args, kwargs)

        result = self._stage_context.time_callback(timed_callback)
        self._log().debug('Stage %s (%s) took %f s', self._name(), self._uuid(), self._delta_time())
        return result

    def _uuid(self):
        return self._stage.uuid()

    def _name(self):
        return self._stage.function_name()

    def _delta_time(self):
        return self._stage_context.delta_time

    def _log(self):
        from foundations.global_state import log_manager
        return log_manager.get_logger(__name__)