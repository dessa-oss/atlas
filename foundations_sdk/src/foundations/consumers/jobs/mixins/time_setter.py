"""
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
"""

from foundations.consumers.jobs.mixins.property_setter import PropertySetter

class TimeSetter(PropertySetter):
    """Saves an event timestamp to a value in redis
    
    Arguments:
        redis {redis.Redis} -- A Redis connection object
    """
    
    def _timestamp_name(self):
        pass

    def _property_name(self):
        return self._timestamp_name()

    def _property_value(self, message, timestamp, meta_data):
        return str(timestamp)
