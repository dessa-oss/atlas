"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class StageLoggingMiddleware(object):

    def __init__(self, stage):
        self._stage = stage

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        self._log().debug('Running stage `%s` (uuid: `%s`), file: %s, line: %s', self._stage.function_name(), self._stage.uuid(), self._stage.source_file(), self._stage.source_line())
        return_value = callback(args, kwargs)
        self._log().debug('Finished stage %s (uuid: %s)', self._stage.function_name(), self._stage.uuid())
        return return_value

    def _log(self):
        from vcat.global_state import log_manager
        return log_manager.get_logger(__name__)