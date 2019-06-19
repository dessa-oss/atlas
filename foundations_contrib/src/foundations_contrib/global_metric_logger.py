"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class GlobalMetricLogger(object):

    def __init__(self, pipeline_context, stage_context):
        self._pipeline_context = pipeline_context
        self._stage_context = stage_context
    
    def log_metric(self, key, value):
        from foundations_contrib.global_state import log_manager

        self._stage_context.stage_log.append({'key': key, 'value': value})

        logger = log_manager.get_logger(__name__)
        logger.warning('Cannot log metric if not deployed with foundations deploy')

    def _is_job_running(self):
        return self._pipeline_context.file_name is not None