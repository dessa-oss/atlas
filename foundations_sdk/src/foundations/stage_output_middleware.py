"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class StageOutputMiddleware(object):

    def __init__(self, stage_config, stage_context):
        self._stage_config = stage_config
        self._stage_context = stage_context

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        result = callback(args, kwargs)
        if self._stage_config.persisted():
            self._stage_context.set_stage_output(result)
        return result
