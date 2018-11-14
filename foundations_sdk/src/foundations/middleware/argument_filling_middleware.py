"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations.middleware.basic_stage_middleware import BasicStageMiddleware


class ArgumentFillingMiddleware(BasicStageMiddleware):

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        new_args, new_kwargs = self._fill_arguments(args, filler_kwargs)
        new_kwargs.update(kwargs)

        return callback(new_args, new_kwargs)

    def _fill_arguments(self, args, filler_kwargs):
        from foundations.live_argument import LiveArgument

        new_args = ()
        new_kwargs = {}
        for argument in args:
            if isinstance(argument, LiveArgument):
                name = argument.name()
                if name is not None:
                    new_kwargs[name] = argument.value()
                else:
                    new_args += (argument.value(),)
            else:
                new_args += (argument,)

        return new_args, new_kwargs
