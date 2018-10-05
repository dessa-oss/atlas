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

    from pandas import DataFrame

    return DataFrame(_flattened_job_metrics(project_name))


def _flattened_job_metrics(project_name):
    stage_uuids = []

    for job_data in _project_job_data(project_name):
        _update_job_data(job_data, stage_uuids)
        _update_datetime(job_data)
        yield job_data

def _update_datetime(job_data):
    from foundations.utils import datetime_string
    job_data['start_time'] = datetime_string(job_data['start_time'])
    job_data['completed_time'] = datetime_string(job_data['completed_time'])


def _update_job_data(job_data, stage_uuids):
    output_metrics = job_data['output_metrics']
    del job_data['output_metrics']

    _fill_job_parameters(job_data, stage_uuids)

    job_data.update(output_metrics)


def _fill_job_parameters(job_data, stage_uuids):
    job_parameters = job_data['job_parameters']
    del job_data['job_parameters']

    input_params = job_data['input_params']
    del job_data['input_params']

    _update_uuid_list(input_params, stage_uuids)

    for param in input_params:
        if param['name'] =='<args>':
            stage_name = _parameter_name(param, stage_uuids)
        else:
            stage_name = param['name']
            
        stage_value = _stage_value(param, job_parameters)

        job_data[stage_name] = stage_value


def _parameter_name(parameter, stage_uuids):
    stage_index = stage_uuids.index(parameter['stage_uuid'])
    return '{}-{}'.format(parameter['name'], stage_index)


def _stage_value(parameter, job_parameters):
    if parameter['value']['type'] == 'stage':
        return parameter['value']['stage_name']

    if parameter['value']['type'] == 'dynamic':
        stage_value_key = parameter['value']['name']
        return job_parameters[stage_value_key]

    return parameter['value']['value']


def _project_job_data(project_name):
    from foundations.models.completed_job_data_listing import CompletedJobDataListing

    for job_data in CompletedJobDataListing.completed_job_data():
        if project_name == job_data['project_name']:
            yield job_data


def _update_uuid_list(input_params, stage_uuids):
    for param in input_params:
        if not param['stage_uuid'] in stage_uuids:
            stage_uuids.append(param['stage_uuid'])
    return stage_uuids

def _datetime_string(time):
    from datetime import datetime

    if time is None:
        return 'No time available'
    date_time = datetime.utcfromtimestamp(time)
    return date_time.isoformat()