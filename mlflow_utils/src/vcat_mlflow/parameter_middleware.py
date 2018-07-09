"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class ParameterMiddleware(object):

    def __init__(self, pipeline_context, stage_config, stage_context, stage):
        self._stage = stage

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        from mlflow import log_param

        for key, value in filler_kwargs.items():
            param_name = key
            log_param(param_name, value)

        return callback(args, kwargs)
