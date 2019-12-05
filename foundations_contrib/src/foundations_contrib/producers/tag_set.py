"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class TagSet(object):
    
    def __init__(self, message_router, job_id, metric_key, metric_value):
        self._message_router = message_router
        self._job_id = job_id
        self._metric_key = metric_key
        self._metric_value = metric_value

    def push_message(self):
        message = {
            'job_id': self._job_id, 
            'key': self._metric_key, 
            'value': self._metric_value
        }

        self._message_router.push_message('job_tag', message)
