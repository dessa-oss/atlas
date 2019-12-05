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
        job_id = message['job_id']
        tag = message['key']
        value = message['value']

        job_annotations_key = 'jobs:{}:annotations'.format(job_id)
        
        if self._is_tag_set(job_annotations_key, tag):
            self._logger().warning('Tag `{}` updated to `{}`'.format(tag, value))

        self._redis.hmset(job_annotations_key, {tag: value})

    def _logger(self):
        from foundations_contrib.global_state import log_manager
        return log_manager.get_logger(__name__)

    def _is_tag_set(self, job_annotations_key, tag):
        annotations = self._redis.hgetall(job_annotations_key)
        decoded_annotations = {key.decode(): value.decode() for key, value in annotations.items()}

        return tag in decoded_annotations