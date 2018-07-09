"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class ParameterMiddleware(object):
    """MFLow integration for logging hyper parameters to a UI

    Arguments:
        pipeline_context {PipelineContext} -- Unused
        stage_config {StageConfig} -- Unused
        stage_context {StageContext} -- Unused
        stage {Stage} -- Stage to execute and collect data from
    """

    def __init__(self, pipeline_context, stage_config, stage_context, stage):
        self._stage = stage

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        """Executes the middleware

        Arguments:
            upstream_result_callback {function} -- Unused
            filler_builder {function} -- Unused
            filler_kwargs {dict} -- Used to collect the hyper parameters
            args {tuple} -- Passed to callback
            kwargs {dict} -- Passed to callback
            callback {function} -- Callback to call before storing the output

        Returns:
            Object -- The result of calling callback
        """

        self._log_parameters(filler_kwargs)

        return callback(args, kwargs)

    def _log_parameters(self, parameters):
        from mlflow import log_param

        for key, value in parameters.items():
            param_name = key
            log_param(param_name, value)
