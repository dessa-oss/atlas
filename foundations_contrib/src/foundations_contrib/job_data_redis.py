"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class JobDataRedis(object):
    """
    As below

    Arguments:
        pipeline {redis.Redis().pipeline()} -- Redis pipeline instance
        job_id {str} -- Job id for job to fetch
    """

    def __init__(self, pipe, job_id):
        self._pipe = pipe
        self._job_id = job_id

    @staticmethod
    def get_all_jobs_data(project_name, redis_connection, include_input_params):
        """
        Gets all data related to jobs in a given project from Redis.

        Arguments:
            project_name {str} -- Name of project to fetch data for
            redis_connection {redis.Redis()} -- Redis connection to pipe to

        Returns:
            job_data {list} -- List with job data. Each element of the list contains a dictionary
             with project_name, job_id, user, job_parameters, input_params, output_metrics, status, start_time, completed_time.
        """

        job_ids = JobDataRedis._fetch_project_job_ids(
            project_name, redis_connection)

        pipe = JobDataRedis._create_redis_pipeline(redis_connection)
        futures = JobDataRedis._get_data_for_each_job(
            job_ids, pipe, include_input_params)
        pipe.execute()
        return [future.get() for future in futures]

    @staticmethod
    def list_all_completed_jobs(redis_connection):
        completed_job_keys = redis_connection.keys('jobs:*:completed_time')
        return [key.decode().split(':')[1] for key in completed_job_keys]
    
    @staticmethod
    def is_job_completed(job_id, redis_connection):
        return job_id in JobDataRedis.list_all_completed_jobs(redis_connection)

    @staticmethod
    def _create_redis_pipeline(redis_connection):
        from foundations_contrib.redis_pipeline_wrapper import RedisPipelineWrapper
        return RedisPipelineWrapper(redis_connection.pipeline())

    @staticmethod
    def _get_data_for_each_job(job_ids, pipe, include_input_params):
        return [JobDataRedis(pipe, job_id).get_job_data(include_input_params)
                for job_id in job_ids]

    @staticmethod
    def _fetch_project_job_ids(project_name, redis_connection):
        job_ids = redis_connection.smembers(
            'project:{}:jobs:running'.format(project_name))
        return [job_id.decode() for job_id in job_ids]

    def get_job_data(self, include_input_params):
        """
        Gets all data related to a given job from Redis.

        Returns:
            results {dict} -- Dictionary with project_name, job_id, user, job_parameters, input_params, output_metrics, status, start_time, completed_time.
        """
        from promise import Promise

        project_name = self._add_decoded_get_to_pipe('project')
        user = self._add_decoded_get_to_pipe('user')
        job_parameters = self._add_decoded_get_to_pipe(
            'parameters').then(self._deserialize_dict)
        if include_input_params:
            input_parameters = self._add_get_to_pipe(
                'input_parameters').then(self._deserialize_list)
        else:
            input_parameters = Promise()
            input_parameters.fulfill([])
        output_metrics = self._add_lrange_to_pipe_and_deserialize('metrics')
        status = self._add_decoded_get_to_pipe('state')
        start_time = self._add_decoded_get_to_pipe('start_time').then(self._make_float)
        completed_time = self._add_decoded_get_to_pipe(
            'completed_time').then(self._make_float)

        list_of_properties = Promise.all(
            [
                project_name,
                user,
                job_parameters,
                input_parameters,
                output_metrics,
                status,
                start_time,
                completed_time
            ]
        )

        return list_of_properties.then(self._seperate_args)

    def _seperate_args(self, args):
        def seperate_args_inner(project_name,
                                user,
                                job_parameters,
                                input_parameters,
                                output_metrics,
                                status,
                                start_time,
                                completed_time):
            return {
                'project_name': project_name,
                'job_id': self._job_id,
                'user': user,
                'job_parameters': job_parameters,
                'input_params': input_parameters,
                'output_metrics': output_metrics,
                'status': status,
                'start_time': start_time,
                'completed_time': completed_time
            }
        return seperate_args_inner(*args)

    def _add_lrange_to_pipe_and_deserialize(self, parameter):
        return self._pipe.lrange('jobs:{}:{}'.format(self._job_id, parameter), 0, -1).then(self._deserialize_set_members)

    def _deserialize_set_members(self, param_set):
        from foundations_internal.fast_serializer import deserialize

        if param_set is None:
            return []

        decoded_param_list = []

        for param in param_set:
            param = deserialize(param)
            decoded_param_list.append(param)

        return decoded_param_list

    def _add_decoded_get_to_pipe(self, parameter):
        return self._add_get_to_pipe(parameter).then(self._decode_bytes)

    def _add_get_to_pipe(self, parameter):
        return self._pipe.get('jobs:{}:{}'.format(self._job_id, parameter))

    def _decode_bytes(self, data):
        if data is None:
            return data
        return data.decode()

    def _deserialize_list(self, data):
        return self._deserialize_or_default(data, [])

    def _deserialize_dict(self, data):
        return self._deserialize_or_default(data, {})

    def _deserialize_or_default(self, data, default):
        from foundations_internal.foundations_serializer import deserialize
        return deserialize(data) or default

    def _make_float(self, time_string):
        if time_string is None:
            return time_string
        return float(time_string)