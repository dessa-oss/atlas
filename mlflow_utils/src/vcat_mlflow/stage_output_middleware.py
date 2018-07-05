"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class StageOutputMiddleware(object):

    def __init__(self, pipeline_context, stage_config, stage_context, stage):
        self._stage_context = stage_context
        self._stage = stage

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        from vcat.simple_tempfile import SimpleTempfile
        from vcat.serializer import serialize_to_file
        from pandas import DataFrame
        from mlflow import log_artifact

        result = callback(args, kwargs)
        if self._stage_context.has_stage_output:
            if isinstance(result, DataFrame):
                with SimpleTempfile('w+b', '.csv') as temp_file:
                    result.to_csv(temp_file.name)
                    log_artifact(temp_file.name, self._name())
            else:
                with SimpleTempfile('w+b', '.bin') as temp_file:
                    serialize_to_file(result, temp_file.file)
                    temp_file.flush()
                    log_artifact(temp_file.name, self._name())

        return result

    def _name(self):
        return self._stage.function_name()
