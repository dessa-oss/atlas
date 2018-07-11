"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class RedundantExecutionMiddleware(object):

    def __init__(self, stage):
        self._result = None
        self._has_run = False
        self._stage = stage

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        if self._has_run:
            self._log().debug('Skipping stage %s (%s)', self._uuid(), self._name())
            return self._result
        else:
            self._log().debug('Running stage %s (%s)', self._uuid(), self._name())
            self._result = callback(args, kwargs)
            self._has_run = True
            return self._result

    def _uuid(self):
        return self._stage.uuid()

    def _name(self):
        return self._stage.function_name()

    def _log(self):
        from vcat.global_state import log_manager
        return log_manager.get_logger(__name__)
