"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class StageOutputMiddleware(object):
    """MLFlow integration for creating artifacts from stage outputs that also
    supports saving csv files to make easier viewing on the dashboard

    Arguments:
        pipeline_context {PipelineContext} -- Unused
        stage_config {StageConfig} -- Unused
        stage_context {StageContext} -- Used to determine if and what to store as an artifact
        stage {Stage} -- Stage to fetch meta data from
    """

    def __init__(self, pipeline_context, stage_config, stage_context, stage):
        self._stage_context = stage_context
        self._stage = stage

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        """Executes the middleware

        Arguments:
            upstream_result_callback {function} -- Unused
            filler_builder {[type]} -- Unused
            filler_kwargs {[type]} -- Unused
            args {[type]} -- Passed to callback
            kwargs {[type]} -- Passed to callback
            callback {function} -- Callback to call before storing the output

        Returns:
            Object -- The result of calling callback
        """

        result = callback(args, kwargs)
        if self._has_stage_output():
            self._save_stage_output(result)

        return result

    def _has_stage_output(self):
        return self._stage_context.has_stage_output

    def _save_stage_output(self, result):
        from pandas import DataFrame

        if isinstance(result, DataFrame):
            self._save_csv_artifact(result)
        else:
            self._save_binary_artifact(result)

    def _save_csv_artifact(self, result):
        from vcat.simple_tempfile import SimpleTempfile

        with SimpleTempfile('w+b', '.csv') as temp_file:
            self._write_csv(result, temp_file)
            self._log_artifact(temp_file)

    def _write_csv(self, result, temp_file):
        result.to_csv(temp_file.name)

    def _save_binary_artifact(self, result):
        from vcat.simple_tempfile import SimpleTempfile

        with SimpleTempfile('w+b', '.bin') as temp_file:
            self._write_binary(result, temp_file)
            self._log_artifact(temp_file)

    def _write_binary(self, result, temp_file):
        from vcat.serializer import serialize_to_file

        serialize_to_file(result, temp_file.file)
        temp_file.flush()

    def _log_artifact(self, file):
        from mlflow import log_artifact
        log_artifact(file.name, self._name())

    def _name(self):
        return self._stage.function_name()
