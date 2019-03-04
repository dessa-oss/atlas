"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def list_jobs(redis):
    return {job_id.decode() for job_id in redis.smembers('projects:global:jobs:completed')}

def remove_jobs(redis, list_of_job_ids):
    for job_id in list_of_job_ids:
        redis.srem('projects:global:jobs:completed', job_id)

def add_jobs_to_archive(redis, list_of_job_ids):
    for job_id in list_of_job_ids:
        redis.sadd('projects:global:jobs:archived', job_id)
