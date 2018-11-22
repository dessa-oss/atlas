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
    def get_all_jobs_data(project_name, redis_connection):
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
            job_ids, pipe)
        pipe.execute()
        return [future.get() for future in futures]

    @staticmethod
    def _create_redis_pipeline(redis_connection):
        from foundations.redis_pipeline_wrapper import RedisPipelineWrapper
        return RedisPipelineWrapper(redis_connection.pipeline())

    @staticmethod
    def _get_data_for_each_job(job_ids, pipe):
        return [JobDataRedis(pipe, job_id).get_job_data()
                for job_id in job_ids]

    @staticmethod
    def _fetch_project_job_ids(project_name, redis_connection):
        job_ids = redis_connection.smembers(
            'project:{}:jobs:running'.format(project_name))
        return [job_id.decode() for job_id in job_ids]

    def get_job_data(self):
        """
        Gets all data related to a given job from Redis.

        Returns:
            results {dict} -- Dictionary with project_name, job_id, user, job_parameters, input_params, output_metrics, status, start_time, completed_time.
        """
        from promise import Promise

        project_name = self._add_get_to_pipe('project')
        user = self._add_get_to_pipe('user')
        job_parameters = self._add_smembers_to_pipe_and_deserialize(
            'parameters')
        input_parameters = self._add_smembers_to_pipe_and_deserialize(
            'input_parameters')
        output_metrics = self._add_smembers_to_pipe_and_deserialize(
            'metrics')
        status = self._add_get_to_pipe('state')
        start_time = self._add_get_to_pipe(
            'start_time')
        completed_time = self._add_get_to_pipe(
            'completed_time')

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

    def _add_smembers_to_pipe_and_deserialize(self, parameter):
        return self._pipe.smembers('jobs:{}:{}'.format(self._job_id, parameter)).then(self._deserialize_set_members)

    def _deserialize_set_members(self, param_set):
        import json

        decoded_param_list = []

        for param in param_set:
            param = json.loads(param.decode())
            decoded_param_list.append(param)

        return decoded_param_list

    def _add_get_to_pipe(self, parameter):
        return self._pipe.get('jobs:{}:{}'.format(self._job_id, parameter)).then(self._decode_bytes)

    def _decode_bytes(self, data):
        return data.decode()
