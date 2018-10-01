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

    return DataFrame(_flattened_job_metrics(project_name))


def _flattened_job_metrics(project_name):
    from foundations.models.completed_job_data_listing import CompletedJobDataListing

    stage_uuids = []

    for job_data in CompletedJobDataListing.completed_job_data():
        if project_name == job_data['project_name']:
            job_parameters = job_data['job_parameters']
            del job_data['job_parameters']

            input_params = job_data['input_params']
            del job_data['input_params']

            output_metrics = job_data['output_metrics']
            del job_data['output_metrics']

            _uuid_list(input_params, stage_uuids)

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

def _uuid_list(input_params, stage_uuids):
    for param in input_params:
        if not param['stage_uuid'] in stage_uuids:
            stage_uuids.append(param['stage_uuid'])
    return stage_uuids