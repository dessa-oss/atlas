"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class GlobalMetricLogger(object):

    def __init__(self, message_router, pipeline_context):
        self._pipeline_context = pipeline_context
        self._message_router = message_router
    
    def log_metric(self, key, value):
        from foundations_contrib.global_state import log_manager
        from foundations_contrib.producers.metric_logged import MetricLogged

        if self._is_job_running():
            metric_logged_producer = MetricLogged(self._message_router, self._project_name(), self._job_id(), key, value)
            metric_logged_producer.push_message()
        else:
            logger = log_manager.get_logger(__name__)
            logger.warning('Cannot log metric if not deployed with foundations deploy')

    def _is_job_running(self):
        try:
            return self._pipeline_context.file_name is not None
        except ValueError:
            return False

    def _project_name(self):
        return self._pipeline_context.provenance.project_name

    def _job_id(self):
        return self._pipeline_context.file_name