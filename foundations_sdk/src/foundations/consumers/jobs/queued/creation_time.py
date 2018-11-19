"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations.consumers.jobs.mixins.time_setter import TimeSetter

class CreationTime(TimeSetter):
    """Stores the creation time for a queued job
    
    Arguments:
        redis {redis.Redis} -- A Redis connection object
    """
    
    def _listing_name(self):
        return 'jobs'

    def _listing_value(self, message):
        return message['job_id']

    def _timestamp_name(self):
        return 'creation_time'
