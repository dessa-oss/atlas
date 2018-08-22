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
        if key in self._stage_context.stage_log:
            previous_value = self._stage_context.stage_log[key]
            if isinstance(previous_value, list):
                self._stage_context.stage_log[key].append(value)
            else:
                self._stage_context.stage_log[key] = [previous_value, value]
        else:
            self._stage_context.stage_log[key] = value

    def pipeline_context(self):
        return self._pipeline_context

    def stage(self):
        return self._stage

    def stage_config(self):
        return self._stage_config

    def stage_context(self):
        return self._stage_context
