"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class Annotate(object):
    """Saves job annotations to redis
    
    Arguments:
        redis {redis.Redis} -- A redis connection
    """

    def __init__(self, redis):
        self._redis = redis
    
    def call(self, message, timestamp, metadata):
        key = 'jobs:{}:annotations'.format(message['job_id'])
        self._redis.hmset(key, message['annotations'])