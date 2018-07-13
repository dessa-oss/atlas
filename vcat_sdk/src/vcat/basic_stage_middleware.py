"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class BasicStageMiddleware(object):

    def __init__(self, pipeline_context, stage_config, stage_context, stage):
        self._pipeline_context = pipeline_context
        self._stage_config = stage_config
        self._stage_context = stage_context
        self._stage = stage

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        return callback(args, kwargs)

    def _uuid(self):
        return self._stage.uuid()

    def _name(self):
        return self._stage.function_name()
