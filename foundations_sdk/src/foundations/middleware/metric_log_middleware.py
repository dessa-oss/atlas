"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations.middleware.basic_stage_middleware import BasicStageMiddleware


class MetricLogMiddleware(BasicStageMiddleware):

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
        return_value = callback(args, kwargs)

        for metric in self._stage_context.stage_log:
            self._push_message_to_channel(metric['key'], metric['value'], 'job_metrics')

        return return_value

    def _push_message_to_channel(self, key, value, channel_name):
        from foundations.global_state import message_router
        message_router.push_message(
            channel_name, {'project_name': self._project_name(), 'job_id': self._job_id(), 'key': key, 'value': value})

    def _project_name(self):
        return self._pipeline_context.provenance.project_name

    def _job_id(self):
        return self._pipeline_context.file_name
