"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class AttributeKeyList(object):
    """Stores a list of attribute keys for a project in redis
    
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

        for key in self._get_attribute(message).keys():
            self._redis.sadd('projects:{}:{}'.format(message['project_name'], self._get_attribute_key()), key)

    def _get_attribute(self, message):
        pass

    def _get_attribute_key(self):
        pass