
from foundations_events.consumers.jobs.mixins.job_event_notifier import JobEventNotifier

class JobNotifier(JobEventNotifier):
    """Sends a notification message when a job is queued
    
    Arguments:
        job_notifier {JobNofitier} -- A JobNotifier for sending out the messages
    """
    
    @staticmethod
    def _state():
        return 'Queued'