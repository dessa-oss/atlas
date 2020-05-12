
class CompleteJob(object):
    """Create and posts a message indicating that a job has been completed
    
    Arguments:
        message_router {MessageRouter} -- The message router with which to push the message with
        pipeline_context {PipelineContext} -- The pipeline context associated with the job
    """
    
    def __init__(self, message_router, foundations_context):
        self._message_router = message_router
        self._foundations_context = foundations_context

    def push_message(self):
        """See above
        """

        self._message_router.push_message(
            'complete_job',
            {
                'job_id': self._foundations_context.job_id,
                'project_name': self._foundations_context.project_name
            }
        )
