"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class JobNotifier(object):
    """Sends a notification message when a job is queued
    
    Arguments:
        job_notifier {JobNofitier} -- A JobNotifier for sending out the messages
    """
    
    def __init__(self, job_notifier):
        self._job_notifier = job_notifier

    def call(self, message, timestamp, meta_data):
        """See above
        
        Arguments:
            message {dict} -- Event attributes
            timestamp {int} -- The time the event was created
            meta_data {dict} -- Additional data about the event
        """

        self._job_notifier.send_message(
            """
Job Queued
Job Id: {}
Timestamp: {}
Project Name: {}
            """.format(message['job_id'], self._readable_timestamp(timestamp), message['project_name'])
        )

    @staticmethod
    def _readable_timestamp(timestamp):
        from datetime import datetime
        return datetime.fromtimestamp(timestamp)
