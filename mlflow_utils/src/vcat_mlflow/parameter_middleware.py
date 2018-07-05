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
            self._log().debug('Saving parameter {} with value {}'.format(param_name, value))
            string_value = repr(value)
            log_param(param_name, string_value)

        return callback(args, kwargs)

    def _log(self):
        from vcat.global_state import log_manager
        return log_manager.get_logger(__name__)
