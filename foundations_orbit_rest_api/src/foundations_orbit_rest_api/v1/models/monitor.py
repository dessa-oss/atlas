"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_core_rest_api_components.common.models.property_model import PropertyModel

class Monitor(PropertyModel):

    @staticmethod
    def job_ids_from_monitors_dictionary(project_name, monitor_name):
        from foundations_core_rest_api_components.lazy_result import LazyResult

        def _monitor_exists_in_project(project_name, monitor_name):
            from foundations_contrib.global_state import redis_connection

            return redis_connection.smembers(f'projects:{project_name}:monitors:{monitor_name}:jobs')

        def _callback():
            from foundations_contrib.global_state import redis_connection
            from foundations_contrib.job_data_redis import JobDataRedis

            if not _monitor_exists_in_project(project_name, monitor_name):
                return None

            serialized_job_ids = redis_connection.smembers(f'projects:{project_name}:monitors:{monitor_name}:jobs')
            job_ids = [serialized_job_id.decode() for serialized_job_id in serialized_job_ids]
            internal_jobs = JobDataRedis.all_jobs_by_list_of_job_ids(job_ids, redis_connection, False)

            return internal_jobs

        return LazyResult(_callback)
