"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class QueueJob(object):
    """Create and posts a message indicated that a job is the queue

    Arguments:
        message_router {MessageRouter} -- The message router with which to push the message with
        pipeline_context {PipelineContext} -- The pipeline context associated with the job
    """

    def __init__(self, message_router, pipeline_context):
        self._message_router = message_router
        self._pipeline_context = pipeline_context

    def push_message(self):
        """See above
        """

        message = self._message()
        self._message_router.push_message('queue_job', message)

    def _message(self):
        job_params = self._load_input_params()
        provenance = self._pipeline_context.provenance

        message = {
            'job_id': self._pipeline_context.file_name,
            'project_name': provenance.project_name,
            'job_parameters': provenance.job_run_data,
            'user_name': provenance.user_name,
            'input_parameters': job_params
        }

        return message

    def _stage_hierarchy_entries(self):
        return self._pipeline_context.provenance.stage_hierarchy.entries.items()

    def _stage_arguments(self):
        for stage_uuid, entry in self._stage_hierarchy_entries():
            for argument in entry.stage_args:
                yield stage_uuid, argument

    def _load_input_params(self):
        input_params = []
        for stage_uuid, argument in self._stage_arguments():
            parameter = self._job_parameter(stage_uuid, argument)
            input_params.append(parameter)
        return input_params

    def _job_parameter(self, stage_uuid, argument):
        return {'argument': argument, 'stage_uuid': stage_uuid}
