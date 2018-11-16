"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations.consumers.jobs.mixins.property_setter import PropertySetter


class JobState(PropertySetter):
    """Sets the state of a job to completed in redis
    
    Arguments:
        redis {redis.Redis} -- A Redis connection object
    """
    
    def _listing_name(self):
        return 'jobs'

    def _listing_value(self, message):
        return message['job_id']

    def _property_name(self):
        return 'state'

    def _property_value(self, message, timestamp, meta_data):
        return 'completed'
