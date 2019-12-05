"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.models.extract_type import extract_type


class InputParameterFormatter(object):

    def __init__(self, input_parameters, job_parameters, stage_rank, handle_duplicate_param_names=True):
        self._stage_rank = stage_rank
        self._input_parameters = input_parameters
        self._job_parameters = job_parameters
        self._handle_duplicate_param_names = handle_duplicate_param_names

    def format_input_parameters(self):
        return list(self._valid_parameter_infos())

    def _valid_parameter_infos(self):
        for param in self._parameter_infos():
            if not self._contains_split_at(param):
                yield param

    def _parameter_infos(self):
        for param in self._input_parameters:
            yield self._get_parameter_info(param, self._stage_rank)

    def _get_parameter_info(self, param, stage_rank):
        param_name = self._index_input_param(param, stage_rank)
        param_value, param_source = self._evaluate_input_param_value(
            param['argument']['value'], stage_rank)

        value_type = extract_type(param_value)
        if 'unknown' in value_type:
            value_type = 'string'
            param_value = type(param_value).__name__

        return {
            'name': param_name,
            'value': param_value,
            'type': value_type,
            'source': param_source
        }

    def _contains_split_at(self, input_param):
        if input_param['type'] == 'string':
            return 'split_at' in input_param['value']

        return False

    def _index_input_param(self, param, stage_ranks):
        if param['stage_uuid'] not in stage_ranks:
            self._update_stage_rank(param['stage_uuid'], stage_ranks)

        stage_rank = stage_ranks[param['stage_uuid']]
        param_name = param['argument']['name']

        if self._handle_duplicate_param_names:
            return '{}-{}'.format(param_name, str(stage_rank))
        return param_name

    def _update_stage_rank(self, stage_uuid, stage_ranks):
        index = max(stage_ranks.values(), default=0) + 1
        stage_ranks[stage_uuid] = index

    def _evaluate_input_param_value(self, argument_value, stage_rank):
        if argument_value['type'] == 'stage':
            value = self._stage_value(argument_value, stage_rank)
            source = 'stage'
        elif argument_value['type'] == 'dynamic':
            value = self._job_parameters[argument_value['name']]
            source = 'placeholder'
        elif argument_value['type'] == 'list':
            value = self._list_parameter_value(argument_value, stage_rank)
            source = 'list'
        elif argument_value['type'] == 'dict':
            value = 'dict'
            source = 'dict'
        else:
            value = argument_value['value']
            source = 'constant'
        return value, source

    def _stage_value(self, argument_value, stage_rank):
        stage_uuid = argument_value['stage_uuid']

        if stage_uuid not in stage_rank.keys():
            self._update_stage_rank(stage_uuid, stage_rank)

        input_stage_rank = stage_rank[stage_uuid]
        return '{}-{}'.format(argument_value['stage_name'], input_stage_rank)

    def _list_parameter_value(self, argument_value, stage_rank):
        return [self._evaluate_input_param_value(parameter, stage_rank)[0] for parameter in argument_value['parameters']]
