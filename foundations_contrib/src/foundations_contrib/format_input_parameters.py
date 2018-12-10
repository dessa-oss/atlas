"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class FormatInputParameters(object):
    
    def __init__(self, project_name, input_parameters, job_parameters, redis):
        self._project_name = project_name
        self._redis = redis
        self._input_parameters = input_parameters
        self._job_parameters = job_parameters
    
    def format_input_parameters(self):
        stage_rank = self._get_stage_rank()

        formatted_input_parameters = []

        for param in self._input_parameters:
            self._append_parameter_info(param, formatted_input_parameters, stage_rank)

        return formatted_input_parameters
    
    def _append_parameter_info(self, param, formatted_input_parameters, stage_rank):
        from foundations_rest_api.v2beta.models.extract_type import extract_type
        param_name = self._index_input_param(param, stage_rank)
        param_value, param_source = self._evaluate_input_param_value(param, stage_rank)

        value_type = extract_type(param_value)
        if 'unknown' in value_type:
            value_type = 'string'
            param_value = type(param_value).__name__
        
        formatted_input_parameters.append(
            {
                'name': param_name,
                'value': param_value,
                'type': value_type,
                'source': param_source
            }
        )

    
    def _get_stage_times(self):
        stage_times = self._redis.smembers('projects:{}:stage_time'.format(self._project_name))
        return self._deserialize_set(stage_times)
    
    def _deserialize_set(self, params):
        import json
        deserialized_set = []
        for param in params:
            param = json.loads(param.decode())
            deserialized_set.append(param)
        return deserialized_set

        
    def _index_input_param(self, param, stage_ranks):
        stage_rank = stage_ranks[param['stage_uuid']]
        name = '{}-{}'.format(param['argument']['name'], str(stage_rank))
        return name

    def _get_stage_rank(self):
        stage_times = self._get_stage_times()
        stage_uuid_rank = {}

        for stage_time in stage_times:           
            self._record_earliest_stage_time(stage_time, stage_uuid_rank)

        times = sorted(stage_uuid_rank.values())

        for key in sorted(stage_uuid_rank.keys()):
            value = stage_uuid_rank[key]
            stage_uuid_rank[key] = times.index(value)
            times[times.index(value)] = 'x'

        return stage_uuid_rank
    
    def _record_earliest_stage_time(self, stage_time, stage_uuid_rank):
        if stage_time['stage_uuid'] in stage_uuid_rank.keys():
            if stage_time['time'] < stage_uuid_rank[stage_time['stage_uuid']]:
                stage_uuid_rank[stage_time['stage_uuid']] = stage_time['time']
        else:
            stage_uuid_rank.update({stage_time['stage_uuid']: stage_time['time']})
            
    def _evaluate_input_param_value(self, param, stage_rank):
        argument_value = param['argument']['value']
        if argument_value['type'] == 'stage':
            input_stage_rank = stage_rank[argument_value['stage_uuid']]
            value = '{}-{}'.format(argument_value['stage_name'], input_stage_rank)
            source = 'stage'
        elif argument_value['type'] == 'dynamic':
            value = self._job_parameters[argument_value['name']]
            source = 'placeholder'
        else:
            value = argument_value['value']
            source = 'constant'
        return value, source
