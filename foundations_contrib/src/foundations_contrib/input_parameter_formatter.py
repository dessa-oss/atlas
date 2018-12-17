"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class InputParameterFormatter(object):

    def __init__(self, input_parameters, job_parameters, stage_rank):
        self._stage_rank = stage_rank
        self._input_parameters = input_parameters
        self._job_parameters = job_parameters

    def format_input_parameters(self):
        formatted_input_parameters = []

        for param in self._input_parameters:
            self._append_parameter_info(
                param, formatted_input_parameters, self._stage_rank)

        return formatted_input_parameters

    def _append_parameter_info(self, param, formatted_input_parameters, stage_rank):
        from foundations_rest_api.v2beta.models.extract_type import extract_type

        param_name = self._index_input_param(param, stage_rank)
        param_value, param_source = self._evaluate_input_param_value(
            param, stage_rank)

        value_type = extract_type(param_value)
        if 'unknown' in value_type:
            value_type = 'string'
            param_value = type(param_value).__name__

        input_param = {
            'name': param_name,
            'value': param_value,
            'type': value_type,
            'source': param_source
        }

        if not self._contains_split_at(input_param):
            formatted_input_parameters.append(input_param)

    def _contains_split_at(self, input_param):
        if input_param['type'] == 'string':
            return 'split_at' in input_param['value']

        return False

    def _index_input_param(self, param, stage_ranks):
        if param['stage_uuid'] not in stage_ranks:
            self._update_stage_rank(param['stage_uuid'], stage_ranks)

        stage_rank = stage_ranks[param['stage_uuid']]
        name = '{}-{}'.format(param['argument']['name'], str(stage_rank))
        return name

    def _update_stage_rank(self, stage_uuid, stage_ranks):
        index = max(stage_ranks.values(), default=0) + 1
        stage_ranks[stage_uuid] = index

    def _evaluate_input_param_value(self, param, stage_rank):
        argument_value = param['argument']['value']
        if argument_value['type'] == 'stage':
            stage_uuid = argument_value['stage_uuid']

            if stage_uuid not in stage_rank.keys():
                self._update_stage_rank(stage_uuid, stage_rank)

            input_stage_rank = stage_rank[stage_uuid]
            value = '{}-{}'.format(argument_value['stage_name'],
                                   input_stage_rank)
            source = 'stage'
        elif argument_value['type'] == 'dynamic':
            value = self._job_parameters[argument_value['name']]
            source = 'placeholder'
        else:
            value = argument_value['value']
            source = 'constant'
        return value, source
