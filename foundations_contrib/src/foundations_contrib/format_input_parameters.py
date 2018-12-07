"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class FormatInputParameters(object):
    
    def __init__(self, project_name, input_parameters, redis):
        self._project_name = project_name
        self._redis = redis
        self._input_parameters = input_parameters
    
    def format_input_parameters(self):
        stage_rank = self._get_stage_rank()

        formatted_input_parameters = []

        for param in self._input_parameters:
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
        return formatted_input_parameters
    
    def _get_input_parameter_names(self):
        input_parameter_names = self._redis.smembers('projects:{}:input_parameter_names'.format(self._project_name))
        return self._deserialize_set(input_parameter_names)
    
    def _deserialize_set(self, params):
        import json
        deserialized_set = []
        for param in params:
            param = json.loads(param.decode())
            deserialized_set.append(param)
        return deserialized_set

        
    def _index_input_param(self, param, stage_rank):
        stage_rank = stage_ranks[param['stage_uuid']]
        name = '{}-{}'.format(param['argument']['name'], str(stage_rank))
        return name

    def _get_stage_rank(self):
        input_param_names = self._get_input_parameter_names()
        stage_uuid_rank = {}

        for param in input_param_names:           
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
    
            
    def _evaluate_input_param_value(self, param, stage_rank):
        argument_value = param['argument']['value']
        if argument_value['type'] == 'stage':
            input_stage_rank = stage_rank[argument_value['stage_uuid']]
            value = '{}-{}'.format(argument_value['stage_name'], input_stage_rank)
            source = 'stage'
        elif argument_value['type'] == 'dynamic':
            value = run_data[argument_value['name']]
            source = 'placeholder'
        else:
            value = argument_value['value']
            source = 'constant'
        return value, source

#desired end state
        #    {
        #         'name': name,
        #         'value': value,
        #         'type': value_type,
        #         'source': source,
        #     }