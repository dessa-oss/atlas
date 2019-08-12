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
    duration = PropertyModel.define_property()
    tags = PropertyModel.define_property()
    artifacts = PropertyModel.define_property()

    @staticmethod
    def all(project_name=None, handle_duplicate_param_names=True):
        from foundations_core_rest_api_components.lazy_result import LazyResult

        def _all():
            return Job._all_internal(project_name, handle_duplicate_param_names)

        return LazyResult(_all)

    @staticmethod
    def _all_internal(project_name, handle_duplicate_param_names):
        return list(Job._load_jobs(project_name, handle_duplicate_param_names))

    @staticmethod
    def _load_jobs(project_name, handle_duplicate_param_names):
        from foundations_contrib.job_data_redis import JobDataRedis
        from foundations_contrib.input_parameter_indexer import InputParameterIndexer
        from foundations_contrib.global_state import redis_connection

        jobs = []
        jobs_data = InputParameterIndexer.index_input_parameters(project_name, JobDataRedis.get_all_jobs_data(project_name, redis_connection, True), handle_duplicate_param_names=handle_duplicate_param_names)

        for job_properties in list(jobs_data):
            job_properties['input_params'] = list(Job._filter_out_non_hyper_parameter_inputs(job_properties['input_params']))
            job = Job._build_job_model(job_properties)
            jobs.append(job)
        Job._default_order(jobs)
        return jobs

    @staticmethod
    def _filter_out_non_hyper_parameter_inputs(input_params):
        for param in input_params:
            if param['source'] == 'placeholder':
                yield param

    @staticmethod
    def _build_job_model(job_data):
        Job._extract_job_parameters(job_data)
        Job._reshape_output_metrics(job_data)
        Job._update_job_time_properties(job_data)
        Job._trim_metric_values(job_data)
        Job._retrieve_artifacts(job_data)
        job_data['project'] = job_data['project_name']
        del job_data['project_name']
        return Job(**job_data)

    @staticmethod
    def _default_order(jobs):
        infinite_date_string = '00000'

        def get_sort_key(job):
            if job.start_time:
                return job.start_time
            else:
                return infinite_date_string + job.job_id

        jobs.sort(key=get_sort_key, reverse=True)

    @staticmethod
    def _extract_job_parameters(job_data):
        run_data = job_data['job_parameters']
        del job_data['job_parameters']
        return run_data

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
    def _update_job_time_properties(properties):
        from datetime import datetime

        start_time = properties['start_time']
        completed_time = properties['completed_time']
        properties['start_time'] = Job._datetime_string(start_time)
        properties['completed_time'] = Job._datetime_string(completed_time)

        if completed_time:
            end_time = datetime.fromtimestamp(completed_time)
        else:
            end_time = datetime.now()

        if start_time:
            time_delta = end_time - datetime.fromtimestamp(start_time)
            total_seconds = time_delta.total_seconds()
            properties['duration'] = Job._total_seconds_to_duration(total_seconds)
        else:
            properties['duration'] = None

    @staticmethod
    def _trim_metric_values(job_data):
        from foundations_contrib.utils import is_string
        for metric in job_data['output_metrics']:
            if is_string(metric['value']):
                metric['value'] = metric['value'][:100]

    @staticmethod
    def _total_seconds_to_duration(total_seconds):
        total_seconds = int(total_seconds)
        days = total_seconds // 86400
        remaining_seconds = total_seconds % 86400
        hours = remaining_seconds // 3600
        remaining_seconds %= 3600
        minutes = remaining_seconds // 60
        remaining_seconds %= 60
        return '{}d{}h{}m{}s'.format(days, hours, minutes, remaining_seconds)

    @staticmethod
    def _datetime_string(time):
        from datetime import datetime

        if time is None:
            return None
        date_time = datetime.utcfromtimestamp(time)
        return date_time.isoformat()

    @staticmethod
    def _retrieve_artifacts(job_data):
        from foundations_rest_api.v2beta.models.job_artifact import JobArtifact
        job_id = job_data['job_id']
        job_data['artifacts'] = JobArtifact.all(job_id=job_id).evaluate()