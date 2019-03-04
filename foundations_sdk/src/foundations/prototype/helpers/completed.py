"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

_COMPLETED_JOBS_KEY = 'projects:global:jobs:completed'
_ARCHIVED_JOBS_KEY = 'projects:global:jobs:archived'

def list_jobs(redis):
    return {job_id.decode() for job_id in redis.smembers(_COMPLETED_JOBS_KEY)}

def remove_jobs(redis, list_of_job_ids):
    for job_id in list_of_job_ids:
        redis.srem(_COMPLETED_JOBS_KEY, job_id)

def add_jobs_to_archive(redis, list_of_job_ids):
    for job_id in list_of_job_ids:
        redis.sadd(_ARCHIVED_JOBS_KEY, job_id)

def list_archived_jobs(redis):
    return {job_id.decode() for job_id in redis.smembers(_ARCHIVED_JOBS_KEY)}
