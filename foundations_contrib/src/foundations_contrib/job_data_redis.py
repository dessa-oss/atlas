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

    def __init__(self, pipe, job_id, project_name):
        self._pipe = pipe
        self._job_id = job_id
        self._project_name = project_name

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
        futures = JobDataRedis._get_data_for_each_job(job_ids, pipe, project_name)

        pipe.execute()
        return [future.get() for future in futures]

    @staticmethod
    def _create_redis_pipeline(redis_connection):
        from foundations_contrib.redis_pipeline_wrapper import RedisPipelineWrapper
        return RedisPipelineWrapper(redis_connection.pipeline())

    @staticmethod
    def _get_data_for_each_job(job_ids, pipe, project_name):
        return [JobDataRedis(pipe, job_id, project_name).get_job_data()
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
        import json

        user = self._add_get_to_pipe('user')
        job_parameters = self._add_get_to_pipe('parameters').then(self._json_loads)
        input_parameters = self._add_get_to_pipe('input_parameters').then(self._json_loads)
        output_metrics = self._add_lrange_to_pipe_and_deserialize('metrics')
        status = self._add_get_to_pipe('state')
        start_time = self._add_get_to_pipe('start_time').then(self._make_float)
        completed_time = self._add_get_to_pipe('completed_time').then(self._make_float)
        input_parameter_keys = self._pipe.smembers('projects:{}:input_parameter_keys'.format(self._project_name)).then(self._deserialize_dictionary)

        list_of_properties = Promise.all(
            [
                user,
                job_parameters,
                input_parameters,
                output_metrics,
                status,
                start_time,
                completed_time,
                input_parameter_keys
            ]
        )

        return list_of_properties.then(self._seperate_args)

    def _seperate_args(self, args):
        def seperate_args_inner(
                                user,
                                job_parameters,
                                input_parameters,
                                output_metrics,
                                status,
                                start_time,
                                completed_time,
                                input_parameter_keys):
            return {
                'project_name': self._project_name,
                'job_id': self._job_id,
                'user': user,
                'job_parameters': job_parameters,
                'input_params': self._index_input_param(input_parameters, input_parameter_keys),
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
    
    def _deserialize_dictionary(self, param_dict):
        import json
        new_param_dict = []
        for param in param_dict:
            param = json.loads(param.decode())
            new_param_dict.append(param)
        return new_param_dict

    def _add_get_to_pipe(self, parameter):
        return self._pipe.get('jobs:{}:{}'.format(self._job_id, parameter)).then(self._decode_bytes)

    def _decode_bytes(self, data):
        if data is None:
            return data
        return data.decode()

    def _json_loads(self, data):
        if data is None:
            return []
        import json
        return json.loads(data)

    def _make_float(self, time_string):
        if time_string is None:
            return time_string
        return float(time_string)

    def _index_input_param(self, input_params, input_parameter_keys):
        stage_ranks = self._get_stage_ranks(input_parameter_keys)
        for param in input_params:
            stage_rank = stage_ranks[param['stage_uuid']]
            param['argument']['name'] += '_' + str(stage_rank)
        return input_params

    
    def _get_stage_ranks(self, input_param_keys):
        stage_uuid_rank = {}
        for param in input_param_keys:
            
            if param['stage_uuid'] in stage_uuid_rank.keys():
                if param['time'] < stage_uuid_rank[param['stage_uuid']]:
                    stage_uuid_rank[param['stage_uuid']] = param['time']
            else:
                stage_uuid_rank.update({param['stage_uuid']: param['time']})

        times = sorted(stage_uuid_rank.values())

        for key, value in stage_uuid_rank.items():
            stage_uuid_rank[key] = times.index(value)
            times[times.index(value)] = 'x'
        return stage_uuid_rank