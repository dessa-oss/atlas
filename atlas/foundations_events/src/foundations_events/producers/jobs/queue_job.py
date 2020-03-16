

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
        provenance = self._pipeline_context.provenance

        message = {
            'job_id': self._pipeline_context.file_name,
            'project_name': provenance.project_name,
            'job_parameters': provenance.job_run_data,
            'user_name': provenance.user_name,
            'annotations': provenance.annotations,
        }

        return message
