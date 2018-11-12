"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class RunData(object):
    
    def __init__(self, redis, serializer):
        self._redis = redis
        self._serializer = serializer

    def call(self, message, timestamp, meta_data):
        serialized_run_data = self._serializer.dumps(message['job_parameters'])
        self._redis.set('jobs:{}:parameters'.format(message['job_id']), serialized_run_data)
