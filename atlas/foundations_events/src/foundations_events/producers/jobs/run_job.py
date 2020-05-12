
class RunJob(object):
    """Create and posts a message indicating that a job is running
    
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

        provenance = self._foundations_context.provenance
        message = {
            'job_id': self._foundations_context.job_id,
            'project_name': provenance.project_name,
            'monitor_name': provenance.monitor_name or 'None'
        }

        self._message_router.push_message('run_job', message)