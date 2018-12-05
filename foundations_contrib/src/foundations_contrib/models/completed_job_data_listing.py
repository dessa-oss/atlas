"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class CompletedJobDataListing(object):
    """
    As below
    """
    @staticmethod
    def completed_job_data(project_name):
        """
        Returns all data for running and completed jobs under a specific project name. 

        Arguments:
            project_name {str} -- Name of project

        Returns:
            job_data {list} -- List with job data. Each element of the list contains a dictionary
             with project_name, job_id, user, job_parameters, input_params, output_metrics, status, start_time, completed_time.

        """
        from foundations_contrib.job_data_redis import JobDataRedis
        from foundations_contrib.job_data_shaper import JobDataShaper
        from foundations.global_state import redis_connection

        jobs_data = JobDataRedis.get_all_jobs_data(
            project_name, redis_connection)

        return JobDataShaper.shape_data(jobs_data)
