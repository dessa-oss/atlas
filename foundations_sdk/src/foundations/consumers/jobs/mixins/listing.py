"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class Listing(object):
    """Saves the a value to a set listing
    
    Arguments:
        redis {redis.Redis} -- A Redis connection object
    """
    
    def __init__(self, redis):
        self._redis = redis

    def call(self, message, timestamp, meta_data):
        """See above
        
        Arguments:
            message {dict} -- Event attributes
            timestamp {int} -- The time the event was created
            meta_data {dict} -- Additional data about the event
        """

        scope = self._scope()
        scope_value = self._scope_value(message)
        listing_name = self._listing_name()
        value = self._listing_value(message)
        self._redis.sadd('{}:{}:{}'.format(scope, scope_value, listing_name), value)

    def _scope(self):
        pass

    def _listing_name(self):
        pass

    def _scope_value(self, message):
        pass

    def _listing_value(self, message):
        pass
