"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def set_project_name(project_name):
    from foundations.global_state import foundations_context
    foundations_context.set_project_name(project_name)


def get_metrics_for_all_jobs(project_name):
    from pandas import DataFrame

    data_frame = DataFrame(_flattened_job_metrics())

    return data_frame[data_frame['project_name'] == project_name]


def _flattened_job_metrics():
    from foundations.models.completed_job_data_listing import CompletedJobDataListing

    for job_data in CompletedJobDataListing.completed_job_data():
        job_parameters = job_data['job_parameters']
        del job_data['job_parameters']

        input_params = job_data['input_params']
        del job_data['input_params']

        output_metrics = job_data['output_metrics']
        del job_data['output_metrics']

        stage_uuids = list(set([param['stage_uuid']
                                for param in input_params]))

        for param in input_params:
            stage_uuid = param['stage_uuid']
            stage_index = stage_uuids.index(stage_uuid)

            stage_name = '{}-{}'.format(param['name'], stage_index)
            if param['value']['type'] == 'stage':
                stage_value = param['value']['stage_name']
            elif param['value']['type'] == 'dynamic':
                stage_value_key = param['value']['name']
                stage_value = job_parameters[stage_value_key]
            else:
                stage_value = param['value']['value']

            job_data[stage_name] = stage_value

        job_data.update(output_metrics)

        yield job_data
