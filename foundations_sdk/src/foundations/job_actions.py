"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

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
        from algorithms import train_model
        
        train_model = foundations.create_stage(train_model)
        model = train_model()
        model.run()

        foundations.get_queued_jobs()
        job_queue = foundations.cancel_queued_jobs(['209762cb-c767-4aea-bcaa-35b131982915'])
        print(job_queue)
        ```
    """
    from foundations_contrib.global_state import redis_connection
    from foundations.helpers.queued import list_jobs, remove_jobs, add_jobs_to_archive, job_project_names, remove_job_from_code_path
    from foundations_contrib.redis_pipeline_wrapper import RedisPipelineWrapper
    from foundations import config_manager

    all_queued_jobs = list_jobs(redis_connection)

    set_of_job_ids = set(list_of_job_ids)
    set_of_queued_jobs = set(all_queued_jobs)

    queued_jobs_ids = list(set_of_job_ids & set_of_queued_jobs)
    ids_for_not_queued_jobs = list(set_of_job_ids - set_of_queued_jobs)

    pipeline = RedisPipelineWrapper(redis_connection.pipeline())
    job_id_project_mapping = job_project_names(redis_connection, list_of_job_ids)
    remove_jobs(redis_connection, job_id_project_mapping)
    add_jobs_to_archive(redis_connection, list_of_job_ids)

    job_deployment_class = _job_deployment(config_manager)

    if hasattr(job_deployment_class, 'cancel_jobs'):
        cancellation_result = job_deployment_class.cancel_jobs(queued_jobs_ids)
    else:
        cancellation_result = _cancel_jobs(config_manager, queued_jobs_ids)
    
    pipeline.execute()

    cancellation_result_not_queued = {job_id: False for job_id in ids_for_not_queued_jobs}
    cancellation_result.update(cancellation_result_not_queued)

    return cancellation_result

def _job_deployment(config_manager):
    return config_manager['deployment_implementation']['deployment_type']

def _cancel_jobs(config_manager, job_ids):
    return {job_id: _cancel_job(config_manager, job_id) for job_id in job_ids}

def _cancel_job(config_manager, job_id):
    from foundations.helpers.queued import remove_job_from_code_path

    try:
        remove_job_from_code_path(config_manager, job_id)
        return True
    except IOError:
        return False