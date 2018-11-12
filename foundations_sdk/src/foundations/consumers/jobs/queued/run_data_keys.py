"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class RunDataKeys(object):
    
    def __init__(self, redis):
        self._redis = redis

    def call(self, message, timestamp, meta_data):
        for key in message['job_parameters'].keys():
            self._redis.sadd('projects:{}:job_parameter_names'.format(message['project_name']), key)
