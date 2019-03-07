"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def job_annotations(redis, job_id):
    encoded_annotations = _encoded_job_annotations(redis, job_id).items()
    return {key.decode(): value.decode() for key, value in encoded_annotations}

def _encoded_job_annotations(redis, job_id):
    key = 'jobs:{}:annotations'.format(job_id)
    return redis.hgetall(key)
