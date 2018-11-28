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
    """Returns metrics for all jobs for a given project

    Arguments:
        project_name {str} -- Name of the project to filter by

    Returns:
        [pandas.DataFrame] -- Pandas DataFrame containing all of the results
    """

    return _flattened_job_metrics(project_name)


def _flattened_job_metrics(project_name):
    from pandas import DataFrame, concat

    job_metadata_list = []
    input_params_list = []
    output_metrics_list = []

    for job_data in _project_job_data(project_name):
        stage_uuids = []
        _update_job_data(job_data, input_params_list,
                         output_metrics_list, stage_uuids)
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


def _update_job_data(job_data, input_param_list, output_metrics_list, stage_uuids):
    output_metrics_list.append(job_data['output_metrics'])
    del job_data['output_metrics']

    _fill_job_parameters(job_data, input_param_list, stage_uuids)


def _fill_job_parameters(job_data, input_param_list, stage_uuids):
    job_parameters = job_data['job_parameters']
    del job_data['job_parameters']

    input_params = job_data['input_params']
    del job_data['input_params']

    _update_uuid_list(input_params, stage_uuids)
    index_tracker = _store_parameter_indices(input_params, stage_uuids)
    input_param_dict = {}

    for param in input_params:
        stage_name = _parameter_name(param, stage_uuids, index_tracker)
        stage_value = _stage_value(param, job_parameters)
        input_param_dict[stage_name] = stage_value

    input_param_list.append(input_param_dict)


def _store_parameter_indices(input_params, stage_uuids):
    from collections import defaultdict
    index_tracker = defaultdict(list)

    for param in input_params:
        index_tracker[param['name']].append(
            stage_uuids.index(param['stage_uuid']))

    for key in index_tracker:
        index_tracker[key] = sorted(index_tracker[key], key=int)

    return index_tracker


def _parameter_name(parameter, stage_uuids, index_tracker):
    stage_index = stage_uuids.index(parameter['stage_uuid'])
    stage_name = parameter['name']

    argument_index = index_tracker[stage_name].index(stage_index)
    index_tracker[stage_name][argument_index] = 'X'

    if argument_index > 0:
        return '{}-{}'.format(stage_name, argument_index)
    return parameter['name']


def _stage_value(parameter, job_parameters):
    if parameter['value']['type'] == 'stage':
        return parameter['value']['stage_name']

    if parameter['value']['type'] == 'dynamic':
        stage_value_key = parameter['value']['name']
        return job_parameters[stage_value_key]

    return parameter['value']['value']


def _project_job_data(project_name):
    from foundations.models.completed_job_data_listing import CompletedJobDataListing
    return CompletedJobDataListing.completed_job_data(project_name)


def _update_uuid_list(input_params, stage_uuids):
    for param in input_params:
        if not param['stage_uuid'] in stage_uuids:
            stage_uuids.append(param['stage_uuid'])
    return stage_uuids
