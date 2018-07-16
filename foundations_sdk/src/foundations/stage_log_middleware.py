"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class StageLogMiddleware(object):

    def __init__(self, stage_context):
        self._stage_context = stage_context

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        stage_output = callback(args, kwargs)
        if isinstance(stage_output, tuple) and len(stage_output) == 2:
            return_value, result = stage_output
            self._stage_context.stage_log = result
        else:
            return_value = stage_output
        return return_value
