"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.middleware.basic_stage_middleware import BasicStageMiddleware


class ArgumentMiddleware(BasicStageMiddleware):

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        new_args = self._fill_arguments(args, filler_kwargs)
        return callback(new_args, kwargs)

    def _fill_arguments(self, args, filler_kwargs):
        from foundations_internal.live_argument import LiveArgument

        new_args = [LiveArgument(argument, filler_kwargs) for argument in args]
        return tuple(new_args)
