
class FailedJob(object):
    """Create and posts a message indicated that a job has been failed
    
    Arguments:
        message_router {MessageRouter} -- The message router with which to push the message with
        pipeline_context {PipelineContext} -- The pipeline context associated with the job
        error_information {dict} -- The error information provided by the StageContext of the failed stage
    """
    
    def __init__(self, message_router, foundations_context, error_information):
        self._message_router = message_router
        self._foundations_context = foundations_context
        self._error_information = error_information

    def push_message(self):
        """See above
        """

        import traceback

        error_information = {
            'type': repr(self._error_information['type']),
            'exception': str(self._error_information['exception']),
            'traceback': traceback.format_list(self._error_information['traceback'])
        }
        job_id = self._foundations_context.job_id
        message = {
            'job_id': job_id,
            'error_information': error_information,
            'project_name': self._foundations_context.provenance.project_name
        }
        self._message_router.push_message('fail_job', message)
