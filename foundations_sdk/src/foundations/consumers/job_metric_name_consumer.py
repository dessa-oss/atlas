"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class JobMetricNameConsumer(object):
    """
    Class to consume the 'stage_log_middleware' channel. 
    Passes the name of job metrics into a list based on project name. 
    Arguments:
        redis {redis.Redis} -- A Redis connection object
    """

    def __init__(self, redis):
        self._redis = redis

    def call(self, message, timestamp, meta_data):
        """
        Adds metric names to redis list

        Arguments:
            message {dict} -- Event attributes
            timestamp {int} -- The time the event was created
            meta_data {dict} -- Additional data about the event
        """
        key = 'project:{}'.format(message['project_name'])
        value = message['key']
        self._redis.sadd(key, value)
