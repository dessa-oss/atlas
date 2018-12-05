"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_rest_api.v2beta.models.property_model import PropertyModel


class Job(PropertyModel):

    job_id = PropertyModel.define_property()
    user = PropertyModel.define_property()
    project = PropertyModel.define_property()
    input_params = PropertyModel.define_property()
    output_metrics = PropertyModel.define_property()
    status = PropertyModel.define_property()
    start_time = PropertyModel.define_property()
    completed_time = PropertyModel.define_property()

    @staticmethod
    def all(project_name=None):
        from foundations_rest_api.lazy_result import LazyResult

        def _all():
            return Job._all_internal(project_name)

        return LazyResult(_all)

    @staticmethod
    def _all_internal(project_name):
        return list(Job._load_jobs(project_name))

    @staticmethod
    def _load_jobs(project_name):
        from foundations_contrib.job_data_redis import JobDataRedis
        from foundations.global_state import redis_connection

        jobs = []
        for job_properties in list(JobDataRedis.get_all_jobs_data(project_name, redis_connection)):
            job = Job._build_job_model(job_properties)
            jobs.append(job)
        Job._default_order(jobs)
        return jobs

    @staticmethod
    def _build_job_model(job_data):
        Job._reshape_input_params(job_data)
        Job._reshape_output_metrics(job_data)
        Job._update_job_properties(job_data)
        job_data['project'] = job_data['project_name']
        del job_data['project_name']
        return Job(**job_data)

    @staticmethod
    def _default_order(jobs):

        def get_sort_key(job):
            return job.start_time

        jobs.sort(key=get_sort_key, reverse=True)

    @staticmethod
    def _extract_job_parameters(job_data):
        run_data = job_data['job_parameters']
        del job_data['job_parameters']
        return run_data

    @staticmethod
    def _extract_input_params(job_data):
        input_params = job_data['input_params']
        del job_data['input_params']
        job_data['input_params'] = []
        return input_params

    @staticmethod
    def _extract_source_and_value(argument_value, run_data, stage_indices):
        if argument_value['type'] == 'stage':
            input_stage_index = stage_indices.get_index(
                argument_value['stage_uuid'])
            value = '{}-{}'.format(argument_value['stage_name'],
                                   input_stage_index)
            source = 'stage'
        elif argument_value['type'] == 'dynamic':
            value = run_data[argument_value['name']]
            source = 'placeholder'
        else:
            value = argument_value['value']
            source = 'constant'
        return value, source

    @staticmethod
    def _flatten_input_params(job_data, param, run_data, stage_indices):
        from foundations_rest_api.v2beta.models.extract_type import extract_type

        stage_index = stage_indices.get_index(param['stage_uuid'])
        name = '{}-{}'.format(param['argument']['name'], stage_index)
        argument_value = param['argument']['value']
        value, source = Job._extract_source_and_value(
            argument_value,
            run_data,
            stage_indices
        )

        value_type = extract_type(value)
        if 'unknown' in value_type:
            value_type = 'string'
            value = type(value).__name__

        job_data['input_params'].append(
            {
                'name': name,
                'value': value,
                'type': value_type,
                'source': source,
            }
        )

    @staticmethod
    def _repopulate_input_params(job_data, input_params, run_data, stage_indices):
        for param in input_params:
            Job._flatten_input_params(job_data, param, run_data, stage_indices)

    @staticmethod
    def _reshape_input_params(job_data):
        from foundations_rest_api.v2beta.models.index_allocator import IndexAllocator
        run_data = Job._extract_job_parameters(job_data)
        input_params = Job._extract_input_params(job_data)
        stage_indices = IndexAllocator()
        Job._repopulate_input_params(
            job_data, input_params, run_data, stage_indices)

    @staticmethod
    def _extract_output_metrics(job_data):
        output_metrics = job_data['output_metrics']
        del job_data['output_metrics']
        job_data['output_metrics'] = []
        output_metrics.sort(key=lambda metric: metric[0])
        return output_metrics

    @staticmethod
    def _reposition_metrics(metric, new_metrics):
        _, key, value = metric
        if not key in new_metrics:
            new_metrics[key] = value
        elif isinstance(new_metrics[key], list):
            new_metrics[key].append(value)
        else:
            new_metrics[key] = [new_metrics[key], value]

    @staticmethod
    def _repopulate_metrics(job_data, new_metrics):
        from foundations_rest_api.v2beta.models.extract_type import extract_type

        for key, value in new_metrics.items():
            job_data['output_metrics'].append(
                {
                    'name': key,
                    'value': value,
                    'type': extract_type(value)
                }
            )

    @staticmethod
    def _reshape_output_metrics(job_data):
        output_metrics = Job._extract_output_metrics(job_data)
        new_metrics = {}
        for metric in output_metrics:
            Job._reposition_metrics(metric, new_metrics)
        Job._repopulate_metrics(job_data, new_metrics)

    @staticmethod
    def _update_job_properties(properties):
        properties['start_time'] = Job._datetime_string(
            properties['start_time'])
        properties['completed_time'] = Job._datetime_string(
            properties['completed_time'])

    @staticmethod
    def _datetime_string(time):
        from datetime import datetime

        if time is None:
            return 'No time available'
        date_time = datetime.utcfromtimestamp(time)
        return date_time.isoformat()
