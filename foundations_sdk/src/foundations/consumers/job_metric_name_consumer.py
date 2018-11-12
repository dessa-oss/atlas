"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class JobMetricNameConsumer(object):
    
    def __init__(self, redis):
        self._redis = redis

    def call(self, message, timestamp, meta_data):
        key = 'project:' + str(message['project_name'])
        value = message['key']
        self._redis.lpush(key, value)
