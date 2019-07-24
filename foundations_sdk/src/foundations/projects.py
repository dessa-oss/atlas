"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def set_project_name(project_name="default"):
    """
    Sets the project a given job. This allows Foundations to know that multiple jobs belong to the same project. The project name is later used to retrieve metrics and analyze experiments

    Arguments:
        project_name {string} -- Optional name specifying which project the job is part of. If no project name is specified, the job will be deployed under the "default" project

    Returns:
        - This function doesn't return a value.

    Raises:
        - This method doesn't raise any exceptions.

    Example:
        ```python
        import foundations
        from algorithms import train_model

        foundations.set_project_name("my project")

        train_model = foundations.create_stage(train_model)
        model = train_model()
        deployment = model.run()
        ```
    """
    from foundations.global_state import current_foundations_context
    current_foundations_context().set_project_name(project_name)

def _get_metrics_for_all_jobs(project_name, include_input_params=False):
    """
    Returns metrics for all jobs for a given project.

    Arguments:
        project_name {string} -- Name of the project to filter by.
        include_input_params {boolean} -- Optional way to specify if metrics should include all model input metrics

    Returns:
        metrics {DataFrame} -- A Pandas DataFrame containing all of the results.

    Raises:
        ValueError -- An exception indicating that the requested project does not exist

    Example:
        ```python
        import foundations
        from algorithms import train_model, print_metrics

        train_model = foundations.create_stage(train_model)
        model = train_model()
        job_name = 'Experiment number 3'
        deployment = model.run(job_name=job_name)
        deployment.wait_for_deployment_to_complete()
        all_metrics = foundations.get_metrics_for_all_jobs(job_name)
        print_metrics(all_metrics)
        ```
    """

    from foundations_contrib.models.project_listing import ProjectListing
    from foundations.global_state import redis_connection

    project_info = ProjectListing.find_project(redis_connection, project_name)
    if project_info is None:
        raise ValueError('Project `{}` does not exist!'.format(project_name))

    return _flattened_job_metrics(project_name, include_input_params)

def get_metrics_for_all_jobs(project_name, include_input_params=False):
    """
    Returns metrics and tags for all jobs for a given project. This function is an experimental feature, and is under the foundations.prototype package

    Arguments:
        project_name {string} -- Name of the project to filter by.
        include_input_params {boolean} -- Optional way to specify if metrics should include all model input metrics

    Returns:
        metrics {DataFrame} -- A Pandas DataFrame containing all of the results.

    Raises:
        ValueError -- An exception indicating that the requested project does not exist

    Example:
        ```python
        import foundations
        from algorithms import train_model, print_metrics

        train_model = foundations.create_stage(train_model)
        foundations.set_tag('model', 'CNN')
        model = train_model()

        all_metrics = foundations.prototype.get_metrics_for_all_jobs(job_name)
        print_metrics(all_metrics)
        ```
    """
    import foundations
    from foundations_contrib.global_state import redis_connection
    from foundations.helpers.annotate import annotations_for_multiple_jobs
    from foundations_contrib.redis_pipeline_wrapper import RedisPipelineWrapper
    from pandas import DataFrame

    metrics = _get_metrics_for_all_jobs(project_name,include_input_params)

    if 'job_id' not in metrics:
        return metrics

    metric_rows = list(metrics.T.to_dict().values())

    job_annotations = annotations_for_multiple_jobs(redis_connection, metrics['job_id'])

    for row in metric_rows:
        annotations = job_annotations[row['job_id']]
        for key, value in annotations.items():
            tag_key = 'tag_{}'.format(key)
            row[tag_key] = value
    
    return DataFrame(metric_rows)

def set_tag(key, value):
    """
    Adds additional static, predetermined information as a tag to the job. This is a way to categorize attributes of a job that is not dynamically generated during runtime.

    Arguments:
        key {str} -- the name of the tag.
        value {number, str, bool, array of [number|str|bool], array of array of [number|str|bool]} -- the value associated with the given tag.

    Returns:
        - This function doesn't return a value.

    Raises:
        - This method doesn't raise any exceptions.

    Notes:
        If a tag is updated multiple times, Foundations will update the tag to the newest value, but return a warning indicating that the
        key has been updated.

    Example:
        ```python
        import foundations
        from algorithms import train_model_xgboost

        train_model = foundations.create_stage(train_model_xgboost)
        model = train_model()
        foundations.set_tag('model', 'xgboost')
        model.run()
        ```
    """
    from foundations_contrib.global_state import log_manager, current_foundations_context, message_router
    from foundations_contrib.producers.tag_set import TagSet

    pipeline_context = current_foundations_context().pipeline_context()

    if _job_running(pipeline_context):
        tag_set_producer = TagSet(message_router, pipeline_context.file_name, key, value)
        tag_set_producer.push_message()
    elif not log_manager.foundations_not_running_warning_printed():
        logger = log_manager.get_logger(__name__)
        logger.warning('Script not run with Foundations.')
        log_manager.set_foundations_not_running_warning_printed()

def _job_running(pipeline_context):
    try:
        return pipeline_context.file_name is not None
    except:
        return False

def _flattened_job_metrics(project_name, include_input_params):
    from pandas import DataFrame, concat

    job_metadata_list = []
    input_params_list = []
    output_metrics_list = []

    for job_data in _project_job_data(project_name, include_input_params):
        _update_job_data(
            job_data,
            input_params_list,
            output_metrics_list,
            include_input_params
        )
        _update_datetime(job_data)
        job_metadata_list.append(job_data)

    return concat([DataFrame(job_metadata_list), DataFrame(input_params_list), DataFrame(output_metrics_list)], axis=1, sort=False)


def _update_datetime(job_data):
    from foundations.utils import datetime_string

    if 'start_time' in job_data:
        job_data['start_time'] = datetime_string(job_data['start_time'])
    if 'completed_time' in job_data:
        job_data['completed_time'] = datetime_string(
            job_data['completed_time'])


def _update_job_data(job_data, input_param_list, output_metrics_list, include_input_params):
    output_metrics_list.append(job_data['output_metrics'])
    del job_data['output_metrics']
    _shape_input_parameters(job_data, input_param_list, include_input_params)


def _shape_input_parameters(job_data, input_param_list, include_input_params):
    input_param_dict = {}

    if include_input_params:
        input_param = job_data['input_params']
        for param in input_param:
            input_param_dict[param['name']] = param['value']

    input_param_dict.update(job_data['job_parameters'])
    input_param_list.append(input_param_dict)

    del job_data['input_params']
    del job_data['job_parameters']


def _project_job_data(project_name, include_input_params):
    from foundations_contrib.models.completed_job_data_listing import CompletedJobDataListing
    return CompletedJobDataListing.completed_job_data(project_name, include_input_params)
