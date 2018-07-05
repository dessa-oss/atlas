"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class StageLogMiddleware(object):

    def __init__(self, pipeline_context, stage_config, stage_context, stage):
        self._stage = stage

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        from mlflow import log_metric

        stage_output = callback(args, kwargs)
        if isinstance(stage_output, tuple):
            _, metrics = stage_output
            for key, value in metrics.items():
                metric_name = "{}.{}".format(self._stage.function_name(), key)
                log_metric(metric_name, value)
        return stage_output

    def _log(self):
        from vcat.global_state import log_manager
        return log_manager.get_logger(__name__)
