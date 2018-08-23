"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations.basic_stage_middleware import BasicStageMiddleware

class NewStageLogMiddleware(BasicStageMiddleware):

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        from foundations.stage_logger import StageLogger
        from foundations.stage_logging import stage_logging_context

        logger = StageLogger(self._pipeline_context, self._stage, self._stage_config, self._stage_context)
        with stage_logging_context.change_logger(logger):
            return callback(args, kwargs)
