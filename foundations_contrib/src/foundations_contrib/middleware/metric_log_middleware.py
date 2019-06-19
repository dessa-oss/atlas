"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.middleware.basic_stage_middleware import BasicStageMiddleware


class MetricLogMiddleware(BasicStageMiddleware):

    class MetricsLogger(object):

        def __init__(self, message_router, project_name, job_id):
            self._message_router = message_router
            self._project_name = project_name
            self._job_id = job_id

        def push_metric(self, key, value):
            message = {
                'project_name': self._project_name, 
                'job_id': self._job_id, 
                'key': key, 'value': value
            }

            self._message_router.push_message('job_metrics', message)

    class Producer(object):

        def __init__(self, message_router, pipeline_context, stage_context):
            self._message_router = message_router
            self._pipeline_context = pipeline_context
            self._stage_context = stage_context

        def push_message(self):
            for metric in self._stage_context.stage_log:
                self._push_message_to_channel(metric['key'], metric['value'])

        def _push_message_to_channel(self, key, value):
            metrics_logger = MetricLogMiddleware.MetricsLogger(self._message_router, self._project_name(), self._job_id())
            metrics_logger.push_metric(key, value)

        def _project_name(self):
            return self._pipeline_context.provenance.project_name

        def _job_id(self):
            return self._pipeline_context.file_name

    def call(self, upstream_result_callback, filler_builder, filler_kwargs, args, kwargs, callback):
        """
        This middleware logs events to a message route named 'job_metrics'

        Arguments:
            upstream_result_callback - not used
            filler_builder - not used
            filler_kwargs - not used
            args - arguments for callback function
            kwargs - keyword arguments for callback function
            callback - function to run stage

        Return:
            return_value - result from callback execution
        """
        from foundations.global_state import message_router

        return_value = callback(args, kwargs)

        self.Producer(message_router, self._pipeline_context,
                      self._stage_context).push_message()

        return return_value
