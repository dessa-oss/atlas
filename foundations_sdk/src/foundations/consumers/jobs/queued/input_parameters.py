"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class InputParameters(object):
    """Stores information about the input parameters used to create each
    parameter for a Foundations stage
    
    Arguments:
        redis {redis.Redis} -- A Redis connection object
    """
    
    def __init__(self, redis, serializer):
        self._redis = redis
        self._serializer = serializer

    def call(self, message, timestamp, meta_data):
        """See above
        
        Arguments:
            message {dict} -- Event attributes
            timestamp {int} -- The time the event was created
            meta_data {dict} -- Additional data about the event
        """

        serialized_run_data = self._serializer.dumps(message['input_parameters'])
        self._redis.set('jobs:{}:input_parameters'.format(message['job_id']), serialized_run_data)
