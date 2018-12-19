"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def set_project_name(project_name="default"):
    from foundations.global_state import foundations_context
    foundations_context.set_project_name(project_name)


def get_metrics_for_all_jobs(project_name):
    """
    Returns metrics for all jobs for a given project.

    # Arguments
        project_name (str): Name of the project to filter by.

    # Returns
        A Pandas DataFrame containing all of the results.
    """

    return _flattened_job_metrics(project_name)


def _flattened_job_metrics(project_name):
    from pandas import DataFrame, concat

    job_metadata_list = []
    input_params_list = []
    output_metrics_list = []

    for job_data in _project_job_data(project_name):
        _update_job_data(job_data, input_params_list,
                         output_metrics_list)
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


def _update_job_data(job_data, input_param_list, output_metrics_list):
    output_metrics_list.append(job_data['output_metrics'])
    del job_data['output_metrics']
    _shape_input_parameters(job_data, input_param_list)

def _shape_input_parameters(job_data, input_param_list):
    input_param = job_data['input_params']
    del job_data['input_params']
    del job_data['job_parameters']

    input_param_dict = {}

    for param in input_param:
        input_param_dict[param['name']] = param['value']

    input_param_list.append(input_param_dict)


def _project_job_data(project_name):
    from foundations_contrib.models.completed_job_data_listing import CompletedJobDataListing
    return CompletedJobDataListing.completed_job_data(project_name)
