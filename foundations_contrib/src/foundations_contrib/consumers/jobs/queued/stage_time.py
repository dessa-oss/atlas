"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.consumers.jobs.queued.mixins.attribute_key_list import AttributeKeyList
import time, json


class StageTime(object):
    """Stores a list of all common stage input parameter keys for a project in redis

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

        for key in message['stage_uuids']:
            self._redis.execute_command('ZADD', 'projects:{}:{}'.format(message['project_name'], 'stage_time'), 'NX', timestamp, key)