"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.models.property_model import PropertyModel


class QueuedJob(PropertyModel):

    job_id = PropertyModel.define_property()
    queued_time = PropertyModel.define_property()
    project_name = PropertyModel.define_property()
    time_since_queued = PropertyModel.define_property()

    @staticmethod
    def find_async(async_redis, job_id):
        from foundations_contrib.models.queued_job_query import QueuedJobQuery
        from promise import Promise

        query = QueuedJobQuery(async_redis, job_id)
        promise = Promise.splat_all(query.exists(), query.queued_time(), query.project_name())
        return promise.splat_then(QueuedJob._make_queued_job_callback(job_id))

    @staticmethod
    def all():
        from foundations.global_state import redis_connection
        from promise import Promise
        from foundations_contrib.redis_pipeline_wrapper import RedisPipelineWrapper

        job_ids = [job_id.decode() for job_id in redis_connection.smembers('projects:global:jobs:queued')]
        pipeline = redis_connection.pipeline()
        async_redis = RedisPipelineWrapper(pipeline)

        async_jobs = [QueuedJob.find_async(async_redis, job_id) for job_id in job_ids]

        async_redis.execute()

        return Promise.all(async_jobs).get()

    @staticmethod
    def _make_queued_job_callback(job_id):
        from time import time

        def _resolution(exists, queued_time, project_name):
            if exists:
                queued_time = float(queued_time)
                project_name = project_name.decode()
                return QueuedJob(
                    job_id=job_id,
                    queued_time=queued_time,
                    project_name=project_name,
                    time_since_queued=time() - queued_time 
                )
            else:
                return None

        return _resolution