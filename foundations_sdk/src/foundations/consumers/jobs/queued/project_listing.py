"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class ProjectListing(object):

    def __init__(self, redis):
        self._redis = redis

    def call(self, message, timestamp, meta_data):
        self._redis.sadd('project:{}:jobs:queued'.format(message['project_name']), message['job_id'])
