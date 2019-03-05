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

def remove_jobs(redis, job_id_project_mapping):
    for job_id, project_name in job_id_project_mapping.items():
        redis.srem(_COMPLETED_JOBS_KEY, job_id)
        redis.srem('project:{}:jobs:running'.format(project_name), job_id)

def job_project_names(redis, list_of_job_ids):
    return {job_id: _job_project_name(redis, job_id) for job_id in list_of_job_ids}

def _job_project_name(redis, job_id):
    project_name = redis.get('jobs:{}:project'.format(job_id))
    if project_name:
        return project_name.decode()

def add_jobs_to_archive(redis, list_of_job_ids):
    for job_id in list_of_job_ids:
        redis.sadd(_ARCHIVED_JOBS_KEY, job_id)

def list_archived_jobs(redis):
    return {job_id.decode() for job_id in redis.smembers(_ARCHIVED_JOBS_KEY)}
