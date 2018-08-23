"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class StageLogger(object):

    def __init__(self, pipeline_context, stage, stage_config, stage_context):
        self._pipeline_context = pipeline_context
        self._stage = stage
        self._stage_config = stage_config
        self._stage_context = stage_context

    def log_metric(self, key, value):
        """Logs a metric to the stage log

        Arguments:
            key {string} -- The name of the metric to log
            value {object} -- The value to store
        """

        from time import time
        self._stage_context.stage_log.append(
            {'key': key, 'value': value, 'timestamp': time()})

    def pipeline_context(self):
        """The PipelineContext associated with the Stage

        Returns:
            PipelineContext -- As above
        """

        return self._pipeline_context

    def stage(self):
        """The Stage itself

        Returns:
            Stage -- As above
        """

        return self._stage

    def stage_config(self):
        """The StageConfig associated with the Stage

        Returns:
            StageConfig -- As above
        """

        return self._stage_config

    def stage_context(self):
        """The StageContext associated with the Stage

        Returns:
            StageContext -- As above
        """

        return self._stage_context
