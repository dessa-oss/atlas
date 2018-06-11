"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class ContextAwareMiddleware(object):

    def __init__(self, stage_context, stage):
        self._stage_context = stage_context
        self._stage = stage

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        from vcat.context_aware import ContextAware

        if isinstance(self._stage.function, ContextAware):
            self._stage.function.set_context(self._stage_context)

        return callback(args, kwargs)
