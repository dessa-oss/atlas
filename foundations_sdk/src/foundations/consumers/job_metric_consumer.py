"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class JobMetricConsumer(object):
    
    def __init__(self, redis):
        self._redis = redis

    def call(self, message, timestamp, meta_data):
        from foundations.fast_serializer import serialize
        key = 'job:'+str(message['job_id'])
        value = (timestamp, message['key'], message['value'])
        self._redis.set(key, serialize(value))
