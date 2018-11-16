"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 11 2018
"""

class RunJob(object):
    """Create and posts a message indicating that a job is running
    
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

        provenance = self._pipeline_context.provenance
        message = {
            'job_id': self._pipeline_context.file_name,
            'project_name': provenance.project_name
        }

        self._message_router.push_message('run_job', message)