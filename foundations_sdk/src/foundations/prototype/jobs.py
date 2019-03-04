"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def get_queued_jobs():
    from pandas import DataFrame
    from foundations_contrib.models.queued_job import QueuedJob

    job_attributes = [job.attributes for job in QueuedJob.all()]

    return DataFrame(job_attributes)

def archive_jobs(list_of_job_ids):
    from foundations_contrib.global_state import redis_connection
    from foundations.prototype.helpers.completed import list_jobs, remove_jobs
    from foundations_contrib.redis_pipeline_wrapper import RedisPipelineWrapper

    completed_jobs = list_jobs(redis_connection)

    pipeline = RedisPipelineWrapper(redis_connection.pipeline())
    remove_jobs(redis_connection, list_of_job_ids)
    pipeline.execute()

    return {job_id: job_id in completed_jobs for job_id in list_of_job_ids}
