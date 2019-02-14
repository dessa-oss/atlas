"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def set_project_name(project_name="default"):
    from foundations.global_state import foundations_context
    foundations_context.set_project_name(project_name)


def get_metrics_for_all_jobs(project_name, include_input_params=False):
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
