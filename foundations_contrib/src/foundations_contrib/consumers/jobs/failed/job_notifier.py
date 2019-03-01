"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.consumers.jobs.mixins.job_event_notifier import JobEventNotifier

class JobNotifier(JobEventNotifier):
    """Sends a notification message when a job is failed
    
    Arguments:
        job_notifier {JobNofitier} -- A JobNotifier for sending out the messages
    """
    
    @staticmethod
    def _state():
        return 'Failed'