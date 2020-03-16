

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
        from foundations_contrib.global_state import redis_connection

        jobs_data = JobDataRedis.get_all_jobs_data(project_name, redis_connection)

        for job in jobs_data:
            job['output_metrics'] = JobDataShaper.shape_output_metrics(job['output_metrics'])

        return jobs_data


