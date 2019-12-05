"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_core_rest_api_components.common.models.property_model import PropertyModel

class Monitor(PropertyModel):

    @staticmethod
    def job_ids_from_monitors_dictionary(project_name, monitor_name, sort_kind='desc'):
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

            jobs_with_completed_time = list(filter(lambda job: job['completed_time'] is not None, internal_jobs))
            jobs_without_completed_time = list(filter(lambda job: job['completed_time'] is None, internal_jobs))
            jobs_with_completed_time.sort(key=lambda job: job['completed_time'],
                                          reverse=True if sort_kind == 'desc' else False)
            jobs_without_completed_time.sort(key=lambda job: job['creation_time'],
                                          reverse=True if sort_kind == 'desc' else False)
            return jobs_without_completed_time + jobs_with_completed_time

        return LazyResult(_callback)

    @staticmethod
    def delete_job(project_name, monitor_name, job_id):
        from foundations_core_rest_api_components.lazy_result import LazyResult
        return LazyResult(lambda: Monitor._delete_job_internal(project_name, monitor_name, job_id))

    @staticmethod
    def _delete_job_internal(project_name, monitor_name, job_id):
        from foundations_contrib.global_state import redis_connection

        redis_key = f'projects:{project_name}:monitors:{monitor_name}:jobs'
        result = redis_connection.srem(redis_key, job_id)

        if result == 0:
            return None
        
        return job_id