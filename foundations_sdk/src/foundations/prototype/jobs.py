"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def get_queued_jobs():
    """
    Retrieves all deployed jobs which are in queue to run, but are not currently running

    Arguments:
        - This method doesn't receive any arguments.

    Returns:
        queued_jobs (DataFrame): A Pandas DataFrame containing all of the jobs which are in queue.

    Raises:
        - This method doesn't raise any exceptions.

    Example:
        ```python
        import foundations
        import foundations.prototype
        from algorithms import train_model
        
        train_model = foundations.create_stage(train_model)
        model = train_model()
        model.run()

        job_queue = foundations.prototype.get_queued_jobs()
        print(job_queue)
        ```
    """
    from pandas import DataFrame
    from foundations_contrib.models.queued_job import QueuedJob

    job_attributes = [job.attributes for job in QueuedJob.all()]

    return DataFrame(job_attributes)

def cancel_queued_jobs(list_of_job_ids):
    """
    Cancels jobs which are currently in the queue, preventing them from eventually running when resources are available

    Arguments:
        list_of_job_ids {array} -- a list of job_ids as strings to cancel from the Foundations job queue

    Returns:
        cancelled_statuses {dict} -- A dictionary indicating if the cancelling of a queued job was successful or not for each input job_id

    Raises:
        - This method doesn't raise any exceptions.

    Example:
        ```python
        import foundations
        import foundations.prototype
        from algorithms import train_model
        
        train_model = foundations.create_stage(train_model)
        model = train_model()
        model.run()

        foundations.prototype.get_queued_jobs()
        job_queue = foundations.prototype.cancel_queued_jobs(['209762cb-c767-4aea-bcaa-35b131982915'])
        print(job_queue)
        ```
    """
    from foundations_contrib.global_state import redis_connection
    from foundations.prototype.helpers.queued import list_jobs, remove_jobs, add_jobs_to_archive, job_project_names, remove_job_from_code_path
    from foundations_contrib.redis_pipeline_wrapper import RedisPipelineWrapper
    from foundations import config_manager

    queued_jobs = list_jobs(redis_connection)
    pipeline = RedisPipelineWrapper(redis_connection.pipeline())
    job_id_project_mapping = job_project_names(redis_connection, list_of_job_ids)
    remove_jobs(redis_connection, job_id_project_mapping)
    add_jobs_to_archive(redis_connection, list_of_job_ids)

    for job_id in list_of_job_ids:
        try:
            remove_job_from_code_path(config_manager, job_id)
        except IOError:
            continue
    
    pipeline.execute()

    return {job_id: job_id in queued_jobs for job_id in list_of_job_ids}

def archive_jobs(list_of_job_ids):
    """
    Archives completed jobs, removing them from any project results on both the GUI and SDK. This function doesn't delete the jobs permanently, but only hides them from appearing again.

    Arguments:
        list_of_job_ids {array} -- a list of job_ids as strings to archive

    Returns:
        archived_statuses {dict} -- A dictionary indicating if the archiving was successful or not for each input job_id

    Raises:
        - This method doesn't raise any exceptions.

    Example:
        ```python
        import foundations
        import foundations.prototype
        from algorithms import train_model

        foundations.get_metrics_for_all_jobs("Demo_Project")
        job_queue = foundations.prototype.archive_jobs(['209762cb-c767-4aea-bcaa-35b131982915'])
        print(job_queue)
        ```
    """
    from foundations_contrib.global_state import redis_connection
    from foundations.prototype.helpers.completed import list_jobs, remove_jobs, add_jobs_to_archive, job_project_names
    from foundations_contrib.redis_pipeline_wrapper import RedisPipelineWrapper

    completed_jobs = list_jobs(redis_connection)

    pipeline = RedisPipelineWrapper(redis_connection.pipeline())
    job_id_project_mapping = job_project_names(redis_connection, list_of_job_ids)
    remove_jobs(redis_connection, job_id_project_mapping)
    add_jobs_to_archive(redis_connection, list_of_job_ids)
    pipeline.execute()

    return {job_id: job_id in completed_jobs for job_id in list_of_job_ids}
