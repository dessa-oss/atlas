"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class ArgumentFillerMiddleware(object):
    def __init__(self, stage):
        self._stage = stage

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        new_args, new_kwargs = filler_builder(*args, **kwargs).fill(**filler_kwargs)
        return callback(new_args, new_kwargs)
    