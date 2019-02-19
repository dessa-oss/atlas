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

        query = QueuedJobQuery(async_redis, job_id)
        promise = QueuedJob._nice_promise_all(query.exists(), query.queued_time(), query.project_name())
        return QueuedJob._nice_promise_all_then(promise, _resolution)

    @staticmethod
    def all():
        return []

    @staticmethod
    def _nice_promise_all(*promises):
        from promise import Promise
        return Promise.all(promises)

    @staticmethod
    def _nice_promise_all_then(promise, callback):
        def _explode_callback(args):
            return callback(*args)
        return promise.then(_explode_callback)
